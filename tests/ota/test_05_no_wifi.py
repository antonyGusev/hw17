import pytest

from lib import has_active_wifi_connection, read_firmware
from helpers import ensure_connection, log_text


@pytest.mark.tc('TC-OTA-014')
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize('command', ['check', 'update', 'update beta', 'install 2.3.0', 'broken', 'url https://example.invalid/fw7.bin'])
def test_ota_without_wifi(ota_connected_device, command):
  device = ota_connected_device
  before = read_firmware(device)
  assert device.wifi.disconnect()
  assert not has_active_wifi_connection(device)
  try:
    response = log_text(device.ota.execute(command, until=('E002', 'E411'), timeout=20))
    assert 'E002' in response, response
    assert read_firmware(device) == before
  finally:
    ensure_connection(device)
