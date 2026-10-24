from lib import UARTConnector, log_step


class LedController:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

  @log_step
  def on(self) -> list[str]:
    return self._connector.execute_command('led on')

  @log_step
  def off(self) -> list[str]:
    return self._connector.execute_command('led off')

  @log_step
  def auto(self) -> list[str]:
    return self._connector.execute_command('led auto')

  @log_step
  def rgb(self) -> list[str]:
    return self._connector.execute_command('led rgb')
