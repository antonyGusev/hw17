import pytest


@pytest.mark.tc('TC-LAMP-009')
@pytest.mark.smoke
@pytest.mark.positive
def test_set_brightness(lamp_on_device, hil):
  lamp_on_device.lamp.set_color('white')
  lamp_on_device.lamp.set_mode('solid')
  values = {}
  for brightness in (0, 10, 50, 100):
    lamp_on_device.lamp.set_brightness(brightness)
    assert lamp_on_device.lamp.status().brightness == brightness
    if brightness:
      values[brightness] = hil.camera.photo.measure('brightness')
  hil.camera.photo.verify('brightness', name='brightness_levels', brightness_levels=values)


@pytest.mark.tc('TC-LAMP-010')
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize('brightness', (0, 100))
def test_brightness_boundaries(lamp_on_device, brightness):
  lamp_on_device.lamp.set_brightness(brightness)
  assert lamp_on_device.lamp.status().brightness == brightness


@pytest.mark.tc('TC-LAMP-012')
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize(('mode', 'duration'), [('solid', 2.0), ('blink', 3.0), ('breathe', 7.0), ('rainbow', 6.0)])
def test_brightness_applies_in_all_modes(lamp_on_device, hil, mode, duration):
  lamp_on_device.lamp.set_color('white')
  lamp_on_device.lamp.set_mode(mode)
  levels = []
  for brightness in (30, 70):
    lamp_on_device.lamp.set_brightness(brightness)
    assert lamp_on_device.lamp.status().brightness == brightness
    level = (hil.camera.photo.measure('brightness') if mode == 'solid'
             else hil.camera.video.measure('max_brightness', duration))
    levels.append(level)
  assert levels[1] > levels[0], f'{mode}: 30%={levels[0]:.2f}, 70%={levels[1]:.2f}'


@pytest.mark.tc('TC-LAMP-011')
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize('brightness', (-1, 101))
def test_reject_brightness_outside_range(lamp_on_device, brightness):
  before = lamp_on_device.lamp.status().brightness
  response = '\n'.join(lamp_on_device.lamp.set_brightness(brightness))
  assert 'E504' in response, response
  assert lamp_on_device.lamp.status().brightness == before
