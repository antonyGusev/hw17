import serial
import pytest

import flash_device


class ConnectorStub:
  instances = []

  def __init__(self, port):
    self.port = port
    self.ser = None
    self.opens = 0
    self.closes = 0
    self.instances.append(self)

  def open(self):
    self.ser = type('SerialPortStub', (), {'is_open': True})()
    self.opens += 1

  def close(self):
    if self.ser is not None:
      self.ser.is_open = False
    self.ser = None
    self.closes += 1


class DeviceStub:
  responses = []

  def __init__(self, connector):
    self.connector = connector

  def help(self):
    value = self.responses.pop(0)
    if isinstance(value, Exception):
      raise value
    return value


def test_flash_readiness_uses_fw7_help_not_firmware_state(monkeypatch):
  ConnectorStub.instances.clear()
  DeviceStub.responses = [
    ['help'],
    ["I (123) sentry: Commands ([wifi] - needs Wi-Fi, [login] - needs Wi-Fi + login, [debug] - debug access):"],
  ]
  monkeypatch.setattr(flash_device, 'UARTConnector', ConnectorStub)
  monkeypatch.setattr(flash_device, 'DeviceDriver', DeviceStub)

  def poll(callback, **kwargs):
    assert not callback()
    assert callback()

  monkeypatch.setattr(flash_device, 'wait_for_condition', poll)
  flash_device.wait_for_device('COM4')
  connector = ConnectorStub.instances[0]
  assert connector.opens == 1
  assert connector.closes == 1


def test_flash_readiness_recovers_after_serial_failure(monkeypatch):
  ConnectorStub.instances.clear()
  DeviceStub.responses = [serial.SerialException('port temporarily unavailable'), ['I (123) sentry: Commands ([wifi] ...)']]
  monkeypatch.setattr(flash_device, 'UARTConnector', ConnectorStub)
  monkeypatch.setattr(flash_device, 'DeviceDriver', DeviceStub)

  def poll(callback, **kwargs):
    assert not callback()
    assert callback()

  monkeypatch.setattr(flash_device, 'wait_for_condition', poll)
  flash_device.wait_for_device('COM4')
  connector = ConnectorStub.instances[0]
  assert connector.opens == 2
  assert connector.closes == 2


def test_flash_readiness_fails_when_help_never_responds(monkeypatch):
  ConnectorStub.instances.clear()
  DeviceStub.responses = [['help']]
  monkeypatch.setattr(flash_device, 'UARTConnector', ConnectorStub)
  monkeypatch.setattr(flash_device, 'DeviceDriver', DeviceStub)

  def poll(callback, error_message, **kwargs):
    assert not callback()
    raise TimeoutError(error_message)

  monkeypatch.setattr(flash_device, 'wait_for_condition', poll)
  with pytest.raises(TimeoutError, match='not responding to help on COM4'):
    flash_device.wait_for_device('COM4')
  assert ConnectorStub.instances[0].closes == 1


def test_flash_keeps_original_power_cycle_fallback(monkeypatch, tmp_path):
  image = tmp_path / 'sentry_fw7_v2.1.0_merged.bin'
  image.write_bytes(b'mock firmware')
  monkeypatch.setattr(flash_device, 'FIRMWARE_PATH', image)
  monkeypatch.setattr(flash_device, 'HIL_PORT', 'COM5')
  monkeypatch.setattr(flash_device, 'UARTConnector', ConnectorStub)
  monkeypatch.setattr(flash_device, 'find_device_port', lambda: 'COM4')
  events = []

  class HilStub:
    def __init__(self, connector):
      pass

    def power_on(self):
      events.append('power_on')

    def power_cycle(self):
      events.append('power_cycle')

  class FlasherStub:
    def erase(self, port):
      events.append('erase')

    def flash(self, port, path):
      events.append('flash')

  def probe(port, timeout=15):
    events.append(('probe', timeout))
    if timeout == 15:
      raise TimeoutError('DUT not responding')

  monkeypatch.setattr(flash_device, 'HILDriver', HilStub)
  monkeypatch.setattr(flash_device, 'FirmwareFlasher', FlasherStub)
  monkeypatch.setattr(flash_device, 'wait_for_device', probe)
  flash_device.main()

  assert events == ['power_on', 'erase', 'flash', ('probe', 15), 'power_cycle', ('probe', 30)]
