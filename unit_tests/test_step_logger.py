import inspect

import pytest

from lib.utilities import log_step
from lib.utilities import step_logger


class ExampleDevice:
  @log_step
  def version(self, wait=True):
    return ['version', 'I (10) sentry: firmware v2.1.0']

  @log_step
  def run(self, command: str, password: str, timeout: int = 2):
    return [command, f'password: {password}', 'done']

  @log_step
  def status(self, response):
    return response

  @log_step
  def fails(self, password):
    raise RuntimeError(f'Could not log in with {password}')

  @log_step
  def login(self, password):
    return False

  @log_step
  def options(self, **kwargs):
    return kwargs


@pytest.fixture
def messages(monkeypatch):
  records = []
  monkeypatch.setattr(step_logger, '_emit', records.append)
  monkeypatch.setenv('STEP_LOG_LEVEL', 'verbose')
  return records


def test_verbose_records_method_inputs_and_result(messages):
  result = ExampleDevice().version(wait=False)
  assert result == ['version', 'I (10) sentry: firmware v2.1.0']
  assert len(messages) == 2
  assert '[STEP]' in messages[0]
  assert 'ExampleDevice.version(wait=False)' in messages[0]
  assert '[OK]' in messages[1]
  assert 'firmware v2.1.0' in messages[1]


def test_warnings_and_errors_from_uart_results(messages, monkeypatch):
  monkeypatch.setenv('STEP_LOG_LEVEL', 'warning')
  device = ExampleDevice()
  device.status(['lamp on', 'W (3) sentry: W510 already on'])
  device.status(['lamp on', 'E (3) sentry: E503 invalid color'])
  device.status(['lamp on', 'successful'])
  assert len(messages) == 2
  assert '[WARNING]' in messages[0] and 'W510' in messages[0]
  assert '[ERROR]' in messages[1] and 'E503' in messages[1]


def test_error_filters_out_success_and_warning(messages, monkeypatch):
  monkeypatch.setenv('STEP_LOG_LEVEL', 'error')
  device = ExampleDevice()
  device.status(['W510 lamp already on'])
  device.version()
  device.login(password='topsecret')
  assert len(messages) == 1
  assert '[ERROR]' in messages[0]
  assert 'topsecret' not in messages[0]
  assert 'password=***' in messages[0]


def test_silent_does_not_change_operation(messages, monkeypatch):
  monkeypatch.setenv('STEP_LOG_LEVEL', 'silent')
  assert ExampleDevice().version() == ['version', 'I (10) sentry: firmware v2.1.0']
  assert messages == []


def test_passwords_redacted_from_args_and_return(messages):
  ExampleDevice().run('login qa pass12345', 'pass12345', timeout=7)
  assert len(messages) == 2
  assert all('pass12345' not in message for message in messages)
  assert 'timeout=7' in messages[0]
  assert 'password=***' in messages[0]
  assert '[OK]' in messages[1]


def test_nested_sensitive_keyword_values_redacted(messages):
  ExampleDevice().options(token='very-secret-token', keep='ok')
  assert all('very-secret-token' not in message for message in messages)
  assert 'keep' in messages[0]


def test_exceptions_are_logged_and_re_raised(messages):
  with pytest.raises(RuntimeError, match='Could not log in'):
    ExampleDevice().fails('password123')
  assert '[ERROR]' in messages[-1]
  assert 'RuntimeError' in messages[-1]
  assert 'password123' not in messages[-1]


def test_invalid_log_level_does_not_run_method(messages, monkeypatch):
  monkeypatch.setenv('STEP_LOG_LEVEL', 'trace')
  with pytest.raises(ValueError, match='STEP_LOG_LEVEL'):
    ExampleDevice().version()


def test_decorator_preserves_signature():
  assert ExampleDevice.version.__name__ == 'version'
  assert str(inspect.signature(ExampleDevice.version)) == '(self, wait=True)'


def test_error_command_masks_passwords_in_text(messages):
  ExampleDevice().status(['login qa private123', 'register qa other456', 'passwd old321 new789', 'sudo supersecret', 'guard disarm 1234'])
  assert all(secret not in messages[-1] for secret in ['private123', 'other456', 'old321', 'new789', 'supersecret', '1234'])

