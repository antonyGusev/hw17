import time

import pytest


@pytest.mark.tc('TC-LAMP-019')
@pytest.mark.regression
@pytest.mark.positive
def test_timer_expires_and_turns_lamp_off(lamp_on_device):
  response = '\n'.join(lamp_on_device.lamp.set_timer(2))
  assert '[BEACON] auto-off in 2 s' in response, response
  assert lamp_on_device.lamp.status().timer_s <= 2
  time.sleep(2.2)
  assert not lamp_on_device.lamp.status().is_on


@pytest.mark.tc('TC-LAMP-020')
@pytest.mark.regression
@pytest.mark.positive
def test_cancel_active_timer(lamp_on_device, hil):
  lamp_on_device.lamp.set_color('yellow')
  lamp_on_device.lamp.set_timer(3)
  lamp_on_device.lamp.set_timer(0)
  assert lamp_on_device.lamp.status().timer_s == 0
  hil.camera.video.verify('stable_color', name='cancelled_timer')
  assert lamp_on_device.lamp.status().is_on


@pytest.mark.tc('TC-LAMP-021')
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize('seconds', (1, 3600))
def test_timer_accepts_boundary_values(lamp_on_device, seconds):
  response = '\n'.join(lamp_on_device.lamp.set_timer(seconds))
  assert f'[BEACON] auto-off in {seconds} s' in response, response
  assert 0 <= lamp_on_device.lamp.status().timer_s <= seconds
  lamp_on_device.lamp.set_timer(0)
  assert lamp_on_device.lamp.status().timer_s == 0


@pytest.mark.tc('TC-LAMP-024')
@pytest.mark.regression
@pytest.mark.positive
def test_timer_reboot_turns_lamp_off(lamp_on_device, lamp_login):
  before = lamp_on_device.lamp.status()
  lamp_on_device.lamp.set_timer(30)
  lamp_on_device.reboot()
  lamp_login(lamp_on_device)
  after = lamp_on_device.lamp.status()
  assert not after.is_on
  assert (after.color, after.brightness, after.mode) == (before.color, before.brightness, before.mode)


@pytest.mark.tc('TC-LAMP-022')
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize('seconds', (-1, 3601))
def test_reject_invalid_timer(lamp_on_device, seconds):
  lamp_on_device.lamp.set_timer(0)
  response = '\n'.join(lamp_on_device.lamp.set_timer(seconds))
  assert 'E506' in response, response
  assert lamp_on_device.lamp.status().timer_s == 0


@pytest.mark.tc('TC-LAMP-023')
@pytest.mark.regression
@pytest.mark.negative
def test_reject_timer_when_lamp_is_off(lamp_device):
  response = '\n'.join(lamp_device.lamp.set_timer(5))
  assert 'E507' in response, response
  assert not lamp_device.lamp.status().is_on
