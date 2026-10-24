import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest
from packaging.version import Version


def load_ota_fixtures(monkeypatch):
  path = Path(__file__).resolve().parents[1] / 'tests' / 'ota'
  spec = importlib.util.spec_from_file_location('ota_baseline_fixtures', path / 'conftest.py')
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


def test_ota_fixture_restores_session_baseline_after_upgrade(monkeypatch):
  fixtures = load_ota_fixtures(monkeypatch)
  device = SimpleNamespace(version=Version('2.1.0'))
  restored = []
  monkeypatch.setattr(fixtures, 'read_firmware', lambda dut: (dut.version, 'ota_0', 'valid'))

  def restore(dut, target):
    restored.append((dut.version, target))
    dut.version = target

  monkeypatch.setattr(fixtures, 'restore_firmware', restore)
  generator = fixtures.ota_connected_device.__wrapped__(device, True, Version('2.1.0'))
  assert next(generator) is device
  device.version = Version('2.3.0')
  with pytest.raises(StopIteration):
    next(generator)
  assert restored == [(Version('2.3.0'), Version('2.1.0'))]
  assert device.version == Version('2.1.0')


def test_ota_fixture_recovers_a_version_left_by_previous_test(monkeypatch):
  fixtures = load_ota_fixtures(monkeypatch)
  device = SimpleNamespace(version=Version('2.3.0'))
  restored = []
  logged_in = []
  monkeypatch.setattr(fixtures, 'read_firmware', lambda dut: (dut.version, 'ota_0', 'valid'))

  def restore(dut, target):
    restored.append((dut.version, target))
    dut.version = target

  monkeypatch.setattr(fixtures, 'restore_firmware', restore)
  monkeypatch.setattr(fixtures, 'require_login', lambda dut: logged_in.append(dut.version))
  generator = fixtures.ota_connected_device.__wrapped__(device, True, Version('2.1.0'))
  assert next(generator) is device
  assert device.version == Version('2.1.0')
  assert restored == [(Version('2.3.0'), Version('2.1.0'))]
  assert logged_in == [Version('2.1.0')]
  with pytest.raises(StopIteration):
    next(generator)


def test_ota_fixture_restores_even_if_test_fails(monkeypatch):
  fixtures = load_ota_fixtures(monkeypatch)
  device = SimpleNamespace(version=Version('2.1.0'))
  monkeypatch.setattr(fixtures, 'read_firmware', lambda dut: (dut.version, 'ota_0', 'valid'))
  monkeypatch.setattr(fixtures, 'restore_firmware', lambda dut, target: setattr(dut, 'version', target))
  generator = fixtures.ota_connected_device.__wrapped__(device, True, Version('2.1.0'))
  next(generator)
  device.version = Version('2.3.0')
  with pytest.raises(AssertionError, match='intentional failure'):
    generator.throw(AssertionError('intentional failure'))
  assert device.version == Version('2.1.0')


def test_session_baseline_restored_at_end_of_suite(monkeypatch):
  fixtures = load_ota_fixtures(monkeypatch)
  commands = []
  device = SimpleNamespace(
    version=Version('2.1.0'),
    ota=SimpleNamespace(server=lambda url: commands.append(url)),
  )
  local_url = 'http://192.168.1.2:8000/fw7/'
  monkeypatch.setattr(fixtures, 'read_firmware', lambda dut: (dut.version, 'ota_0', 'valid'))
  monkeypatch.setattr(fixtures, 'restore_firmware', lambda dut, target: setattr(dut, 'version', target))
  monkeypatch.setattr(fixtures, 'require_login', lambda dut: commands.append('login'))
  session = fixtures.ota_initial_firmware.__wrapped__(device, local_url)
  assert next(session) == Version('2.1.0')
  assert commands == ['login', local_url]
  device.version = Version('2.3.0')
  with pytest.raises(StopIteration):
    next(session)
  assert device.version == Version('2.1.0')