class MockSerial:
  is_open = True

  def __init__(self):
    self.sent = []

  def write(self, data):
    self.sent.append(data)

  def flush(self):
    pass


def _mock_uart(monkeypatch):
  from lib.connectors.uart_connector import UARTConnector

  connector = UARTConnector('TEST')
  connector.ser = MockSerial()
  monkeypatch.setattr(connector, '_read_response', lambda timeout, until=None: ['[BEACON] on'])
  return connector


def test_debug_shows_nested_controller_connector_chain(messages, monkeypatch):
  from framework.device.controllers.lamp_controller import LampController

  monkeypatch.setenv('STEP_LOG_LEVEL', 'debug')
  connector = _mock_uart(monkeypatch)
  assert LampController(connector).on() == ['[BEACON] on']
  starts = [line for line in messages if '[STEP]' in line]
  assert len(starts) == 3
  assert '[CONTROLLER]' in starts[0] and 'LampController.on' in starts[0]
  assert '[CONNECTOR]' in starts[1] and 'UARTConnector.execute_command' in starts[1]
  assert '[CONNECTOR]' in starts[2] and 'UARTConnector.write_command' in starts[2]
  assert not starts[0].startswith('  ')
  assert starts[1].startswith('  ')
  assert starts[2].startswith('    ')


def test_verbose_hides_connector_but_keeps_controller_and_driver(messages, monkeypatch):
  from framework.device.device_driver import DeviceDriver

  monkeypatch.setenv('STEP_LOG_LEVEL', 'verbose')
  connector = _mock_uart(monkeypatch)
  device = DeviceDriver(connector)
  assert device.lamp.on() == ['[BEACON] on']
  assert device.help() == ['[BEACON] on']
  starts = [line for line in messages if '[STEP]' in line]
  assert len(starts) == 2
  assert 'LampController.on' in starts[0]
  assert 'DeviceDriver.help' in starts[1]
  assert all('UARTConnector' not in line for line in messages)


def test_debug_masks_auth_and_uart_password(messages, monkeypatch):
  from framework.device.controllers.auth_controller import AuthController

  monkeypatch.setenv('STEP_LOG_LEVEL', 'debug')
  connector = _mock_uart(monkeypatch)
  AuthController(connector).login('qauser', 'criticalpassword123')
  assert all('criticalpassword123' not in line for line in messages)
  assert any('password=***' in line for line in messages)


def test_warning_level_keeps_nested_uart_error(messages, monkeypatch):
  from framework.device.controllers.lamp_controller import LampController

  monkeypatch.setenv('STEP_LOG_LEVEL', 'warning')
  connector = _mock_uart(monkeypatch)
  monkeypatch.setattr(connector, '_read_response', lambda timeout, until=None: ['E502 bad RGB'])
  result = LampController(connector).set_rgb(-1, 0, 0)
  assert result == ['E502 bad RGB']
  assert messages and all('[ERROR]' in line for line in messages)


def test_debug_summarizes_numpy_frame_without_pixel_dump(messages, monkeypatch):
  np = pytest.importorskip('numpy')
  from framework.hil.controllers.modules.base_camera_module import BaseCameraModule

  monkeypatch.setenv('STEP_LOG_LEVEL', 'debug')
  dummy = BaseCameraModule(type('Endpoints', (), {'capture_url': '', 'stream_url': ''})())
  frame = np.zeros((500, 500, 3), dtype=np.uint8)
  dummy.get_roi(frame)
  assert any('shape=(500, 500, 3)' in line for line in messages)
  assert all(len(line) < 1300 for line in messages)


def test_call_stack_is_reset_after_failure(messages, monkeypatch):
  from framework.device.controllers.lamp_controller import LampController

  monkeypatch.setenv('STEP_LOG_LEVEL', 'debug')
  connector = _mock_uart(monkeypatch)
  def fail(timeout, until=None):
    raise RuntimeError('UART failed')
  monkeypatch.setattr(connector, '_read_response', fail)
  with pytest.raises(RuntimeError, match='UART failed'):
    LampController(connector).on()
  messages.clear()
  monkeypatch.setattr(connector, '_read_response', lambda timeout, until=None: ['[BEACON] on'])
  LampController(connector).on()
  first = next(line for line in messages if '[STEP]' in line)
  assert first.startswith('[STEP]')


