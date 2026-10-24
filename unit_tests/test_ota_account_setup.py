import importlib.util
from pathlib import Path

import pytest

from framework.device.controllers.auth_controller import AuthController
from framework.device.controllers.ota_controller import OtaController
from framework.device.controllers.wifi_controller import WifiStatus


spec = importlib.util.spec_from_file_location(
  'ota_helpers_for_unit_tests', Path(__file__).resolve().parents[1] / 'tests' / 'ota' / 'helpers.py'
)
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)


class FakeAuth:
  def __init__(self, stored=None):
    self.stored = stored
    self.logged_in = None
    self.registration_count = 0
    self.login_count = 0

  def whoami(self):
    if self.logged_in:
      return [f'user: {self.logged_in}, access: user']
    return ['not logged in']

  def register(self, username, password):
    self.registration_count += 1
    if self.stored is not None:
      return False
    self.stored = (username, password)
    return True

  def login(self, username, password):
    self.login_count += 1
    if self.stored != (username, password):
      return False
    self.logged_in = username
    return True


class FakeDevice:
  def __init__(self, stored=None):
    self.auth = FakeAuth(stored)
    self.buoy = type('Wifi', (), {
      'status': lambda self: WifiStatus(True, 'test-ap', '192.168.1.2', -42)
    })()

  def status(self):
    return [
      "I (1) sentry:   link: buoy link 'test-ap', ip 192.168.1.2, rssi -42 dBm",
      'I (2) sentry:   heap: 251 KB free',
    ]


def test_fixture_registers_once_then_logs_in_again_after_reboot():
  dut = FakeDevice()
  helpers.require_login(dut)
  assert dut.auth.stored == (helpers.OTA_TEST_LOGIN, helpers.OTA_TEST_PASSWORD)
  assert dut.auth.registration_count == 1
  dut.auth.logged_in = None  # firmware reboot invalidates session, not the account
  helpers.require_login(dut)
  assert dut.auth.registration_count == 1
  assert dut.auth.login_count == 2


def test_fixture_reuses_existing_suite_account():
  dut = FakeDevice((helpers.OTA_TEST_LOGIN, helpers.OTA_TEST_PASSWORD))
  helpers.require_login(dut)
  assert dut.auth.logged_in == helpers.OTA_TEST_LOGIN


def test_fixture_fails_if_an_unrelated_profile_is_in_nvs():
  dut = FakeDevice(('other_user', 'other_password'))
  with pytest.raises(AssertionError, match='different NVS profile or password'):
    helpers.require_login(dut)


class ConnectorStub:
  def __init__(self, response):
    self.response = response
    self.last_command = None
    self.until = None

  def execute_command(self, command, until=None, timeout=None):
    self.last_command = command
    self.until = until
    return self.response


def test_fw7_url_command_and_completion_marker():
  connector = ConnectorStub(['[OTA] success: v2.1.0 -> v2.3.0 in 4 s. Rebooting...'])
  OtaController(connector).url('https://example.test/fw7/sentry_fw7.bin', force=True)
  assert connector.last_command == 'ota url https://example.test/fw7/sentry_fw7.bin force'
  assert '[OTA] success:' in connector.until


def test_register_does_not_depend_on_legacy_profile_created_text():
  connector = ConnectorStub(['[AUTH] account saved'])
  assert AuthController(connector).register('ota_qa', 'OtaQa_2026')
  connector.response = ['E202 profile already exists']
  assert not AuthController(connector).register('ota_qa', 'OtaQa_2026')
