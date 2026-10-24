import pytest
from packaging.version import Version

from lib import check_versions, read_firmware, require_login, restore_firmware


@pytest.fixture(scope='session', autouse=True)
def ota_initial_firmware(ota_device, ota_server_url):
  # Keep one baseline for the entire OTA run, not the version left by a failed test.
  original, _, _ = read_firmware(ota_device)
  require_login(ota_device)
  ota_device.ota.server(ota_server_url)
  print(f'OTA firmware baseline: {original}')

  yield original

  restore_firmware(ota_device, original)


@pytest.fixture(autouse=True)
def ota_authorized(ota_device):
  # OTA commands require a logged-in user on fw_7 (observed E003 on ota check).
  # Function scope restores the session after reboot/OTA in previous tests.
  require_login(ota_device)


@pytest.fixture
def ota_connected_device(ota_device, ota_authorized, ota_initial_firmware):
  # Recover the session baseline if an earlier teardown left another version.
  current, _, _ = read_firmware(ota_device)
  if current != ota_initial_firmware:
    restore_firmware(ota_device, ota_initial_firmware)
    require_login(ota_device)

  try:
    yield ota_device
  finally:
    restore_firmware(ota_device, ota_initial_firmware)


@pytest.fixture
def ota_logged_in_device(ota_connected_device):
  return ota_connected_device


@pytest.fixture(scope='session')
def ota_versions(ota_device):
  # Session fixtures are initialized before function-scoped autouse fixtures.
  require_login(ota_device)
  versions = check_versions(ota_device.ota.check())
  assert versions['stable'] == Version('2.1.0'), versions
  assert versions['beta'] == Version('2.3.0'), versions
  return versions

