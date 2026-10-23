import re

import pytest

from lib import read_firmware
from helpers import (
  OTA_TEST_LOGIN, OTA_TEST_PASSWORD, OTA_TEMP_PASSWORD,
  ensure_connection, install_and_verify, log_text, require_login, restore_firmware, wait_boot,
)


def command(device, cmd):
  return log_text(device._connector.execute_command(cmd))


@pytest.mark.tc('TC-OTA-042')
@pytest.mark.regression
@pytest.mark.positive
def test_changed_password_persists_upgrade_downgrade_rollback(ota_connected_device, ota_versions):
  new_password = OTA_TEMP_PASSWORD
  original_password = OTA_TEST_PASSWORD
  login = OTA_TEST_LOGIN
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  stable, beta = ota_versions['stable'], ota_versions['beta']
  if original != stable:
    pytest.skip('Requires initial 2.1.0 for up/down/rollback validation')
  changed = False

  def login_new_and_reject_old(check_old=False):
    ensure_connection(device)
    device.auth.login(login, new_password)
    assert re.search(rf'user:\s*{re.escape(login)}\b', log_text(device.auth.whoami()))
    if check_old:
      command(device, 'logout')
      assert 'E209' in command(device, f'login {login} {original_password}')
      device.auth.login(login, new_password)
      assert re.search(rf'user:\s*{re.escape(login)}\b', log_text(device.auth.whoami()))

  try:
    assert 'E215' not in command(device, f'passwd {original_password} {new_password}')
    changed = True
    install_and_verify(device, beta)
    login_new_and_reject_old(check_old=True)
    install_and_verify(device, stable, force=True)
    login_new_and_reject_old()
    ensure_connection(device)
    response = device.ota.rollback()
    assert 'E416' not in log_text(response) and 'E417' not in log_text(response)
    wait_boot(device)
    assert read_firmware(device)[0] == beta
    login_new_and_reject_old()
  finally:
    if changed:
      ensure_connection(device)
      device.auth.login(login, new_password)
      assert 'E215' not in command(device, f'passwd {new_password} {original_password}')
    restore_firmware(device, original)


@pytest.mark.tc('TC-OTA-043')
@pytest.mark.regression
@pytest.mark.positive
def test_relay_auto_and_cycles_persist_upgrade(ota_connected_device, ota_versions):
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  if original != ota_versions['stable']:
    pytest.skip('Requires initial 2.1.0 upgrade')
  previous = command(device, 'relay status')
  saved_mode = re.search(r'auto\s*:?\s*(on|off)', previous, re.I)
  saved_count = re.search(r'cycles\s+(\d+)', previous, re.I)
  assert saved_mode and saved_count, previous
  try:
    command(device, 'relay auto on')
    before = command(device, 'relay status')
    counter = re.search(r'cycles\s+(\d+)', before, re.I)
    assert counter, before
    install_and_verify(device, ota_versions['beta'])
    require_login(device)
    after = command(device, 'relay status')
    assert re.search(r'auto\s*:?\s*on\b', after, re.I), after
    assert re.search(rf'cycles\s+{counter.group(1)}\b', after, re.I), after
  finally:
    restore_firmware(device, original)
    require_login(device)
    command(device, f'relay auto {saved_mode.group(1).lower()}')


@pytest.mark.tc('TC-OTA-045')
@pytest.mark.regression
@pytest.mark.positive
def test_health_configuration_persists_upgrade(ota_connected_device, ota_versions):
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  if original != ota_versions['stable']:
    pytest.skip('Requires initial 2.1.0 upgrade')
  previous = command(device, 'health')
  interval = re.search(r'interval\s*:?\s*(\d+)', previous, re.I)
  enabled = re.search(r'(?:enabled|health)\s*:?\s*(on|off)', previous, re.I)
  assert interval and enabled, previous
  try:
    command(device, 'health interval 42')
    command(device, 'health off')
    install_and_verify(device, ota_versions['beta'])
    require_login(device)
    status = command(device, 'health')
    assert re.search(r'interval\s*:?\s*42\b', status, re.I), status
    assert re.search(r'(?:enabled|health)\s*:?\s*off\b', status, re.I), status
  finally:
    restore_firmware(device, original)
    require_login(device)
    command(device, f'health interval {interval.group(1)}')
    command(device, f'health {enabled.group(1).lower()}')
