import re

import pytest
from helpers import VERSION_PATTERN, log_text, wait_boot

from lib import read_firmware


@pytest.mark.tc('TC-OTA-001')
@pytest.mark.ota_gatekeeper
@pytest.mark.positive
def test_version_reports_firmware_partition_and_state(ota_device):
  response = log_text(ota_device.version())
  assert re.search(rf'{VERSION_PATTERN}\s*\(build\s+[^)]+\)', response), response
  assert re.search(r'partition:\s*ota_[01]\s*@\s*0x[0-9a-fA-F]+,\s*state:\s*valid', response), response


@pytest.mark.tc('TC-OTA-002')
@pytest.mark.regression
@pytest.mark.positive
def test_version_matches_boot_and_ota_status(ota_device):
  version, _, _ = read_firmware(ota_device)
  ota_status = log_text(ota_device.ota.status())
  assert str(version) in ota_status, ota_status

  # The PRD does not prescribe boot version line prefix; match its version token.
  ota_device.ota.execute('')  # Read current OTA info before reboot.
  ota_device._connector.write_command('reboot')
  boot_log = log_text(wait_boot(ota_device))
  assert re.search(rf'(?<!\d)v?{re.escape(str(version))}(?!\d)', boot_log), boot_log
  assert read_firmware(ota_device)[0] == version


@pytest.mark.tc('TC-OTA-028')
@pytest.mark.regression
@pytest.mark.positive
def test_ota_status_reports_current_and_previous_slot(ota_device):
  version, partition, _ = read_firmware(ota_device)
  for response in (ota_device.ota.execute(), ota_device.ota.status()):
    output = log_text(response)
    assert str(version) in output, output
    assert partition in output, output
    assert re.search(r'(previous|other|inactive)', output, re.IGNORECASE), output
