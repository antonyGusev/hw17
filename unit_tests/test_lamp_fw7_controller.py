import pytest

from framework.device.controllers.lamp_controller import LampController
from lib import ResponseParseError


class Connector:
  def __init__(self, response=None):
    self.calls = []
    self.response = response or ['[BEACON] ON, color (12,34,56), brightness 37%, mode breathe, timer 9 s left']

  def execute_command(self, command, timeout=None, until=None):
    self.calls.append((command, timeout, until))
    return self.response


def test_text_status_parses_fw7():
  lamp = LampController(Connector())
  status = lamp.status()
  assert status.is_on
  assert (status.color, status.brightness, status.mode, status.timer_s) == ((12,34,56),37,'breathe',9)


def test_off_status_without_running_timer():
  lamp = LampController(Connector(['[BEACON] off, color (0,0,255), brightness 0%, mode solid, timer off']))
  assert not lamp.status().is_on
  assert lamp.status().timer_s == 0


def test_unparsable_status_rejected():
  with pytest.raises(ResponseParseError):
    LampController(Connector(['lamp status', 'something else'])).status()


def test_toggle_uses_fw7_command():
  connector = Connector()
  LampController(connector).toggle()
  assert connector.calls[0][0] == 'lamp toggle'


def test_status_waits_for_status_not_asynchronous_timer_expiry():
  connector = Connector([
    '[BEACON] off (timer expired)',
    '[BEACON] off, color (12,34,56), brightness 37%, mode breathe, timer off',
  ])
  status = LampController(connector).status()
  assert not status.is_on
  assert status.timer_s == 0
  command, timeout, until = connector.calls[-1]
  assert command == 'lamp status'
  assert 'timer' not in until
  assert 'timer off' in until
  assert ' s left' in until
  assert 'E002' in until
  assert timeout == 5


def test_status_active_timer_waits_for_remaining_seconds():
  connector = Connector()
  status = LampController(connector).status()
  assert status.timer_s == 9
  assert ' s left' in connector.calls[-1][2]
