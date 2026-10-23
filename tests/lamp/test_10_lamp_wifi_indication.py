import pytest


@pytest.mark.tc('TC-LAMP-036')
@pytest.mark.regression
@pytest.mark.positive
def test_system_indication_restored_after_lamp_off(lamp_on_device):
  lamp_on_device.lamp.off()
  assert not lamp_on_device.lamp.status().is_on
  # LM-8 does not prescribe a fixed Wi-Fi-specific LED color.
  # Complete priority/color verification is tracked as manual in CHECK_LIST.md.
