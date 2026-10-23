import pytest

from framework.hil.controllers.buttons_controller import ButtonsController


class Connector:
  def __init__(self):
    self.calls = []

  def execute_command(self, command, timeout=None, until=None):
    self.calls.append((command, timeout, until))
    button = command.split()[1] if command.startswith('hold ') else command
    return [f'[HIL] {button.upper()} release']


def test_hold_sends_button_and_seconds():
  connector = Connector()
  response = ButtonsController(connector).hold('k1', 1.7)
  assert connector.calls[0][0] == 'hold k1 1.7'
  assert connector.calls[0][1] > 1.7
  assert '[HIL] K1 release' in response


@pytest.mark.parametrize(('button', 'duration'), [('k5', 1.5), ('k1', 0), ('k1', 31), ('k1', float('nan'))])
def test_hold_rejects_invalid_arguments(button, duration):
  with pytest.raises(ValueError):
    ButtonsController(Connector()).hold(button, duration)


def test_old_short_button_commands_remain_unchanged():
  connector = Connector()
  ButtonsController(connector).k1()
  assert connector.calls[0][0] == 'k1'
