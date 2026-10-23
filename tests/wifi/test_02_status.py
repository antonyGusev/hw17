"""WF-4: status and network discovery."""

import re

import pytest

from config import SSID


@pytest.mark.tc('TC-WIFI-006')
@pytest.mark.regression
@pytest.mark.positive
def test_connected_status_and_network_details(wifi_connected):
  status = wifi_connected.wifi.status()
  assert status.connected and status.ssid == SSID, status
  assert status.ip and status.ip != '0.0.0.0' and status.rssi is not None, status
  response = wifi_connected._connector.execute_command(
    'net', until=('MAC', 'mac', 'E1'), timeout=10,
  )
  output = '\n'.join(response)
  assert re.search(r'\bIP\b\s*:?[ \t]*\d{1,3}(?:\.\d{1,3}){3}', output, re.I), output
  assert re.search(r'\b(?:gateway|gw)\b\s*:', output, re.I), output
  assert re.search(r'\bDNS\b\s*:', output, re.I), output
  assert re.search(r'\bMAC\b\s*:', output, re.I), output


@pytest.mark.tc('TC-WIFI-007')
@pytest.mark.regression
@pytest.mark.positive
def test_disconnected_status(wifi_disconnected):
  status = wifi_disconnected.wifi.status()
  assert not status.connected and status.ip is None, status
  result = wifi_disconnected.wifi.reconnect()
  assert result.connected, result.response


@pytest.mark.tc('TC-WIFI-008')
@pytest.mark.regression
@pytest.mark.positive
def test_scan_includes_reference_ssid_and_rssi(wifi_device):
  networks = wifi_device.wifi.scan()
  matching = [network for network in networks if network.ssid == SSID]
  assert matching, f'SSID {SSID!r} missing from scan: {networks}'
  assert all(network.number > 0 and -100 <= network.rssi <= 0 for network in matching)
