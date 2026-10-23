import re

import pytest
import serial

from config import OTA_PRISTINE_SINGLE_SLOT, OTA_THROTTLED_TRANSFER, OTA_DOWNLOAD_START_FAILURE_URL
from lib import read_firmware, wait_for_condition
from helpers import require_login, log_text, ota_success, wait_boot


@pytest.mark.tc('TC-OTA-020')
@pytest.mark.regression
@pytest.mark.negative
def test_power_cut_during_pending_verify(ota_connected_device, ota_versions, hil):
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  target = ota_versions['beta'] if original < ota_versions['beta'] else original
  try:
    result = device.ota.install(str(target), force=(target == original))
    ota_success(result, original, target)
    pending = log_text(device.wait_for_log('PENDING_VERIFY', timeout=90))
    assert 'PENDING_VERIFY' in pending, pending
    # Cut power immediately after observing the pending state.
    hil.power_off()
    device.close()
    hil.power_on()

    def open_uart():
      try:
        device.open()
        return True
      except (serial.SerialException, OSError):
        return False

    wait_for_condition(open_uart, timeout=30, interval=0.5)
    wait_boot(device)
    version, _, state = read_firmware(device)
    assert state.lower() == 'valid', (version, state)
    assert version in (original, target), f'Unexpected image after reset: {version}'
  finally:
    if not device.is_open:
      device.open()


@pytest.mark.tc('TC-OTA-030')
@pytest.mark.regression
@pytest.mark.negative
def test_rollback_without_previous_image(ota_connected_device):
  if OTA_PRISTINE_SINGLE_SLOT != '1':
    pytest.skip('Requires freshly flashed single-slot DUT; set OTA_PRISTINE_SINGLE_SLOT=1')
  device = ota_connected_device
  before = read_firmware(device)
  response = log_text(device.ota.rollback(timeout=15))
  assert 'E416' in response, response
  assert read_firmware(device) == before


@pytest.mark.tc('TC-OTA-031')
@pytest.mark.regression
@pytest.mark.negative
def test_rollback_rejects_invalid_other_slot(ota_connected_device):
  device = ota_connected_device
  original = read_firmware(device)
  device.ota.broken(wait=False)
  logs = log_text(device.wait_for_log('Rolling back', timeout=180))
  assert 'self-check FAILED' in logs, logs
  wait_boot(device)
  assert read_firmware(device) == original
  require_login(device)
  response = log_text(device.ota.rollback(timeout=15))
  assert 'E417' in response, response
  assert read_firmware(device) == original


@pytest.mark.tc('TC-OTA-035')
@pytest.mark.regression
@pytest.mark.negative
def test_concurrent_ota_rejected(ota_connected_device):
  if OTA_THROTTLED_TRANSFER != '1':
    pytest.skip('Requires throttled fw7 server to keep OTA active at the CLI probe')
  device = ota_connected_device
  original = read_firmware(device)
  first = device.ota.install(str(original[0]), force=True, until=('10%', '[OTA] success:', 'E4'))
  assert re.search(r'\[OTA\]\s+10%', log_text(first)), first
  device._connector.write_command('ota check')
  stream = log_text(device.wait_for_log('[OTA] success:', timeout=300))
  assert 'E401' in stream, stream
  wait_boot(device)
  assert read_firmware(device)[0] == original[0]
  assert read_firmware(device)[2].lower() == 'valid'


@pytest.mark.tc('TC-OTA-038')
@pytest.mark.regression
@pytest.mark.negative
def test_download_cannot_start(ota_connected_device):
  url = OTA_DOWNLOAD_START_FAILURE_URL
  if not url:
    pytest.skip('Configure OTA_DOWNLOAD_START_FAILURE_URL for a controlled E405 response')
  device = ota_connected_device
  before = read_firmware(device)
  result = log_text(device.ota.url(url, timeout=30))
  assert 'E405' in result, result
  assert read_firmware(device) == before
  response = device.ota.install(str(before[0]), force=True)
  ota_success(response, before[0], before[0])
  wait_boot(device)
  assert read_firmware(device)[0] == before[0]
