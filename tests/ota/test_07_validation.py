import re

import pytest

from lib import read_firmware
from helpers import require_login, install_and_verify, log_text, ota_success, wait_boot


@pytest.mark.tc('TC-OTA-018')
@pytest.mark.regression
@pytest.mark.positive
def test_first_boot_self_check_pending_then_valid(ota_connected_device, ota_versions):
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  target = ota_versions['beta'] if original < ota_versions['beta'] else original
  response = device.ota.install(str(target), force=(target == original))
  ota_success(response, original, target)
  boot = log_text(wait_boot(device))
  pending = re.search(r'new firmware,\s*PENDING_VERIFY\s*-\s*self-check', boot)
  valid = re.search(r'self-check passed, firmware marked VALID', boot)
  assert pending and valid and pending.start() < valid.start(), boot
  assert read_firmware(device)[0] == target
  assert read_firmware(device)[2].lower() == 'valid'


@pytest.mark.tc('TC-OTA-019')
@pytest.mark.regression
@pytest.mark.negative
def test_broken_image_automatic_rollback(ota_connected_device):
  device = ota_connected_device
  original = read_firmware(device)
  device.ota.broken(wait=False)
  logs = log_text(device.wait_for_log('Rolling back', timeout=180))
  assert 'self-check FAILED' in logs, logs
  assert 'Rolling back' in logs, logs
  wait_boot(device)
  assert read_firmware(device) == original


@pytest.mark.tc('TC-OTA-029')
@pytest.mark.regression
@pytest.mark.positive
def test_manual_rollback(ota_connected_device, ota_versions):
  device = ota_connected_device
  original, original_slot, _ = read_firmware(device)
  other = ota_versions['stable'] if original == ota_versions['beta'] else ota_versions['beta']
  install_and_verify(device, other, force=(other < original))
  version, slot, _ = read_firmware(device)
  require_login(device)
  response = log_text(device.ota.rollback())
  assert 'E416' not in response and 'E417' not in response, response
  wait_boot(device)
  assert read_firmware(device) == (original, original_slot, 'valid')
