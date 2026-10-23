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
