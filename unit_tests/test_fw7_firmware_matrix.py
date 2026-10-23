import importlib.util
import os
from pathlib import Path
from types import SimpleNamespace

import pytest
from packaging.version import Version


def load_runner():
  path = Path(__file__).resolve().parents[1] / 'run_firmware_matrix.py'
  spec = importlib.util.spec_from_file_location('fw7_firmware_matrix', path)
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


def test_fw7_matrix_runs_gatekeeper_and_both_versions(monkeypatch):
  runner = load_runner()
  events = []
  monkeypatch.setattr(runner, 'check_version', lambda version: events.append(('check', str(version))))
  monkeypatch.setattr(runner, 'install_version', lambda source, target: events.append(('install', str(source), str(target))))
  monkeypatch.setattr(runner, 'run_pytest', lambda label, args, allow_failures=True: events.append(('pytest', label, tuple(args))) or True)
  monkeypatch.setattr(runner.subprocess, 'run', lambda *args, **kwargs: events.append(('flash',)))

  assert runner.main() == 0
  assert events[0] == ('flash',)
  assert [event[1] for event in events if event[0] == 'pytest'] == [
    '2.1.0: first', '2.1.0: OTA gatekeeper', '2.1.0: suite', '2.3.0: suite',
  ]
  assert ('install', '2.1.0', '2.3.0') in events
  assert events[-1] == ('check', '2.3.0')


def test_no_flash_requires_stable_and_skips_first(monkeypatch):
  runner = load_runner()
  events = []
  monkeypatch.setattr(runner, 'check_version', lambda version: events.append(('check', str(version))))
  monkeypatch.setattr(runner, 'install_version', lambda source, target: events.append(('install', str(source), str(target))))
  monkeypatch.setattr(runner, 'run_pytest', lambda label, args, allow_failures=True: events.append(('pytest', label)) or True)
  monkeypatch.setattr(runner.subprocess, 'run', lambda *args, **kwargs: pytest.fail('Must not flash in --no-flash mode'))

  assert runner.main(no_flash=True) == 0
  assert events[0] == ('check', '2.1.0')
  assert '2.1.0: first' not in [event[1] for event in events if event[0] == 'pytest']


def test_failed_gatekeeper_prevents_firmware_upgrade(monkeypatch):
  runner = load_runner()
  calls = []
  monkeypatch.setattr(runner, 'check_version', lambda version: calls.append(('check', str(version))))
  monkeypatch.setattr(runner, 'install_version', lambda *args: pytest.fail('Must not upgrade after failed gatekeeper'))

  def run_pytest(label, args, allow_failures=True):
    calls.append(('pytest', label))
    assert not allow_failures
    raise RuntimeError('gatekeeper failed')

  monkeypatch.setattr(runner, 'run_pytest', run_pytest)
  with pytest.raises(RuntimeError, match='gatekeeper failed'):
    runner.main(no_flash=True)
  assert calls == [('check', '2.1.0'), ('pytest', '2.1.0: OTA gatekeeper')]


def test_flash_checks_fw7_image_before_erasing(monkeypatch, tmp_path):
  import flash_device

  monkeypatch.setattr(flash_device, 'FIRMWARE_PATH', tmp_path / 'missing_fw7_v2.1.0_merged.bin')
  with pytest.raises(FileNotFoundError, match='FW7_FLASH_IMAGE'):
    flash_device.main()


def test_pristine_slot_flag_is_scoped_to_first_stage(monkeypatch):
  runner = load_runner()
  monkeypatch.delenv('OTA_PRISTINE_SINGLE_SLOT', raising=False)
  phases = []

  monkeypatch.setattr(runner, 'check_version', lambda version: None)
  monkeypatch.setattr(runner, 'install_version', lambda source, target: None)
  monkeypatch.setattr(runner.subprocess, 'run', lambda *args, **kwargs: None)

  def run_pytest(label, args, allow_failures=True):
    phases.append((label, os.getenv('OTA_PRISTINE_SINGLE_SLOT')))
    return True

  monkeypatch.setattr(runner, 'run_pytest', run_pytest)

  assert runner.main() == 0
  assert phases[0] == ('2.1.0: first', '1')
  assert all(value is None for _, value in phases[1:])
  assert os.getenv('OTA_PRISTINE_SINGLE_SLOT') is None


def test_pristine_slot_flag_removed_after_first_failure(monkeypatch):
  runner = load_runner()
  monkeypatch.delenv('OTA_PRISTINE_SINGLE_SLOT', raising=False)
  monkeypatch.setattr(runner, 'check_version', lambda version: None)
  monkeypatch.setattr(runner.subprocess, 'run', lambda *args, **kwargs: None)

  def run_pytest(label, args, allow_failures=True):
    assert os.getenv('OTA_PRISTINE_SINGLE_SLOT') == '1'
    raise RuntimeError('first stage failed')

  monkeypatch.setattr(runner, 'run_pytest', run_pytest)

  with pytest.raises(RuntimeError, match='first stage failed'):
    runner.main()
  assert os.getenv('OTA_PRISTINE_SINGLE_SLOT') is None


def test_pristine_slot_flag_restores_existing_env_value(monkeypatch):
  runner = load_runner()
  monkeypatch.setenv('OTA_PRISTINE_SINGLE_SLOT', 'manual')
  phases = []

  monkeypatch.setattr(runner, 'check_version', lambda version: None)
  monkeypatch.setattr(runner, 'install_version', lambda source, target: None)
  monkeypatch.setattr(runner.subprocess, 'run', lambda *args, **kwargs: None)

  def run_pytest(label, args, allow_failures=True):
    phases.append((label, os.getenv('OTA_PRISTINE_SINGLE_SLOT')))
    return True

  monkeypatch.setattr(runner, 'run_pytest', run_pytest)
  assert runner.main() == 0
  assert phases[0] == ('2.1.0: first', '1')
  assert all(value == 'manual' for _, value in phases[1:])
  assert os.getenv('OTA_PRISTINE_SINGLE_SLOT') == 'manual'
