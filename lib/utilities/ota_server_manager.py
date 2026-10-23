"""Session lifecycle for the existing local fw_7 OTA HTTP server."""

import os
import socket
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path

from lib.utilities.ota_server import local_ip

SERVER_SCRIPT = Path(__file__).with_name('ota_server.py')
SERVER_MANAGED_ENV = 'FW7_OTA_SERVER_MANAGED'
SERVER_URL_ENV = 'OTA_TEST_SERVER'
ROOT = Path(__file__).resolve().parents[2]


def _port_open(port):
  try:
    with socket.create_connection(('127.0.0.1', port), timeout=0.2):
      return True
  except OSError:
    return False


def _firmware_ready():
  fw = SERVER_SCRIPT.parent / 'server_files' / 'fw7'
  stable = fw / 'stable.txt'
  beta = fw / 'beta.txt'
  if not stable.is_file() or not beta.is_file():
    return False
  try:
    versions = {stable.read_text().strip(), beta.read_text().strip()}
  except OSError:
    return False
  images_present = all(
    version and (fw / f'v{version}' / 'sentry_fw7.bin').is_file() for version in versions
  )
  return images_present and (fw / 'broken' / 'sentry_fw7.bin').is_file()


@contextmanager
def running_ota_server():
  """Start one owned process and always stop it, even on pytest failures."""
  port = int(os.getenv('OTA_SERVER_PORT', '8000'))
  if not 1 <= port <= 65535:
    raise ValueError(f'Invalid OTA_SERVER_PORT: {port}')
  if not SERVER_SCRIPT.is_file():
    raise FileNotFoundError(f'Local OTA server is missing: {SERVER_SCRIPT}')
  if _port_open(port):
    raise RuntimeError(f'Port {port} is occupied. Stop the existing server or set OTA_SERVER_PORT.')

  if not _firmware_ready():
    print('OTA server: downloading firmware cache (--download) ...', flush=True)
    subprocess.run([sys.executable, str(SERVER_SCRIPT), '--download'], cwd=ROOT, check=True)
    if not _firmware_ready():
      raise RuntimeError('OTA server firmware cache is incomplete after --download')

  log_path = ROOT / 'artifacts' / 'ota_server.log'
  log_path.parent.mkdir(parents=True, exist_ok=True)
  with log_path.open('w', encoding='utf-8') as log:
    process = subprocess.Popen(
      [sys.executable, '-u', str(SERVER_SCRIPT), '--port', str(port)],
      cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
    )
    try:
      deadline = time.monotonic() + 10
      while time.monotonic() < deadline:
        if process.poll() is not None:
          raise RuntimeError(f'OTA server exited (code {process.returncode}); see {log_path}')
        if _port_open(port):
          print(f'OTA server started: port {port} (PID {process.pid}); log: {log_path}', flush=True)
          break
        time.sleep(0.1)
      else:
        raise RuntimeError(f'OTA server did not start on port {port}; see {log_path}')
      url = f'http://{local_ip()}:{port}/fw7/'
      previous_url = os.environ.get(SERVER_URL_ENV)
      os.environ[SERVER_URL_ENV] = url
      print(f'OTA server URL: {url}', flush=True)
      try:
        yield url
      finally:
        if previous_url is None:
          os.environ.pop(SERVER_URL_ENV, None)
        else:
          os.environ[SERVER_URL_ENV] = previous_url
    finally:
      if process.poll() is None:
        process.terminate()
        try:
          process.wait(timeout=5)
        except subprocess.TimeoutExpired:
          process.kill()
          process.wait(timeout=5)
      print('OTA server stopped.', flush=True)
