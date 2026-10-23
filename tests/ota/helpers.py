import re
import time

import pytest
from packaging.version import Version

from config import PASSWORD, SSID
from lib import DeviceTimeoutError, has_active_wifi_connection, read_firmware


VERSION_PATTERN = r'(?:SENTRY SWM-2 sonar watch module,\s*fw|FW:)\s*v?(\d+\.\d+\.\d+)'
BOOT_READY = 'ready. state'  # fw_7 CLI is ready only after OTA self-check has completed

# Dedicated lab account for fw_7: registered on the DUT at first use, then
# reused after reboot/OTA. No DEVICE_LOGIN/DEVICE_PASSWORD .env entries needed.
OTA_TEST_LOGIN = 'ota_qa'
OTA_TEST_PASSWORD = 'OtaQa_2026'
OTA_TEMP_PASSWORD = 'OtaQa_2026_tmp'


def log_text(lines):
  return '\n'.join(lines)


def ota_success(lines, source, target):
  output = log_text(lines)
  assert re.search(
    rf'\[OTA\] success:\s*v?{re.escape(str(source))}\s*->\s*'
    rf'v?{re.escape(str(target))}\s+in\s+\d+\s+s\. Rebooting\.\.\.', output,
  ), f'Incorrect OTA success message: {lines}'


def wait_boot(device):
  return device.wait_for_log(BOOT_READY, timeout=90)


def ensure_connection(device):
  if has_active_wifi_connection(device):
    return
  # Autoconnect is explicitly disabled in fw_7. Prefer saved credentials.
  result = device.wifi.reconnect()
  if result.connected:
    assert has_active_wifi_connection(device), (
      f'Reconnect reported success, but status shows buoy link down: {result.response}'
    )
    return

  assert SSID and PASSWORD, f'Wi-Fi reconnect failed, SSID/PASSWORD not configured: {result.response}'
  result = device.wifi.connect(SSID, PASSWORD)
  assert result.connected and has_active_wifi_connection(device), (
    f'Wi-Fi connect failed: {result.response}'
  )


def install_and_verify(device, target, force=False):
  source, partition, state = read_firmware(device)
  assert state.lower() == 'valid'
  require_login(device)
  response = device.ota.install(str(target), force=force)
  ota_success(response, source, target)
  wait_boot(device)
  version, slot, state = read_firmware(device)
  assert version == target
  assert slot != partition
  assert state.lower() == 'valid'
  return response


def restore_firmware(device, original):
  # A failed test can leave the DUT rebooting. Retry the version query instead
  # of treating boot/OTA log fragments as a completed CLI response.
  for attempt in range(3):
    try:
      version, _, _ = read_firmware(device)
      break
    except (AssertionError, DeviceTimeoutError):
      if attempt == 2:
        raise
      time.sleep(1)

  if version != original:
    print(f'OTA firmware restore: {version} -> {original}')
    install_and_verify(device, original, force=True)
    print(f'OTA firmware restored: {original}')


def require_version(device, desired):
  version, _, _ = read_firmware(device)
  if version != desired:
    pytest.skip(f'Requires firmware {desired}; DUT has {version}. No implicit setup flash.')


def require_login(device):
  ensure_connection(device)
  who = log_text(device.auth.whoami())
  account = re.search(r'user:\s*([A-Za-z0-9_]+)\s*,\s*access:', who, re.I)
  if account and account.group(1) == OTA_TEST_LOGIN:
    return

  if account:
    # A dedicated OTA test DUT may retain a session from a previous scenario.
    device._connector.execute_command('logout')

  if not getattr(device, '_ota_test_account_prepared', False):
    # AU-1 allows only one NVS profile. E202 is expected on repeat runs;
    # successful login with our credentials proves the profile is ours.
    device.auth.register(OTA_TEST_LOGIN, OTA_TEST_PASSWORD)

  device.auth.login(OTA_TEST_LOGIN, OTA_TEST_PASSWORD)
  who = log_text(device.auth.whoami())
  assert re.search(
    rf'user:\s*{re.escape(OTA_TEST_LOGIN)}\s*,\s*access:', who, re.I
  ), (
    'OTA test account is not logged in. The DUT may have a different NVS '
    'profile or password (AU-1): verify the existing credentials or use '
    f'a clean test DUT. whoami={who!r}'
  )
  device._ota_test_account_prepared = True


def check_versions(lines):
  output = log_text(lines)
  versions = {}
  for label in ('current', 'stable', 'beta'):
    match = re.search(
      rf'\[OTA\]\s*{label}(?:\s+(?:version|channel))?\s*:\s*v?(\d+\.\d+\.\d+)',
      output, re.I,
    )
    assert match, f'{label} version missing in OTA check: {lines}'
    versions[label] = Version(match.group(1))
  return versions
