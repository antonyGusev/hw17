from lib import UARTConnector

from .controllers import (
  AlarmController,
  BuoyController,
  AuthController,
  ConfigController,
  DistanceSensorController,
  LampController,
  LedController,
  OtaController,
)


class DeviceDriver:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

    self.auth = AuthController(connector)
    self.alarm = AlarmController(connector)
    self.config = ConfigController(connector)
    self.distance = DistanceSensorController(connector)
    self.lamp = LampController(connector)
    self.led = LedController(connector)
    self.ota = OtaController(connector)
    self.buoy = BuoyController(connector)
    self.wifi = self.buoy  # Compatibility for existing tests; use device.buoy in new code.

  def help(self) -> list[str]:
    return self._connector.execute_command('help')

  def status(self) -> list[str]:
    # The response is complete only after the final heap field. The UART idle
    # timeout can expire between the command echo and the status lines.
    return self._connector.execute_command('status', until='heap:', timeout=10)
  
  def version(self, wait=True) -> list[str]:
    if wait:
      return self._connector.execute_command('version', until='state:', timeout=10)
    else:
      return self._connector.write_command('version')
    
  def open(self) -> None:
    self._connector.open()

  def close(self) -> None:
    self._connector.close()

  def reboot(self) -> list[str]:
    # Reboot is complete only when the fw_7 CLI reports its ready state.
    self._connector.write_command('reboot')

    return self._connector.wait_for_response('ready. state', timeout=90)

  def wait_for_log(self, pattern: str, timeout: float = 5) -> list[str]:
    return self._connector.wait_for_response(pattern, timeout)
  
  @property
  def is_open(self) -> bool:
    return self._connector.is_open
