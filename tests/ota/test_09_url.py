import pytest
from packaging.version import Version

from config import OTA_HTTPS_URL, OTA_HTTPS_VERSION, OTA_VALID_IMAGE_URLS
from lib import log_text, ota_success, read_firmware, wait_boot


@pytest.mark.tc('TC-OTA-023')
@pytest.mark.regression
@pytest.mark.positive
def test_ota_install_from_https_url(ota_connected_device):
  if not OTA_HTTPS_URL or not OTA_HTTPS_VERSION:
    pytest.skip('Configure OTA_HTTPS_URL and OTA_HTTPS_VERSION')

  device = ota_connected_device
  original, slot, state = read_firmware(device)
  target = Version(OTA_HTTPS_VERSION)
  assert state.lower() == 'valid'

  if target <= original:
    pytest.skip(f'Requires HTTPS target newer than {original}, got {target}')

  response = device.ota.url(OTA_HTTPS_URL)
  ota_success(response, original, target)
  wait_boot(device)
  version, partition, state = read_firmware(device)
  assert version == target
  assert partition != slot
  assert state.lower() == 'valid'


@pytest.mark.tc('TC-OTA-048')
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize('url', ['ftp://host/file.bin', 'file:///firmware.bin'])
def test_reject_unsupported_url_scheme(ota_connected_device, url):
  device = ota_connected_device
  before = read_firmware(device)
  response = log_text(device.ota.url(url, timeout=10))
  assert 'E418' in response, response
  assert read_firmware(device) == before


@pytest.mark.tc('TC-OTA-049')
@pytest.mark.regression
@pytest.mark.positive
def test_forced_same_version_url(ota_connected_device):
  device = ota_connected_device
  original, _, _ = read_firmware(device)

  url = OTA_VALID_IMAGE_URLS.get(str(original))
  if not url:
    pytest.skip(f'Configure OTA_VALID_IMAGE_URL_{str(original).replace(".", "_")}')

  response = device.ota.url(url, force=True)
  assert 'W409' in log_text(response), response

  ota_success(response, original, original)
  wait_boot(device)

  assert read_firmware(device)[0] == original
  assert read_firmware(device)[2].lower() == 'valid'
