import re

import pytest

from lib import install_and_verify, log_text, ota_success, read_firmware, require_login, wait_boot


@pytest.mark.tc('TC-OTA-006')
@pytest.mark.ota_gatekeeper
@pytest.mark.positive
def test_install_exact_newer_release(ota_connected_device, ota_versions):
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  target = ota_versions['beta']
  if original >= target:
    pytest.skip(f'Requires firmware older than {target}')
  install_and_verify(device, target)


@pytest.mark.tc('TC-OTA-007')
@pytest.mark.fw_only('2.3.0')
@pytest.mark.regression
@pytest.mark.negative
def test_nonforced_downgrade_blocked(ota_connected_device, ota_versions):
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  beta, stable = ota_versions['beta'], ota_versions['stable']

  if original != beta:
    install_and_verify(device, beta, force=(original > beta))

  require_login(device)

  before = read_firmware(device)
  response = log_text(device.ota.install(str(stable), timeout=15))

  assert re.search(rf'E408.*v?{beta}.*v?{stable}.*force', response, re.IGNORECASE), response
  assert read_firmware(device) == before


@pytest.mark.tc('TC-OTA-008')
@pytest.mark.fw_only('2.3.0')
@pytest.mark.ota_gatekeeper
@pytest.mark.positive
def test_forced_downgrade(ota_connected_device, ota_versions):
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  beta, stable = ota_versions['beta'], ota_versions['stable']
  if original != beta:
    install_and_verify(device, beta, force=(original > beta))
  install_and_verify(device, stable, force=True)


@pytest.mark.tc('TC-OTA-009')
@pytest.mark.regression
@pytest.mark.positive
def test_force_reinstall_same_version(ota_connected_device):
  device = ota_connected_device
  version, before, state = read_firmware(device)
  assert state.lower() == 'valid'
  response = device.ota.install(str(version), force=True)
  output = log_text(response)
  assert 'W409' in output, output
  assert 'downloading' in output, output
  ota_success(response, version, version)
  wait_boot(device)
  assert read_firmware(device) == (version, 'ota_1' if before == 'ota_0' else 'ota_0', 'valid')


@pytest.mark.tc('TC-OTA-010')
@pytest.mark.regression
@pytest.mark.positive
def test_alternate_inactive_partition(ota_connected_device, ota_versions):
  device = ota_connected_device
  original, original_slot, _ = read_firmware(device)
  other = ota_versions['beta'] if original != ota_versions['beta'] else ota_versions['stable']
  for target in (other, original):
    before, slot, _ = read_firmware(device)
    expected_slot = 'ota_1' if slot == 'ota_0' else 'ota_0'
    require_login(device)
    response = device.ota.install(str(target), force=(target <= before))
    output = log_text(response)
    assert re.search(rf'target partition\s*:?\s*{expected_slot}', output, re.IGNORECASE), output
    ota_success(response, before, target)
    wait_boot(device)
    assert read_firmware(device) == (target, expected_slot, 'valid')
  assert read_firmware(device)[1] == original_slot


@pytest.mark.tc('TC-OTA-011')
@pytest.mark.regression
@pytest.mark.positive
def test_ota_complete_progress(ota_connected_device):
  device = ota_connected_device
  version, slot, _ = read_firmware(device)
  response = device.ota.install(str(version), force=True)
  output = log_text(response)
  expected = 'ota_1' if slot == 'ota_0' else 'ota_0'
  assert re.search(rf'current\s+v?{re.escape(str(version))}\s*\({slot}\)\s*->\s*target partition\s+{expected}', output), output
  assert re.search(rf'downloading\s+https?://\S+/v{version}/sentry_fw7\.bin', output), output
  assert re.search(rf'image:\s*sentry_fw7\s+v?{version}', output), output
  progress = [int(x) for x in re.findall(r'\[OTA\]\s+(\d+)%', output)]
  assert progress == list(range(10, 101, 10)), f'Expected progress 10..100 by 10: {progress}'
  ota_success(response, version, version)
  wait_boot(device)
  assert read_firmware(device) == (version, expected, 'valid')


@pytest.mark.tc('TC-OTA-032')
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize('bad_version', ['abc', '2.3', '2.3.0.1', '-1.0.0'])
def test_reject_malformed_version(ota_connected_device, bad_version):
  device = ota_connected_device
  original = read_firmware(device)
  response = log_text(device.ota.install(bad_version, timeout=10))
  assert 'E414' in response, response
  assert read_firmware(device) == original


@pytest.mark.tc('TC-OTA-033')
@pytest.mark.regression
@pytest.mark.negative
def test_reject_missing_release(ota_connected_device):
  device = ota_connected_device
  original = read_firmware(device)
  # Use a future, correctly formatted version not present in the fw_7 server manifest.
  response = log_text(device.ota.install('99.99.99', timeout=30))
  assert 'E415' in response, response
  assert read_firmware(device) == original
