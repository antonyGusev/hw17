import re

import serial

from config import FIRMWARE_PATH, HIL_PORT
from framework import DeviceDriver, HILDriver
from lib import FirmwareFlasher, UARTConnector, find_device_port, wait_for_condition


def wait_for_device(port: str, timeout: float = 15) -> None:
  connector = UARTConnector(port)
  device = DeviceDriver(connector)

  def is_ready() -> bool:
    try:
      if connector.ser is None or not connector.ser.is_open:
        connector.open()

      response = device.help()

      return any(re.search(r'Commands \(', line) for line in response)
    except (serial.SerialException, OSError):
      connector.close()
      return False

  try:
    wait_for_condition(
      is_ready,
      timeout=timeout,
      interval=0.5,
      error_message=f'DUT is not responding to help on {port}.',
    )
  finally:
    connector.close()


def main():
  if not FIRMWARE_PATH.is_file():
    raise FileNotFoundError(
      f'fw_7 v2.1.0 merged firmware not found: {FIRMWARE_PATH}. '
      'Set FW7_FLASH_IMAGE to the v2.1.0 merged binary, or use '
      '`poe full_cycle_no_flash` with an already flashed v2.1.0 device.'
    )
  if 'merged' not in FIRMWARE_PATH.name.lower() or 'station_wifi' in FIRMWARE_PATH.name.lower():
    raise ValueError(f'Expected a fw_7 merged binary for flashing at 0x0: {FIRMWARE_PATH}')

  hil_connector = UARTConnector(HIL_PORT)
  hil_connector.open()

  try:
    hil = HILDriver(hil_connector)
    hil.power_on()

    port = find_device_port()

    flasher = FirmwareFlasher()
    flasher.erase(port)
    flasher.flash(port, str(FIRMWARE_PATH))

    try:
      wait_for_device(port)
      print('DUT is ready after flashing.')

    except TimeoutError:
      print('DUT is not responding. Performing HIL power cycle...')

      hil.power_cycle()

      wait_for_device(port, timeout=30)
      print('DUT recovered after power cycle.')

  finally:
    hil_connector.close()


if __name__ == '__main__':
  main()
