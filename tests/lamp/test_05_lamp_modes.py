import pytest


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.parametrize('mode', [
  pytest.param('solid', marks=pytest.mark.tc('TC-LAMP-013')),
  pytest.param('blink', marks=pytest.mark.tc('TC-LAMP-014')),
  pytest.param('breathe', marks=pytest.mark.tc('TC-LAMP-015')),
  pytest.param('rainbow', marks=pytest.mark.tc('TC-LAMP-016')),
])
def test_set_supported_mode(lamp_on_device, hil, mode):
  lamp_on_device.lamp.set_color('yellow')
  lamp_on_device.lamp.set_brightness(50)
  response = lamp_on_device.lamp.set_mode(mode)
  assert lamp_on_device.lamp.status().mode == mode, response
  # Existing HIL video implementation is used unchanged.
  hil.camera.video.verify(mode)


@pytest.mark.tc('TC-LAMP-018')
@pytest.mark.regression
@pytest.mark.negative
def test_reject_unknown_mode(lamp_on_device):
  before = lamp_on_device.lamp.status().mode
  response = '\n'.join(lamp_on_device.lamp.set_mode('disco'))
  assert 'E505' in response, response
  assert lamp_on_device.lamp.status().mode == before
