import pytest


@pytest.mark.tc('TC-LAMP-004')
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.parametrize('color', ('white', 'red', 'green', 'blue', 'yellow', 'purple', 'cyan', 'orange'))
def test_set_named_color(lamp_on_device, hil, color):
  response = lamp_on_device.lamp.set_color(color)
  status = lamp_on_device.lamp.status()
  assert all(0 <= component <= 255 for component in status.color), response
  # LM-2 does not specify the exact RGB triple used by each named color.
  hil.camera.photo.verify('rgb', name=f'named_{color}', expected_rgb=status.color)


@pytest.mark.tc('TC-LAMP-005')
@pytest.mark.regression
@pytest.mark.negative
def test_reject_unknown_named_color(lamp_on_device):
  before = lamp_on_device.lamp.status()
  response = '\n'.join(lamp_on_device.lamp.set_color('ultramarine'))
  assert 'E503' in response, response
  assert lamp_on_device.lamp.status().color == before.color
