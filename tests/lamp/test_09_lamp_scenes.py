import pytest


@pytest.mark.tc('TC-LAMP-031')
@pytest.mark.first
@pytest.mark.negative
def test_reject_loading_empty_scene(lamp_on_device):
  # Scene slots are persistent NVS data and may have been populated by prior runs.
  original = lamp_on_device.lamp.status()
  try:
    for scene in (1, 2, 3):
      before = lamp_on_device.lamp.status()
      response = '\n'.join(lamp_on_device.lamp.load_scene(scene))
      if 'E509' in response:
        assert lamp_on_device.lamp.status() == before
        return
      assert f'scene {scene} loaded' in response.lower(), response

    pytest.skip('All three NVS scene slots are populated; E509 requires an empty slot')
  finally:
    lamp_on_device.lamp.set_rgb(*original.color)
    lamp_on_device.lamp.set_brightness(original.brightness)
    lamp_on_device.lamp.set_mode(original.mode)


@pytest.mark.tc('TC-LAMP-029')
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.parametrize(('scene', 'rgb', 'brightness', 'mode'), [
  (1, (255, 0, 0), 25, 'solid'),
  (2, (0, 255, 0), 50, 'blink'),
  (3, (0, 0, 255), 75, 'breathe'),
])
def test_save_and_load_scene(lamp_on_device, scene, rgb, brightness, mode):
  lamp_on_device.lamp.set_rgb(*rgb)
  lamp_on_device.lamp.set_brightness(brightness)
  lamp_on_device.lamp.set_mode(mode)
  lamp_on_device.lamp.save_scene(scene)
  lamp_on_device.lamp.set_rgb(1, 2, 3)
  lamp_on_device.lamp.set_brightness(10)
  lamp_on_device.lamp.set_mode('solid')
  lamp_on_device.lamp.load_scene(scene)
  status = lamp_on_device.lamp.status()
  assert (status.color, status.brightness, status.mode) == (rgb, brightness, mode)


@pytest.mark.tc('TC-LAMP-032')
@pytest.mark.regression
@pytest.mark.positive
def test_scene_survives_reboot(lamp_on_device, lamp_login):
  expected_rgb = (160, 0, 255)
  lamp_on_device.lamp.set_rgb(*expected_rgb)
  lamp_on_device.lamp.set_brightness(42)
  lamp_on_device.lamp.set_mode('solid')
  lamp_on_device.lamp.save_scene(1)
  lamp_on_device.reboot()
  lamp_login(lamp_on_device)
  lamp_on_device.lamp.load_scene(1)
  status = lamp_on_device.lamp.status()
  assert (status.color, status.brightness, status.mode) == (expected_rgb, 42, 'solid')


@pytest.mark.tc('TC-LAMP-030')
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize('command', ('scene save 0', 'scene save 4', 'scene load 0', 'scene load 4'))
def test_reject_invalid_scene_number(lamp_on_device, command):
  before = lamp_on_device.lamp.status()
  response = '\n'.join(lamp_on_device.lamp.execute(command))
  assert 'E508' in response, response
  assert lamp_on_device.lamp.status() == before


@pytest.mark.tc('TC-LAMP-048')
@pytest.mark.regression
@pytest.mark.positive
def test_scene_survives_logout(lamp_on_device, lamp_login):
  lamp_on_device.lamp.set_rgb(24, 48, 72)
  lamp_on_device.lamp.set_brightness(38)
  lamp_on_device.lamp.set_mode('solid')
  lamp_on_device.lamp.save_scene(2)
  lamp_on_device._connector.execute_command('logout', until=('relieved from watch', 'W211', 'E003'), timeout=5)
  lamp_login(lamp_on_device)
  lamp_on_device.lamp.load_scene(2)
  status = lamp_on_device.lamp.status()
  assert (status.color, status.brightness, status.mode) == ((24, 48, 72), 38, 'solid')
