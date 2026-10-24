import pytest

from lib import install_and_verify, log_text, ota_success, read_firmware, require_login, wait_boot


@pytest.mark.tc('TC-OTA-004')
@pytest.mark.ota_gatekeeper
@pytest.mark.positive
def test_channel_update(ota_connected_device, ota_versions):
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  target = ota_versions['beta']
  if original >= target:
    pytest.skip(f'Requires version below beta {target}; DUT has {original}')
  response = device.ota.update(beta=True)
  ota_success(response, original, target)
  wait_boot(device)
  assert read_firmware(device)[0] == target
  assert read_firmware(device)[2].lower() == 'valid'


@pytest.mark.tc('TC-OTA-005')
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize('channel', ['stable', 'beta'])
def test_channel_up_to_date_no_reboot(ota_connected_device, ota_versions, channel):
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  target = ota_versions[channel]
  if original != target:
    install_and_verify(device, target, force=(original > target))
  require_login(device)
  before = read_firmware(device)
  response = log_text(device.ota.update(beta=(channel == 'beta')))
  if '[OTA] success:' in response:
    # The firmware reflashed the same version instead of returning 'already up to date'.
    # Consume the reboot to avoid corrupting the next test's UART session.
    wait_boot(device)
    pytest.fail(f'OTA-4: same-version update unexpectedly flashed and rebooted:\n{response}')
  assert '[OTA] already up to date' in response, response
  assert 'downloading' not in response.lower()
  assert 'Rebooting' not in response
  assert read_firmware(device) == before
