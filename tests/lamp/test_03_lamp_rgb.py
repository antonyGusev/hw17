import pytest

from test_data import RGB_COLORS


@pytest.mark.tc('TC-LAMP-006')
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize(('color', 'rgb'), RGB_COLORS.items())
def test_set_rgb_color(lamp_on_device, hil, color, rgb):
  lamp_on_device.lamp.set_rgb(*rgb)
  assert lamp_on_device.lamp.status().color == rgb
  hil.camera.photo.verify('rgb', name=color, expected_rgb=rgb)


@pytest.mark.tc('TC-LAMP-007')
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize('rgb', ((0, 0, 0), (255, 255, 255)))
def test_set_rgb_boundary_values(lamp_on_device, hil, rgb):
  lamp_on_device.lamp.set_rgb(*rgb)
  assert lamp_on_device.lamp.status().color == rgb
  # Black is a valid saved RGB value, not a guarantee that system LED is dark.
  if rgb != (0, 0, 0):
    hil.camera.photo.verify('rgb', name='rgb_max', expected_rgb=rgb)


@pytest.mark.tc('TC-LAMP-008')
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize('rgb', ((-1,0,0),(256,0,0),(0,-1,0),(0,256,0),(0,0,-1),(0,0,256)))
def test_reject_rgb_values_outside_range(lamp_on_device, rgb):
  before = lamp_on_device.lamp.status().color
  response = '\n'.join(lamp_on_device.lamp.set_rgb(*rgb))
  assert 'E502' in response, response
  assert lamp_on_device.lamp.status().color == before
