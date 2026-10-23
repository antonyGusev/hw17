import pytest


@pytest.mark.tc('TC-LAMP-025')
@pytest.mark.smoke
@pytest.mark.positive
def test_lamp_status_contains_required_fields(lamp_on_device):
  raw = '\n'.join(lamp_on_device.lamp.status_raw()).lower()
  for field in ('color', 'brightness', 'mode', 'timer'):
    assert field in raw, raw
  status = lamp_on_device.lamp.status()
  assert status.lamp in ('on', 'off')
  assert len(status.color) == 3
  assert 0 <= status.brightness <= 100
  assert status.mode in ('solid', 'blink', 'breathe', 'rainbow')


@pytest.mark.tc('TC-LAMP-026')
@pytest.mark.regression
@pytest.mark.positive
def test_lamp_status_matches_configured_state(lamp_on_device):
  lamp_on_device.lamp.set_rgb(255, 0, 128)
  lamp_on_device.lamp.set_brightness(30)
  lamp_on_device.lamp.set_mode('solid')
  lamp_on_device.lamp.set_timer(30)
  status = lamp_on_device.lamp.status()
  assert status.is_on
  assert status.color == (255, 0, 128)
  assert status.brightness == 30
  assert status.mode == 'solid'
  assert 0 < status.timer_s <= 30
