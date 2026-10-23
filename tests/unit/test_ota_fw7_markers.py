import importlib.util
from pathlib import Path

from packaging.version import Version

from framework.device import DeviceDriver
from framework.device.controllers.lamp_controller import LampController


spec = importlib.util.spec_from_file_location(
  'fw7_ota_helpers_markers', Path(__file__).resolve().parents[1] / 'ota' / 'helpers.py'
)
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)


class ConnectorStub:
  def __init__(self):
    self.calls = []

  def write_command(self, command):
    self.calls.append(('write', command))

  def wait_for_response(self, pattern, timeout):
    self.calls.append(('wait', pattern, timeout))
    return ["I (713) sentry: ready. state 1 NORMAL (patrol). Type 'help'"]

  def execute_command(self, command, until=None, timeout=None):
    self.calls.append(('execute', command, until, timeout))
    return ['W (9693) sentry: W510 lamp already off']


def test_wait_boot_uses_complete_ready_marker():
  connector = ConnectorStub()
  device = DeviceDriver(connector)
  helpers.wait_boot(device)
  assert connector.calls == [('wait', 'ready. state', 90)]


def test_reboot_waits_for_ready_after_self_check():
  connector = ConnectorStub()
  DeviceDriver(connector).reboot()
  assert connector.calls == [('write', 'reboot'), ('wait', 'ready. state', 90)]


def test_lamp_off_accepts_already_off_warning():
  connector = ConnectorStub()
  LampController(connector).off()
  assert 'W510' in connector.calls[0][2]


def test_restore_firmware_retries_incomplete_reboot_output(monkeypatch):
  responses = iter([AssertionError('Incomplete boot'), (Version('2.1.0'), 'ota_0', 'valid')])
  calls = []

  def read_firmware(device):
    calls.append(device)
    result = next(responses)
    if isinstance(result, Exception):
      raise result
    return result

  monkeypatch.setattr(helpers, 'read_firmware', read_firmware)
  monkeypatch.setattr(helpers.time, 'sleep', lambda seconds: None)
  device = object()
  helpers.restore_firmware(device, Version('2.1.0'))
  assert calls == [device, device]
