"""Report routing and media attachment checks without requiring the Allure CLI."""

from contextlib import contextmanager
from types import SimpleNamespace

import pytest

from lib.utilities.logger import allure_logger, step_logger


class FakeAllure:
  def __init__(self):
    self.steps = []
    self.texts = []
    self.files = []
    self.attach = SimpleNamespace(__call__=self.attach_text, file=self.attach_file)

  @contextmanager
  def step(self, title):
    self.steps.append(title)
    yield

  def attach_text(self, body, name, attachment_type, extension):
    self.texts.append((name, body, attachment_type, extension))

  def attach_file(self, path, name, attachment_type, extension):
    self.files.append((path, name, attachment_type, extension))


@pytest.fixture
def report(monkeypatch):
  reporter = FakeAllure()
  reporter.attach = lambda body, name, attachment_type, extension: reporter.attach_text(body, name, attachment_type, extension)
  reporter.attach.file = reporter.attach_file
  monkeypatch.setattr(allure_logger, 'allure', reporter)
  monkeypatch.setenv('STEP_LOG_REPORTER', 'allure')
  return reporter


def test_allure_ignores_console_silent_and_debug_levels(report, monkeypatch):
  from framework.device.controllers.lamp_controller import LampController

  class StubConnector:
    def execute_command(self, command, **kwargs):
      return ['[BEACON] on']

  for level in ('silent', 'debug'):
    monkeypatch.setenv('STEP_LOG_LEVEL', level)
    assert LampController(StubConnector()).on() == ['[BEACON] on']
  assert len(report.steps) == 2
  assert all('LampController.on(' in title for title in report.steps)
  assert [item[0] for item in report.texts] == ['Result', 'Result']


def test_allure_excludes_connector_and_module_steps(report):
  from framework.device.controllers.lamp_controller import LampController

  class StubConnector:
    def execute_command(self, command, **kwargs):
      return ['[BEACON] on']

  assert LampController(StubConnector()).on() == ['[BEACON] on']
  assert len(report.steps) == 1
  assert 'LampController' in report.steps[0]


def test_allure_redacts_sensitive_arguments_and_result(report):
  from framework.device.controllers.auth_controller import AuthController

  class StubConnector:
    def execute_command(self, command, **kwargs):
      return [f'password: highlysecret123', 'login qa highlysecret123']

  AuthController(StubConnector()).login('qa', 'highlysecret123')
  assert report.steps
  assert all('highlysecret123' not in title for title in report.steps)
  assert all('highlysecret123' not in body for _, body, _, _ in report.texts)


def test_allure_exception_is_attached_and_propagates(report):
  from framework.device.controllers.lamp_controller import LampController

  class StubConnector:
    def execute_command(self, command, **kwargs):
      raise RuntimeError('connector offline')

  with pytest.raises(RuntimeError, match='connector offline'):
    LampController(StubConnector()).on()
  assert len(report.steps) == 1
  assert report.texts[-1][0] == 'Exception'


def test_allure_media_are_attached_using_mime_types(report, tmp_path):
  for name, media_type in [('frame.jpg', 'image/jpeg'), ('roi.png', 'image/png'), ('mode.mp4', 'video/mp4')]:
    source = tmp_path/name
    source.write_bytes(b'placeholder')
    step_logger.attach_artifact(source)
    assert report.files[-1][1] == name
    assert report.files[-1][2] == media_type
  assert len(report.files) == 3


def test_console_does_not_attach_media(monkeypatch, tmp_path):
  monkeypatch.setenv('STEP_LOG_REPORTER', 'console')
  source = tmp_path/'frame.jpg'
  source.write_bytes(b'image')
  step_logger.attach_artifact(source)


def test_invalid_reporter_is_rejected(monkeypatch):
  monkeypatch.setenv('STEP_LOG_REPORTER', 'archive')
  with pytest.raises(ValueError, match='STEP_LOG_REPORTER'):
    step_logger._reporter()


def test_allure_optional_dependency_error(monkeypatch):
  monkeypatch.setenv('STEP_LOG_REPORTER', 'allure')
  monkeypatch.setattr(allure_logger, 'allure', None)
  from framework.device.controllers.lamp_controller import LampController

  with pytest.raises(RuntimeError, match='allure-pytest'):
    LampController(object()).on()


def test_allure_reporting_failure_cannot_fail_camera_attachment(report, tmp_path):
  def bad_attachment(path, name, attachment_type, extension):
    raise OSError(6, 'invalid handle')
  report.attach.file = bad_attachment
  source = tmp_path/'image.jpg'
  source.write_bytes(b'image')
  step_logger.attach_artifact(source)


def test_camera_roi_artifact_attached_after_successful_write(report, tmp_path):
  np = pytest.importorskip('numpy')
  from framework.hil.controllers.modules.base_camera_module import BaseCameraModule
  cam = BaseCameraModule(type('Endpoints', (), {'capture_url': '', 'stream_url': ''})())
  path = tmp_path/'test_roi.jpg'
  cam.save_roi(np.zeros((480, 480, 3), dtype=np.uint8), str(path))
  assert path.is_file()
  assert report.files[-1][1] == 'test_roi.jpg'


def test_video_artifact_attached_after_writing(report, tmp_path, monkeypatch):
  np = pytest.importorskip('numpy')
  from framework.hil.controllers.modules import video_module

  class FakeWriter:
    def __init__(self, path, *_):
      self.path = path
    def isOpened(self):
      return True
    def write(self, frame):
      pass
    def release(self):
      from pathlib import Path
      Path(self.path).write_bytes(b'mp4')

  monkeypatch.setattr(video_module.cv2, 'VideoWriter', FakeWriter)
  cam = video_module.VideoModule(type('Endpoints', (), {'capture_url': '', 'stream_url': ''})())
  path = tmp_path/'mode.mp4'
  cam._save_video([np.zeros((2, 2, 3), dtype=np.uint8)], str(path))
  assert path.is_file()
  assert report.files[-1][1] == 'mode.mp4'


def test_allure_uses_driver_paths_and_buoy_name(report):
  from framework.device.device_driver import DeviceDriver
  from framework.hil.hil_driver import HILDriver

  class StubConnector:
    def execute_command(self, command, **kwargs):
      return ['[BEACON] on']

  device = DeviceDriver(StubConnector())
  device.lamp.on()
  assert report.steps[-1] == 'DeviceDriver.lamp.on()'
  assert device.buoy._log_path == 'DeviceDriver.buoy'
  class NetworkConnector:
    def execute_command(self, command, **kwargs):
      return ["W114 connected to 'test-ap'"]
  device.buoy._connector = NetworkConnector()
  assert device.buoy.reconnect().connected
  assert report.steps[-1] == 'DeviceDriver.buoy.reconnect()'

  hil = HILDriver(StubConnector())
  hil.buttons.k1()
  assert report.steps[-1] == 'HILDriver.buttons.k1()'


def test_allure_lamp_status_uses_driver_path(report):
  from framework.device.device_driver import DeviceDriver

  class StubConnector:
    def execute_command(self, command, **kwargs):
      return ['{"lamp":"on","color":[255,255,255],"brightness":50,"mode":"solid","timer_s":0}']

  assert DeviceDriver(StubConnector()).lamp.status().is_on
  assert report.steps == ['DeviceDriver.lamp.status()', 'DeviceDriver.lamp.status_raw()']
