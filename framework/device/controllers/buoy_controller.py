import re
from dataclasses import dataclass

from lib import ResponseParseError, UARTConnector, UnexpectedResponseError


@dataclass
class BuoyNetwork:
  number: int
  ssid: str
  rssi: int
  channel: int | None = None


@dataclass
class BuoyStatus:
  connected: bool
  ssid: str | None
  ip: str | None
  rssi: int | None


@dataclass
class BuoyConnectResult:
  connected: bool
  error: str | None
  response: list[str]


class BuoyController:
  _CONNECT_ERRORS = ('E101', 'E102', 'E103', 'E104', 'E105', 'E108', 'E111', 'E112', 'E113')
  # The link is not fully ready until the internet/NTP checks finish (WF-1).
  # Stopping at "connected to" leaves pending logs that can swallow the next UART command.
  _CONNECTION_RESULT = ('time: synced via NTP', 'W106', 'W114', *_CONNECT_ERRORS)

  def __init__(self, connector: UARTConnector):
    self._connector = connector

  def scan(self) -> list[BuoyNetwork]:
    # fw_7 emits "[LINK] scanning..." followed by numbered APs, without
    # the older "found N networks:" header or a reliable completion marker.
    response = self._connector.execute_command(
      'scan', until=('dBm', 'found 0 networks:', 'E108'), timeout=15,
    )
    if any('E108' in line for line in response):
      return []

    response.extend(self._connector.read_until_quiet(timeout=5, idle_timeout=0.6))
    return self._parse_networks(response)

  def connect(self, ssid: str | int | None = None, password: str | None = None,
              by_number: bool = False) -> BuoyConnectResult:
    self._connector.write_command('connect')
    # WF-1 is an interactive command: scan -> SSID/number -> password.
    response = self._connector.wait_for_response(('Enter SSID', 'SSID or number', 'Enter network'), timeout=15)

    if by_number and isinstance(ssid, str):
      value = str(self._get_network_number(response, ssid))
    else:
      value = '' if ssid is None else str(ssid)

    self._connector.write_command(value)
    ssid_response = self._connector.wait_for_response(
      ('password:', 'Password:', 'Enter password', 'E111', 'E102', 'E108'), timeout=10,
    )
    response.extend(ssid_response)
    if self._error_code(ssid_response):
      return self._parse_connect_result(response)

    self._connector.write_command(password or '')
    response.extend(self._connector.wait_for_response(self._CONNECTION_RESULT, timeout=45))
    return self._parse_connect_result(response)

  def reconnect(self) -> BuoyConnectResult:
    response = self._connector.execute_command('reconnect', until=self._CONNECTION_RESULT, timeout=45)
    return self._parse_connect_result(response)

  def disconnect(self) -> bool:
    response = self._connector.execute_command(
      'disconnect', until=('[LINK] disconnected', 'WiFi: disconnected', 'wifi station: disconnected', 'W115'),
      timeout=10,
    )
    return not any('W115' in line for line in response) and any(
      'disconnected' in line.lower() for line in response
    )

  def forget(self) -> list[str]:
    # WF-3 does not specify a stable completion message for forget.
    return self._connector.execute_command('forget')

  def net(self) -> list[str]:
    # WF-4 specifies IP / gateway / DNS / MAC but does not fix the wire format.
    return self._connector.execute_command('net')

  def ping(self, host: str | None = None) -> list[str]:
    # With no host, firmware uses its documented default: 8.8.8.8.
    return self._connector.execute_command('ping' if host is None else f'ping {host}')

  def time(self) -> list[str]:
    # E121 (time not synchronized) is returned unmodified to the caller.
    return self._connector.execute_command('time')

  def status(self) -> BuoyStatus:
    # fw_7 status ends at heap:, not at the RSSI in the middle of the output.
    response = self._connector.execute_command('status', until='heap:', timeout=10)
    return self._parse_status(response)

  # region Service Methods

  @staticmethod
  def _error_code(response: list[str]) -> str | None:
    match = re.search(r'\bE1\d{2}\b', '\n'.join(response))
    return match.group(0) if match else None

  def _parse_networks(self, response: list[str]) -> list[BuoyNetwork]:
    networks: list[BuoyNetwork] = []
    for line in response:
      index = re.search(r'\[\s*(\d+)\s*\]', line)
      if not index:
        continue

      if 'SSID:' in line and 'RSSI:' in line:
        ssid_match = re.search(r'SSID:\s*(.*?)\s+RSSI:', line, re.I)
        rssi_match = re.search(r'RSSI:\s*(-?\d+)', line, re.I)
      else:
        ssid_match = re.search(r'\[\s*\d+\s*\]\s*(.*?)\s+-?\d+\s*dBm', line, re.I)
        rssi_match = re.search(r'(-?\d+)\s*dBm', line, re.I)

      if not ssid_match or not rssi_match:
        continue

      channel_match = re.search(r'\bch\s*:?\s*(\d+)', line, re.I)
      networks.append(BuoyNetwork(
        number=int(index.group(1)), ssid=ssid_match.group(1).strip(),
        rssi=int(rssi_match.group(1)),
        channel=int(channel_match.group(1)) if channel_match else None,
      ))
    return networks

  def _parse_connect_result(self, response: list[str]) -> BuoyConnectResult:
    error = self._error_code(response)
    if error:
      return BuoyConnectResult(False, error, response)

    if any("connected to '" in line or 'W114' in line for line in response):
      return BuoyConnectResult(True, None, response)

    raise UnexpectedResponseError(f'Unknown buoy connection response: {response}')

  def _parse_status(self, response: list[str]) -> BuoyStatus:
    # Only the latest 'link:' field is authoritative. Other Wi-Fi log lines
    # and the saved network do not indicate an active connection.
    status = BuoyStatus(False, None, None, None)

    for line in response:
      if re.search(r'\blink:\s*buoy link down\b', line, re.I):
        status = BuoyStatus(False, None, None, None)
        continue

      match = re.search(
        r"\blink:\s*buoy link '([^']+)',\s*ip\s+(\d{1,3}(?:\.\d{1,3}){3})",
        line, re.I,
      )
      if not match:
        continue

      rssi = re.search(r'\brssi\s+(-?\d+)\s*dBm', line, re.I)
      status = BuoyStatus(
        match.group(2) != '0.0.0.0', match.group(1), match.group(2),
        int(rssi.group(1)) if rssi else None,
      )

    return status

  def _get_network_number(self, response: list[str], ssid: str) -> int:
    for network in self._parse_networks(response):
      if network.ssid == ssid:
        return network.number
    raise ResponseParseError(f'Network {ssid!r} was not found in connect scan: {response}')

  # endregion
