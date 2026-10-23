import pytest

from lib import read_firmware
from helpers import check_versions, require_login, install_and_verify, log_text


@pytest.mark.tc('TC-OTA-003')
@pytest.mark.ota_gatekeeper
@pytest.mark.positive
def test_ota_check_reports_channels(ota_connected_device, ota_versions):
  device = ota_connected_device
  output = device.ota.check()
  assert 'E003' not in log_text(output), output
  versions = check_versions(output)
  assert versions['current'] == read_firmware(device)[0]
  assert versions['stable'] == ota_versions['stable']
  assert versions['beta'] == ota_versions['beta']


@pytest.mark.tc('TC-OTA-034')
@pytest.mark.regression
@pytest.mark.positive
def test_ota_check_on_newer_beta(ota_connected_device, ota_versions):
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  if original != ota_versions['beta']:
    install_and_verify(device, ota_versions['beta'], force=(original > ota_versions['beta']))
  require_login(device)
  response = log_text(device.ota.check())
  assert 'running newer than stable' in response, response


@pytest.mark.tc('TC-OTA-053')
@pytest.mark.regression
@pytest.mark.negative
def test_stable_update_does_not_downgrade_beta(ota_connected_device, ota_versions):
  device = ota_connected_device
  version, partition, state = read_firmware(device)
  if version != ota_versions['beta']:
    pytest.skip('Runs only with 2.3.0 beta installed; no implicit firmware changes.')
  response = log_text(device.ota.update(timeout=15))
  assert 'E408' in response or 'running newer than stable' in response, response
  assert read_firmware(device) == (version, partition, state)
