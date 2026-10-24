import lib
import lib.utilities as utilities
from lib.utilities import ota_helpers


def test_ota_helpers_are_exported_from_lib_and_utilities():
  names = (
    'BOOT_READY', 'VERSION_PATTERN',
    'OTA_TEST_LOGIN', 'OTA_TEST_PASSWORD', 'OTA_TEMP_PASSWORD',
    'log_text', 'ota_success', 'wait_boot', 'ensure_connection',
    'install_and_verify', 'restore_firmware', 'require_version',
    'require_login', 'check_versions',
  )
  for name in names:
    expected = getattr(ota_helpers, name)
    assert getattr(lib, name) is expected
    assert getattr(utilities, name) is expected
    assert name in lib.__all__
    assert name in utilities.__all__
