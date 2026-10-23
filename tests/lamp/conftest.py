import re

import pytest

from config import PASSWORD, SSID
from lib import has_active_wifi_connection

# Shared NVS test account; the fw_7 DUT supports only one account.
LAMP_LOGIN = 'ota_qa'
LAMP_PASSWORD = 'OtaQa_2026'


def ensure_lamp_login(device):
  if not has_active_wifi_connection(device):
    device.wifi.reconnect()
    if not has_active_wifi_connection(device):
      assert SSID and PASSWORD, 'Wi-Fi is disconnected and SSID/PASSWORD are not configured'
      device.wifi.connect(SSID, PASSWORD)
      assert has_active_wifi_connection(device), 'Cannot establish Wi-Fi before lamp login'

  who = '\n'.join(device.auth.whoami())
  expected = rf'user:\s*{re.escape(LAMP_LOGIN)}\s*,\s*access:'
  if re.search(expected, who, re.I):
    return

  account = re.search(r'user:\s*([A-Za-z0-9_]+)\s*,\s*access:', who, re.I)
  if account:
    device._connector.execute_command('logout')

  if not getattr(device, '_lamp_account_prepared', False):
    # AU-1: E202 is expected if the NVS profile already exists.
    device.auth.register(LAMP_LOGIN, LAMP_PASSWORD)
    device._lamp_account_prepared = True

  login_ok = device.auth.login(LAMP_LOGIN, LAMP_PASSWORD)
  who = '\n'.join(device.auth.whoami())
  assert re.search(expected, who, re.I), (
    f'Lamp account is not logged in; login_ok={login_ok}; whoami={who!r}. '
    'Verify the saved NVS account credentials.'
  )


@pytest.fixture
def lamp_login():
  return ensure_lamp_login


@pytest.fixture
def lamp_device(ota_device):
  ensure_lamp_login(ota_device)
  status = ota_device.lamp.status()
  if status.is_on:
    if status.timer_s:
      ota_device.lamp.set_timer(0)
    ota_device.lamp.off()

  try:
    yield ota_device
  finally:
    ensure_lamp_login(ota_device)
    status = ota_device.lamp.status()
    if status.is_on:
      if status.timer_s:
        ota_device.lamp.set_timer(0)
      ota_device.lamp.off()


@pytest.fixture
def lamp_on_device(lamp_device):
  lamp_device.lamp.on()
  lamp_device.lamp.set_color('white')
  lamp_device.lamp.set_brightness(50)
  lamp_device.lamp.set_mode('solid')
  yield lamp_device
