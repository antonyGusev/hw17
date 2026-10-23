"""WF-1/WF-3: connecting, disconnecting and retained credentials."""

import re

import pytest
import serial

from config import PASSWORD, SSID
from lib import DeviceTimeoutError, has_active_wifi_connection, wait_for_condition


@pytest.mark.tc('TC-WIFI-001')
@pytest.mark.smoke
@pytest.mark.positive
def test_connect_by_ssid(wifi_disconnected):
  result = wifi_disconnected.wifi.connect(SSID, PASSWORD)
  status = wifi_disconnected.wifi.status()
  output = '\n'.join(result.response)
  assert result.connected, output
  assert "got ip" in output.lower(), output
  assert re.search(r"connected to '.*', rssi -?\d+ dBm", output), output
  assert status.connected and status.ssid == SSID and status.ip != '0.0.0.0', status
  assert status.rssi is not None, status
  assert 'time: synced via NTP' in output or 'W106' in output, output


@pytest.mark.tc('TC-WIFI-002')
@pytest.mark.regression
@pytest.mark.positive
def test_connect_by_scan_index(wifi_disconnected):
  result = wifi_disconnected.wifi.connect(SSID, PASSWORD, by_number=True)
  status = wifi_disconnected.wifi.status()
  assert result.connected, result.response
  assert status.connected and status.ssid == SSID and status.rssi is not None, status


@pytest.mark.tc('TC-WIFI-003')
@pytest.mark.regression
@pytest.mark.positive
def test_reconnect_with_saved_credentials(wifi_disconnected):
  result = wifi_disconnected.wifi.reconnect()
  assert result.connected, result.response
  assert has_active_wifi_connection(wifi_disconnected)
  assert wifi_disconnected.wifi.status().ssid == SSID


@pytest.mark.tc('TC-WIFI-004')
@pytest.mark.regression
@pytest.mark.positive
def test_disconnect_preserves_saved_credentials(wifi_connected):
  assert wifi_connected.wifi.disconnect()
  assert not has_active_wifi_connection(wifi_connected)
  assert wifi_connected.help()
  result = wifi_connected.wifi.reconnect()
  assert result.connected, result.response
  assert wifi_connected.wifi.status().ssid == SSID


@pytest.mark.tc('TC-WIFI-005')
@pytest.mark.regression
@pytest.mark.positive
def test_saved_credentials_survive_reboot_without_auto_connect(wifi_connected):
  boot = wifi_connected.reboot()
  output = '\n'.join(boot)
  assert re.search(r'known network.*reconnect', output, re.I), boot
  assert not has_active_wifi_connection(wifi_connected), 'Unexpected auto-connect after reboot'
  result = wifi_connected.wifi.reconnect()
  assert result.connected, result.response
  assert wifi_connected.wifi.status().ssid == SSID


@pytest.mark.tc('TC-WIFI-034')
@pytest.mark.regression
@pytest.mark.positive
def test_saved_credentials_survive_power_cycle(wifi_connected, hil):
  device = wifi_connected
  try:
    device.close()
    hil.power_cycle()

    def open_uart():
      try:
        device.open()
        return True
      except (serial.SerialException, OSError):
        return False

    wait_for_condition(open_uart, timeout=30, interval=0.5)
    def cli_ready():
      try:
        return any('Commands (' in line for line in device.help())
      except DeviceTimeoutError:
        return False

    wait_for_condition(cli_ready, timeout=30, interval=0.5)
    assert not has_active_wifi_connection(device), 'Unexpected auto-connect after power cycle'
    result = device.wifi.reconnect()
    assert result.connected, result.response
    assert device.wifi.status().ssid == SSID
  finally:
    if not device.is_open:
      device.open()
