import pytest

from config import OTA_MISSING_CHANNEL_SERVER, OTA_OTHER_PROJECT_IMAGE_URL

from lib import read_firmware
from helpers import log_text


@pytest.mark.tc('TC-OTA-036')
@pytest.mark.regression
@pytest.mark.negative
def test_unreachable_custom_server(ota_connected_device):
  device = ota_connected_device
  before = read_firmware(device)
  try:
    device.ota.server('http://127.0.0.1:1/fw7/')
    result = log_text(device.ota.check())
    assert 'E402' in result, result
    assert read_firmware(device) == before
  finally:
    device.ota.server('default')


@pytest.mark.tc('TC-OTA-037')
@pytest.mark.regression
@pytest.mark.negative
def test_missing_channel_metadata(ota_connected_device):
  server = OTA_MISSING_CHANNEL_SERVER
  if not server:
    pytest.skip('Provide OTA_MISSING_CHANNEL_SERVER serving firmware but missing channel txt')
  device = ota_connected_device
  before = read_firmware(device)
  try:
    device.ota.server(server)
    result = log_text(device.ota.check())
    assert 'E403' in result, result
    assert read_firmware(device) == before
  finally:
    device.ota.server('default')


@pytest.mark.tc('TC-OTA-039')
@pytest.mark.regression
@pytest.mark.negative
def test_reject_other_project_image(ota_connected_device):
  url = OTA_OTHER_PROJECT_IMAGE_URL
  if not url:
    pytest.skip('Configure OTA_OTHER_PROJECT_IMAGE_URL')
  device = ota_connected_device
  before = read_firmware(device)
  response = log_text(device.ota.url(url))
  assert 'E407' in response, response
  assert read_firmware(device) == before
