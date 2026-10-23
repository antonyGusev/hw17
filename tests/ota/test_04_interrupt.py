import re

import pytest
import serial

from lib import read_firmware, wait_for_condition
from helpers import log_text


@pytest.mark.tc('TC-OTA-021')
@pytest.mark.regression
@pytest.mark.negative
def test_power_cut_while_downloading(ota_connected_device, hil):
  device = ota_connected_device
  original, slot, state = read_firmware(device)
  assert state.lower() == 'valid'
  try:
    response = device.ota.install(
      str(original), force=True, until=('%', '[OTA] success:', 'E4'),
    )
    progress = re.search(r'\[OTA\]\s+(\d+)%', log_text(response))
    assert progress and int(progress.group(1)) < 100, response
    device.close()
    hil.power_cycle()

    def open_uart():
      try:
        device.open()
        return True
      except (serial.SerialException, OSError):
        return False

    wait_for_condition(open_uart, timeout=30, interval=0.5)
    # Power interruption of a download must not invalidate the active image.
    assert read_firmware(device) == (original, slot, 'valid')
  finally:
    if not device.is_open:
      device.open()
