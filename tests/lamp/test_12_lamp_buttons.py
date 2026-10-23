import pytest


@pytest.mark.tc('TC-LAMP-041')
@pytest.mark.regression
@pytest.mark.positive
def test_k1_short_press_toggles_lamp(lamp_device, hil):
  assert not lamp_device.lamp.status().is_on
  hil.buttons.k1()
  assert lamp_device.lamp.status().is_on
  hil.buttons.k1()
  assert not lamp_device.lamp.status().is_on


@pytest.mark.tc('TC-LAMP-042')
@pytest.mark.regression
@pytest.mark.positive
def test_k1_long_hold_advances_color(lamp_on_device, hil):
  before = lamp_on_device.lamp.status().color
  response = hil.buttons.hold('k1', 1.7)
  assert any('[HIL] K1 release' in line for line in response), response
  after = lamp_on_device.lamp.status().color
  assert after != before, f'K1 1.7s hold did not change color: {before}'
  assert lamp_on_device.lamp.status().is_on
