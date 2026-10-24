import pytest
from lib import check_versions, log_text, require_login, wait_boot


@pytest.mark.tc('TC-OTA-050')
@pytest.mark.regression
@pytest.mark.positive
def test_custom_ota_server_used_for_check(ota_connected_device, ota_server_url):
  server = ota_server_url
  device = ota_connected_device
  try:
    device.ota.server(server)
    assert server in log_text(device.ota.server(until=server, timeout=10))
    response = device.ota.check()
    assert check_versions(response)['stable'] is not None
  finally:
    device.ota.server(ota_server_url)


@pytest.mark.tc('TC-OTA-051')
@pytest.mark.regression
@pytest.mark.positive
def test_custom_ota_server_persists_reboot(ota_connected_device, ota_server_url):
  server = ota_server_url
  device = ota_connected_device
  try:
    device.ota.server(server)
    device._connector.write_command('reboot')
    boot = log_text(wait_boot(device))
    assert f'custom update server: {server}' in boot, boot
    require_login(device)
    assert server in log_text(device.ota.server(until=server, timeout=10))
    assert check_versions(device.ota.check())['beta'] is not None
  finally:
    require_login(device)
    device.ota.server(ota_server_url)


@pytest.mark.tc('TC-OTA-052')
@pytest.mark.regression
@pytest.mark.positive
def test_reset_ota_server_to_default(ota_connected_device, ota_server_url):
  server = ota_server_url
  device = ota_connected_device
  try:
    device.ota.server(server)
    device.ota.server('default')
    expected = 'https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/fw7/'
    assert expected in log_text(device.ota.server(until=expected, timeout=10))
    device._connector.write_command('reboot')
    wait_boot(device)
    require_login(device)
    assert expected in log_text(device.ota.server(until=expected, timeout=10))
  finally:
    require_login(device)
    device.ota.server(ota_server_url)
