import pytest


@pytest.mark.tc('TC-LAMP-027')
@pytest.mark.first
@pytest.mark.positive
def test_default_lamp_state_on_clean_device(ota_device, lamp_login):
  # Authenticate without applying lamp settings before reading factory values.
  lamp_login(ota_device)
  status = ota_device.lamp.status()
  assert not status.is_on
  assert 0 <= status.brightness <= 100
  assert all(0 <= component <= 255 for component in status.color)
  assert status.mode in ('solid', 'blink', 'breathe', 'rainbow')