def test_debug_masks_password_passed_as_raw_uart_command(messages, monkeypatch):
  monkeypatch.setenv('STEP_LOG_LEVEL', 'debug')
  connector = _mock_uart(monkeypatch)

  class InteractiveLogin:
    @log_step
    def connect(self, password: str):
      connector.write_command(password)
      return True

  assert InteractiveLogin().connect('wifi-password-987654')
  assert connector.ser.sent[-1] == b'wifi-password-987654\r\n'
  assert all('wifi-password-987654' not in line for line in messages)
  assert any('command=\'***\'' in line for line in messages)


class _UnavailableConsole:
  def __init__(self, error):
    self.error = error

  def write(self, message):
    raise self.error

  def flush(self):
    raise self.error


def test_invalid_console_handle_uses_fallback_stream(monkeypatch):
  monkeypatch.delenv('PYTEST_CURRENT_TEST', raising=False)
  from io import StringIO

  output = StringIO()
  monkeypatch.setattr(step_logger.sys, '__stdout__', _UnavailableConsole(OSError(6, 'Invalid handle')))
  monkeypatch.setattr(step_logger.sys, '__stderr__', output)
  step_logger._emit('[STEP] test')
  assert '[STEP] test' in output.getvalue()


def test_logger_cannot_break_method_when_every_stream_is_invalid(monkeypatch):
  monkeypatch.delenv('PYTEST_CURRENT_TEST', raising=False)
  monkeypatch.setenv('STEP_LOG_LEVEL', 'debug')
  invalid = _UnavailableConsole(OSError(6, 'Invalid handle'))
  closed = _UnavailableConsole(ValueError('I/O operation on closed file'))
  for name, value in (('__stdout__', invalid), ('__stderr__', invalid), ('stdout', closed), ('stderr', closed)):
    monkeypatch.setattr(step_logger.sys, name, value)
  assert ExampleDevice().version(wait=False) == ['version', 'I (10) sentry: firmware v2.1.0']
  with pytest.raises(RuntimeError, match='Could not log in'):
    ExampleDevice().fails('pass123456')


def test_pytest_live_logging_uses_logging_instead_of_invalid_stdout(monkeypatch):
  monkeypatch.setenv('PYTEST_CURRENT_TEST', 'test_example (call)')
  monkeypatch.setattr(step_logger.sys, '__stdout__', _UnavailableConsole(OSError(6, 'Invalid handle')))
  records = []
  monkeypatch.setattr(step_logger._STEP_LOGGER, 'log', lambda severity, message: records.append((severity, message)))

  step_logger._emit('[STEP] demo')
  step_logger._emit('[WARNING] demo')
  step_logger._emit('[ERROR] demo')

  assert [severity for severity, _ in records] == [
    step_logger.logging.INFO, step_logger.logging.WARNING, step_logger.logging.ERROR,
  ]
  assert all('demo' in message for _, message in records)


def test_pytest_logging_failure_does_not_break_device_calls(monkeypatch):
  monkeypatch.setenv('STEP_LOG_LEVEL', 'verbose')
  monkeypatch.setenv('PYTEST_CURRENT_TEST', 'test_example (call)')
  def broken_log(severity, message):
    raise OSError(6, 'Invalid handle')
  monkeypatch.setattr(step_logger._STEP_LOGGER, 'log', broken_log)

  assert ExampleDevice().version() == ['version', 'I (10) sentry: firmware v2.1.0']
  with pytest.raises(RuntimeError, match='Could not log in'):
    ExampleDevice().fails('password123')


def test_missing_log_level_defaults_to_silent(monkeypatch):
  monkeypatch.delenv('STEP_LOG_LEVEL', raising=False)
  messages = []
  monkeypatch.setattr(step_logger, '_emit', messages.append)

  assert step_logger._log_level() == 'silent'
  assert ExampleDevice().version() == ['version', 'I (10) sentry: firmware v2.1.0']
  assert messages == []
