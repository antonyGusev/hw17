import http.client
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

from lib.utilities import ota_server_manager as manager


def fake_cache(tmp_path, monkeypatch):
  server_dir = tmp_path / 'utilities'
  server_dir.mkdir()
  script = Path(__file__).resolve().parents[1] / 'lib' / 'utilities' / 'ota_server.py'
  destination = server_dir / 'ota_server.py'
  destination.write_bytes(script.read_bytes())
  fw = server_dir / 'server_files' / 'fw7'
  fw.mkdir(parents=True)
  (fw / 'stable.txt').write_text('2.1.0\n')
  (fw / 'beta.txt').write_text('2.3.0\n')
  for name in ('v2.1.0', 'v2.3.0', 'broken'):
    directory = fw / name
    directory.mkdir()
    (directory / 'sentry_fw7.bin').write_bytes(b'image')
  monkeypatch.setattr(manager, 'SERVER_SCRIPT', destination)
  monkeypatch.setattr(manager, 'ROOT', tmp_path)


def unused_port():
  with socket.socket() as sock:
    sock.bind(('127.0.0.1', 0))
    return sock.getsockname()[1]


def test_server_starts_and_stops(tmp_path, monkeypatch, capsys):
  fake_cache(tmp_path, monkeypatch)
  port = unused_port()
  monkeypatch.setenv('OTA_SERVER_PORT', str(port))
  previous = os.environ.get(manager.SERVER_URL_ENV)
  with manager.running_ota_server() as url:
    assert url == os.environ[manager.SERVER_URL_ENV]
    assert url.startswith('http://') and url.endswith(f':{port}/fw7/')
    assert manager._port_open(port)
    inherited = subprocess.check_output(
      [sys.executable, '-c', 'import os; print(os.environ["OTA_TEST_SERVER"])'], text=True,
    ).strip()
    assert inherited == url
    conn = http.client.HTTPConnection('127.0.0.1', port, timeout=2)
    conn.request('GET', '/fw7/stable.txt')
    response = conn.getresponse()
    assert response.status == 200
    assert response.read().splitlines() == [b'2.1.0']
    conn.request('GET', '/fw7/missing-channel/stable.txt')
    response = conn.getresponse()
    assert response.status == 404
    response.read()
    conn.request('GET', '/fw7/missing-channel/beta.txt')
    response = conn.getresponse()
    assert response.status == 404
    response.read()
    conn.request('GET', '/fw7/missing-channel/v2.1.0/sentry_fw7.bin')
    response = conn.getresponse()
    assert response.status == 200
    assert response.read() == b'image'
    conn.request('GET', '/fw7/stable.txt')
    response = conn.getresponse()
    assert response.status == 200
    assert response.read().splitlines() == [b'2.1.0']
    conn.close()
  assert not manager._port_open(port)
  assert os.environ.get(manager.SERVER_URL_ENV) == previous
  assert f'OTA server URL: {url}' in capsys.readouterr().out


def test_server_stops_when_test_fails(tmp_path, monkeypatch):
  fake_cache(tmp_path, monkeypatch)
  port = unused_port()
  monkeypatch.setenv('OTA_SERVER_PORT', str(port))
  with pytest.raises(AssertionError, match='test error'):
    with manager.running_ota_server() as url:
      assert os.environ[manager.SERVER_URL_ENV] == url
      assert manager._port_open(port)
      raise AssertionError('test error')
  assert not manager._port_open(port)


def test_occupied_port_is_not_killed(tmp_path, monkeypatch):
  fake_cache(tmp_path, monkeypatch)
  with socket.socket() as sock:
    sock.bind(('127.0.0.1', 0))
    sock.listen()
    port = sock.getsockname()[1]
    monkeypatch.setenv('OTA_SERVER_PORT', str(port))
    with pytest.raises(RuntimeError, match='occupied'):
      with manager.running_ota_server():
        pass
    assert manager._port_open(port)


def test_generated_url_overrides_static_env_and_restores_it(tmp_path, monkeypatch):
  fake_cache(tmp_path, monkeypatch)
  port = unused_port()
  monkeypatch.setenv('OTA_SERVER_PORT', str(port))
  monkeypatch.setenv(manager.SERVER_URL_ENV, 'http://old.invalid/fw7/')
  with manager.running_ota_server() as url:
    assert url != 'http://old.invalid/fw7/'
    assert os.environ[manager.SERVER_URL_ENV] == url
  assert os.environ[manager.SERVER_URL_ENV] == 'http://old.invalid/fw7/'


def test_download_start_failure_route_does_not_affect_normal_firmware(tmp_path, monkeypatch):
  fake_cache(tmp_path, monkeypatch)
  port = unused_port()
  monkeypatch.setenv('OTA_SERVER_PORT', str(port))

  with manager.running_ota_server():
    conn = http.client.HTTPConnection('127.0.0.1', port, timeout=2)
    failed = '/fw7/download-start-failure/v2.1.0/sentry_fw7.bin'
    normal = '/fw7/v2.1.0/sentry_fw7.bin'
    try:
      conn.request('HEAD', failed)
      response = conn.getresponse()
      assert response.status == 200
      assert response.getheader('Content-Length') == '5'
      assert response.read() == b''

      conn.request('GET', failed)
      response = conn.getresponse()
      assert response.status == 503
      assert b'image' not in response.read()

      conn.request('GET', normal)
      response = conn.getresponse()
      assert response.status == 200
      assert response.read() == b'image'

      conn.request('GET', failed)
      response = conn.getresponse()
      assert response.status == 503
      response.read()

      conn.request('GET', normal)
      response = conn.getresponse()
      assert response.status == 200
      assert response.read() == b'image'
    finally:
      conn.close()


def test_slow_route_only_throttles_its_requests(tmp_path, monkeypatch):
  fake_cache(tmp_path, monkeypatch)
  fw_file = tmp_path / 'utilities' / 'server_files' / 'fw7' / 'v2.1.0' / 'sentry_fw7.bin'
  payload = b'F' * (32 * 1024)
  fw_file.write_bytes(payload)
  port = unused_port()
  monkeypatch.setenv('OTA_SERVER_PORT', str(port))

  def download(path):
    conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
    try:
      start = time.monotonic()
      conn.request('GET', path)
      response = conn.getresponse()
      assert response.status == 200
      assert response.read() == payload
      return time.monotonic() - start
    finally:
      conn.close()

  with manager.running_ota_server():
    normal_before = download('/fw7/v2.1.0/sentry_fw7.bin')
    slow = download('/fw7/slow/v2.1.0/sentry_fw7.bin')
    normal_after = download('/fw7/v2.1.0/sentry_fw7.bin')

  assert slow > normal_before + 0.7, (normal_before, slow)
  assert slow > normal_after + 0.7, (normal_after, slow)
