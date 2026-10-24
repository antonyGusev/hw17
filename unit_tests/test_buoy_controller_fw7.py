import pytest

from framework.device.controllers.buoy_controller import BuoyController, BuoyStatus


class FakeConnector:
  def __init__(self, response):
    self.response = response
    self.calls = []

  def execute_command(self, command, until=None, timeout=None):
    self.calls.append((command, until, timeout))
    return self.response


@pytest.mark.parametrize('link, expected', [
  ('link:     buoy link down (known: none)', BuoyStatus(False, None, None, None)),
  ('link:     buoy link down (known: antony_g5)', BuoyStatus(False, None, None, None)),
  ("link:     buoy link 'antony_g5', ip 192.168.68.104, rssi -52 dBm (excellent), ch 5",
   BuoyStatus(True, 'antony_g5', '192.168.68.104', -52)),
  ("link:     buoy link 'antony_g5', ip 0.0.0.0, rssi -80 dBm (weak), ch 5",
   BuoyStatus(False, 'antony_g5', '0.0.0.0', -80)),
])
def test_parse_fw7_status(link, expected):
  response = [
    'status', 'I (1) sentry: === SWM-2 status ===',
    f'I (2) sentry:   {link}', 'I (3) sentry:   heap: 258 KB free',
  ]
  assert BuoyController(FakeConnector([]))._parse_status(response) == expected


def test_latest_status_field_wins_over_stale_logs():
  controller = BuoyController(FakeConnector([]))
  response = [
    "I (1) sentry:   link: buoy link 'antony_g5', ip 192.168.68.104, rssi -50 dBm",
    'I (2) sentry:   link: buoy link down (known: antony_g5)',
  ]
  assert not controller._parse_status(response).connected


def test_status_waits_for_heap_instead_of_rssi():
  connector = FakeConnector([
    "I (2) sentry:   link: buoy link 'antony_g5', ip 192.168.68.104, rssi -52 dBm",
    'I (3) sentry:   heap: 258 KB free',
  ])
  assert BuoyController(connector).status().connected
  assert connector.calls == [('status', 'heap:', 10)]


def test_reconnect_waits_for_ntp_terminal_event():
  response = [
    "I (1) sentry: [LINK] connected to 'antony_g5', rssi -52 dBm",
    'I (2) sentry: [LINK] fleet network reachable (internet OK)',
    'I (3) sentry: [LINK] time: synced via NTP, 19:21:47',
  ]
  connector = FakeConnector(response)
  assert BuoyController(connector).reconnect().connected
  assert 'time: synced via NTP' in connector.calls[0][1]
  assert "connected to '" not in connector.calls[0][1]


def test_ntp_failure_warning_does_not_cancel_wifi_connection():
  response = [
    "I (1) sentry: [LINK] connected to 'antony_g5', rssi -52 dBm",
    'W (2) sentry: W106 [LINK] time: NTP sync failed',
  ]
  assert BuoyController(FakeConnector(response)).reconnect().connected


class ScanConnector:
  def __init__(self, scan_header, scan_tail):
    self.scan_header = scan_header
    self.scan_tail = scan_tail
    self.calls = []

  def execute_command(self, command, until=None, timeout=None):
    self.calls.append((command, until, timeout))
    return list(self.scan_header)

  def wait_for_response(self, until, timeout):
    self.calls.append(('wait', until, timeout))
    return list(self.scan_tail)


def test_scan_waits_until_scan_count_and_last_network():
  connector = ScanConnector(
    ['scan', 'I (1) sentry: found 2 networks:',
     'I (2) sentry: [ 1] lab_ap -45 dBm'],
    ['I (3) sentry: [ 2] guest_ap -72 dBm'],
  )
  networks = BuoyController(connector).scan()
  assert [(network.number, network.ssid, network.rssi) for network in networks] == [
    (1, 'lab_ap', -45), (2, 'guest_ap', -72),
  ]
  assert connector.calls[0] == ('scan', ('networks:', 'E108'), 15)
  assert connector.calls[1] == ('wait', ('[ 2]', '[2]'), 5)


def test_scan_zero_networks_needs_no_followup_read():
  connector = ScanConnector(['scan', 'found 0 networks:'], [])
  assert BuoyController(connector).scan() == []
  assert len(connector.calls) == 1
