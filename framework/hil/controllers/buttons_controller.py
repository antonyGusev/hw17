import math
from typing import Literal

from lib import UARTConnector

Button = Literal['k1', 'k2', 'k3', 'k4']


class ButtonsController:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

  def k1(self) -> list[str]:
    return self._press('k1')

  def k2(self) -> list[str]:
    return self._press('k2')

  def k3(self) -> list[str]:
    return self._press('k3')

  def k4(self) -> list[str]:
    return self._press('k4')
  
  def hold(self, button: Button, duration: float) -> list[str]:
    button = button.lower()
    if button not in ('k1', 'k2', 'k3', 'k4'):
      raise ValueError(f'Unknown HIL button: {button}')

    if not math.isfinite(duration) or not 0.05 <= duration <= 30:
      raise ValueError('Hold duration must be between 0.05 and 30 seconds')

    return self._connector.execute_command(
      f'hold {button} {duration:g}',
      timeout=duration + 3,
      until=(f'[HIL] {button.upper()} release', '[HIL] ERROR:'),
    )

  # region Service methods

  def _press(self, button: str) -> list[str]:
    return self._connector.execute_command(
      button,
      timeout=2,
      until=f'[HIL] {button.upper()} release',
    )
    
  # endregion
