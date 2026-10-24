import pytest


@pytest.mark.tc('TC-LAMP-001')
@pytest.mark.smoke
@pytest.mark.positive
def test_lamp_on(lamp_device, hil):
  lamp_device.lamp.set_color('white')
  response = lamp_device.lamp.on()
  status = lamp_device.lamp.status()
  assert status.is_on, response
  hil.camera.photo.verify('rgb', name='lamp_on_white', expected_rgb=status.color)


@pytest.mark.tc('TC-LAMP-002')
@pytest.mark.smoke
@pytest.mark.positive
def test_lamp_off(lamp_on_device):
  response = lamp_on_device.lamp.off()
  assert not lamp_on_device.lamp.status().is_on, response
  # LM-8: after lamp off the RGB LED indicates system state, not fixed red.


@pytest.mark.tc('TC-LAMP-003')
@pytest.mark.regression
@pytest.mark.positive
def test_lamp_is_off_after_reboot(lamp_on_device, lamp_login):
  saved = lamp_on_device.lamp.status()
  lamp_on_device.reboot()
  # fw_7 does not reconnect automatically after reboot.
  lamp_on_device.buoy.reconnect()
  lamp_login(lamp_on_device)
  status = lamp_on_device.lamp.status()
  assert not status.is_on
  assert status.color == saved.color
  assert status.brightness == saved.brightness
  assert status.mode == saved.mode


@pytest.mark.tc('TC-LAMP-037')
@pytest.mark.regression
@pytest.mark.positive
def test_lamp_toggle(lamp_device):
  lamp_device.lamp.toggle()
  assert lamp_device.lamp.status().is_on
  lamp_device.lamp.toggle()
  assert not lamp_device.lamp.status().is_on


@pytest.mark.tc('TC-LAMP-038')
@pytest.mark.regression
@pytest.mark.negative
def test_repeated_power_commands_warn(lamp_device):
  off = '\n'.join(lamp_device.lamp.off())
  assert 'W510' in off, off
  lamp_device.lamp.on()
  on = '\n'.join(lamp_device.lamp.on())
  assert 'W510' in on, on
  assert lamp_device.lamp.status().is_on


@pytest.mark.tc('TC-LAMP-039')
@pytest.mark.regression
@pytest.mark.positive
def test_logout_turns_lamp_off(lamp_on_device, lamp_login):
  saved = lamp_on_device.lamp.status()
  lamp_on_device._connector.execute_command('logout', until=('relieved from watch', 'W211', 'E003'), timeout=5)
  lamp_login(lamp_on_device)
  status = lamp_on_device.lamp.status()
  assert not status.is_on
  assert (status.color, status.brightness, status.mode) == (saved.color, saved.brightness, saved.mode)


@pytest.mark.tc('TC-LAMP-040')
@pytest.mark.regression
@pytest.mark.negative
def test_power_commands_require_login(lamp_device, lamp_login):
  before = lamp_device.lamp.status()
  lamp_device._connector.execute_command('logout', until=('relieved from watch', 'W211', 'E003'), timeout=5)
  try:
    for command in ('on', 'off', 'toggle'):
      result = '\n'.join(lamp_device.lamp.execute(command))
      assert 'E003' in result, result
  finally:
    lamp_login(lamp_device)
  assert lamp_device.lamp.status() == before
