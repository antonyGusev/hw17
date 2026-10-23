import re

import pytest
from helpers import install_and_verify, log_text, require_login, restore_firmware

from config import OTA_GUARD_CURRENT_PIN, OTA_GUARD_TEST_PIN
from lib import read_firmware


def guard(device, subcommand):
  return log_text(device._connector.execute_command(f'guard {subcommand}'))


@pytest.mark.tc('TC-OTA-046')
@pytest.mark.regression
@pytest.mark.positive
def test_guard_pin_and_zone_survive_downgrade(ota_connected_device, ota_versions):
  old_pin = OTA_GUARD_CURRENT_PIN
  new_pin = OTA_GUARD_TEST_PIN
  if not old_pin or not new_pin or not re.fullmatch(r'\d{4}', old_pin) or not re.fullmatch(r'\d{4}', new_pin):
    pytest.skip('Provide OTA_GUARD_CURRENT_PIN and OTA_GUARD_TEST_PIN (four digits each)')
  assert old_pin != new_pin
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  if original != ota_versions['beta']:
    pytest.skip('Requires 2.3.0 initially; Guard is unavailable in 2.1.0')
  status = guard(device, 'status')
  zone_match = re.search(r'zone\s*:?\s*(\d+)\s*cm', status, re.I)
  assert zone_match and re.search(r'DISARMED', status, re.I), status
  original_zone = int(zone_match.group(1))
  pin_changed = False
  try:
    result = guard(device, f'pin {old_pin} {new_pin}')
    assert not re.search(r'\bE8\d{2}\b', result), result
    pin_changed = True
    assert not re.search(r'\bE8\d{2}\b', guard(device, 'zone 88'))
    install_and_verify(device, ota_versions['stable'], force=True)
    install_and_verify(device, ota_versions['beta'])
    require_login(device)
    after = guard(device, 'status')
    assert re.search(r'zone\s*:?\s*88\s*cm', after, re.I), after
    assert not re.search(r'\bE8\d{2}\b', guard(device, 'arm'))
    response = guard(device, f'disarm {new_pin}')
    assert not re.search(r'\bE8\d{2}\b', response), response
    assert 'DISARMED' in guard(device, 'status').upper()
  finally:
    restore_firmware(device, original)
    require_login(device)
    if pin_changed:
      # Recover from armed/alarm state before restoring persistent Guard settings.
      guard(device, f'disarm {new_pin}')
      guard(device, f'pin {new_pin} {old_pin}')
    guard(device, f'zone {original_zone}')
