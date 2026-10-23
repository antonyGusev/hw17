import importlib.util
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest


def load_fixtures():
  path = Path(__file__).resolve().parents[1] / 'tests' / 'conftest.py'
  spec = importlib.util.spec_from_file_location('hil_pytest_fixtures', path)
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


def session(collectonly=False):
  return SimpleNamespace(config=SimpleNamespace(option=SimpleNamespace(collectonly=collectonly)))


def test_standalone_pytest_starts_and_stops_server(monkeypatch):
  fixtures = load_fixtures()
  monkeypatch.delenv(fixtures.SERVER_MANAGED_ENV, raising=False)
  events = []

  @contextmanager
  def server():
    events.append('start')
    try:
      yield 'http://192.168.1.2:8000/fw7/'
    finally:
      events.append('stop')

  monkeypatch.setattr(fixtures, 'running_ota_server', server)
  run = session()
  fixtures.pytest_sessionstart(run)
  assert run.config._ota_server_url == 'http://192.168.1.2:8000/fw7/'
  assert events == ['start']
  fixtures.pytest_sessionfinish(run, 1)
  fixtures.pytest_unconfigure(run.config)
  assert events == ['start', 'stop']


def test_matrix_stage_reuses_runner_server(monkeypatch):
  fixtures = load_fixtures()
  monkeypatch.setenv(fixtures.SERVER_MANAGED_ENV, '1')
  monkeypatch.setenv(fixtures.SERVER_URL_ENV, 'http://192.168.1.2:8000/fw7/')
  monkeypatch.setattr(fixtures, 'running_ota_server', lambda: pytest.fail('Must not start another server'))
  run = session()
  fixtures.pytest_sessionstart(run)
  assert run.config._ota_server_url == 'http://192.168.1.2:8000/fw7/'
  fixtures.pytest_sessionfinish(run, 0)


def test_collect_only_does_not_start_server(monkeypatch):
  fixtures = load_fixtures()
  monkeypatch.delenv(fixtures.SERVER_MANAGED_ENV, raising=False)
  monkeypatch.setattr(fixtures, 'running_ota_server', lambda: pytest.fail('Must not start on --collect-only'))
  run = session(collectonly=True)
  fixtures.pytest_sessionstart(run)
  assert not hasattr(run.config, '_ota_server_url')
  fixtures.pytest_sessionfinish(run, 0)
