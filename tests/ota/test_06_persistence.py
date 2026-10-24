import pytest
from helpers import ensure_connection, install_and_verify, require_login, restore_firmware

from config import SSID
from lib import read_firmware


@pytest.mark.tc('TC-OTA-015')
@pytest.mark.regression
@pytest.mark.positive
def test_wifi_and_lamp_persist_upgrade(ota_connected_device, ota_versions):
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  target = ota_versions['beta']
  if original >= target:
    pytest.skip('Requires 2.1.0 -> 2.3.0 upgrade')
  previous = device.lamp.status()
  try:
    device.lamp.set_rgb(12, 34, 56)
    device.lamp.set_brightness(37)
    device.lamp.set_mode('breathe')
    install_and_verify(device, target)
    ensure_connection(device)  # fw_7 does not autoconnect at boot.
    assert device.buoy.status().ssid == SSID
    require_login(device)
    current = device.lamp.status()
    assert not current.is_on, 'Lamp must be OFF after reboot (LM-1)'
    assert (current.color, current.brightness, current.mode) == ((12, 34, 56), 37, 'breathe')
  finally:
    restore_firmware(device, original)
    require_login(device)
    device.lamp.set_rgb(*previous.color)
    device.lamp.set_brightness(previous.brightness)
    device.lamp.set_mode(previous.mode)
    device.lamp.on() if previous.is_on else device.lamp.off()


@pytest.mark.tc('TC-OTA-016')
@pytest.mark.regression
@pytest.mark.positive
def test_scenes_persist_upgrade(ota_connected_device, ota_versions):
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  target = ota_versions['beta']
  if original >= target:
    pytest.skip('Requires 2.1.0 -> 2.3.0 upgrade')
  previous = device.lamp.status()
  scenes = ((1, (255, 0, 0), 25, 'solid'),
            (2, (0, 255, 0), 50, 'blink'),
            (3, (0, 0, 255), 75, 'breathe'))
  try:
    for slot, rgb, brightness, mode in scenes:
      device.lamp.set_rgb(*rgb)
      device.lamp.set_brightness(brightness)
      device.lamp.set_mode(mode)
      device.lamp.save_scene(slot)
    install_and_verify(device, target)
    require_login(device)
    for slot, rgb, brightness, mode in scenes:
      device.lamp.load_scene(slot)
      status = device.lamp.status()
      assert (status.color, status.brightness, status.mode) == (rgb, brightness, mode)
  finally:
    restore_firmware(device, original)
    require_login(device)
    device.lamp.set_rgb(*previous.color)
    device.lamp.set_brightness(previous.brightness)
    device.lamp.set_mode(previous.mode)
    device.lamp.on() if previous.is_on else device.lamp.off()


@pytest.mark.tc('TC-OTA-017')
@pytest.mark.regression
@pytest.mark.positive
def test_lamp_settings_persist_forced_downgrade(ota_connected_device, ota_versions):
  device = ota_connected_device
  original, _, _ = read_firmware(device)
  if original != ota_versions['beta']:
    pytest.skip('Requires initial 2.3.0 for forced downgrade')
  previous = device.lamp.status()
  try:
    device.lamp.set_rgb(12, 34, 56)
    device.lamp.set_brightness(37)
    device.lamp.set_mode('breathe')
    install_and_verify(device, ota_versions['stable'], force=True)
    require_login(device)
    status = device.lamp.status()
    assert (status.color, status.brightness, status.mode) == ((12, 34, 56), 37, 'breathe')
    assert device.buoy.status().ssid == SSID
  finally:
    restore_firmware(device, original)
    require_login(device)
    device.lamp.set_rgb(*previous.color)
    device.lamp.set_brightness(previous.brightness)
    device.lamp.set_mode(previous.mode)
    device.lamp.on() if previous.is_on else device.lamp.off()
