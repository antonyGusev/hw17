from urllib.parse import urljoin

import pytest
from helpers import log_text, ota_success, wait_boot

from config import OTA_CORRUPTED_IMAGES
from lib import read_firmware


@pytest.mark.tc('TC-OTA-022')
@pytest.mark.regression
@pytest.mark.negative
def test_non_firmware_binary_rejected_and_retry(ota_connected_device, ota_server_url):
  device = ota_connected_device
  before = read_firmware(device)
  url = urljoin(ota_server_url, '../test/garbage.bin')
  result = log_text(device.ota.url(url))
  assert 'E406' in result, result
  assert read_firmware(device) == before
  response = device.ota.install(str(before[0]), force=True)
  ota_success(response, before[0], before[0])
  wait_boot(device)
  assert read_firmware(device)[0] == before[0]
  assert read_firmware(device)[2].lower() == 'valid'


@pytest.mark.tc('TC-OTA-027')
@pytest.mark.regression
@pytest.mark.negative
def test_corrupted_binary_rejected_and_retry(ota_connected_device):
  device = ota_connected_device
  before = read_firmware(device)
  url = OTA_CORRUPTED_IMAGES.get(str(before[0]))
  if not url:
    pytest.skip('Configure OTA_CORRUPTED_IMAGE_2_1_0 or OTA_CORRUPTED_IMAGE_2_3_0')
  result = log_text(device.ota.url(url))
  assert 'E412' in result, result
  assert read_firmware(device) == before
  response = device.ota.install(str(before[0]), force=True)
  ota_success(response, before[0], before[0])
  wait_boot(device)
  assert read_firmware(device)[0] == before[0]
  assert read_firmware(device)[2].lower() == 'valid'
