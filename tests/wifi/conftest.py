"""Wi-Fi fixtures for fw_7. Each scenario restores the known lab AP."""

import pytest

from config import PASSWORD, SSID
from lib import has_active_wifi_connection


def ensure_lab_wifi(device):
  assert SSID and PASSWORD, 'Configure SSID and PASSWORD for Wi-Fi HIL tests'
  status = device.wifi.status()
  if status.connected and status.ssid == SSID:
    return

  if status.connected:
    assert device.wifi.disconnect(), f'Cannot leave the previous AP: {status}'

  device.wifi.reconnect()
  status = device.wifi.status()
  if status.connected and status.ssid == SSID:
    return

  result = device.wifi.connect(SSID, PASSWORD)
  status = device.wifi.status()
  assert status.connected and status.ssid == SSID, (
    f'Cannot restore lab Wi-Fi: {result.response}; status={status}'
  )


@pytest.fixture
def wifi_device(ota_device):
  assert SSID and PASSWORD, 'Configure SSID and PASSWORD for Wi-Fi HIL tests'
  try:
    yield ota_device
  finally:
    # A negative test, forget, or reboot must not break the following tests.
    ensure_lab_wifi(ota_device)


@pytest.fixture
def wifi_connected(wifi_device):
  ensure_lab_wifi(wifi_device)
  return wifi_device


@pytest.fixture
def wifi_disconnected(wifi_connected):
  assert wifi_connected.wifi.disconnect()
  assert not has_active_wifi_connection(wifi_connected)
  return wifi_connected
