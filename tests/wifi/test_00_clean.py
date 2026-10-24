"""First-state Wi-Fi checks: must run before any test stores credentials."""

import pytest


@pytest.mark.tc('TC-WIFI-025')
@pytest.mark.first
@pytest.mark.negative
def test_time_unavailable_before_first_ntp_sync(ota_device):
  response = ota_device._connector.execute_command('time', until='E121', timeout=10)
  assert any('E121' in line for line in response), response


@pytest.mark.tc('TC-WIFI-020')
@pytest.mark.first
@pytest.mark.negative
def test_reconnect_without_saved_credentials(ota_device):
  result = ota_device.wifi.reconnect()
  assert result.error == 'E113', result.response
  assert not ota_device.wifi.status().connected
