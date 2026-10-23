import json
import re
from dataclasses import dataclass

from lib import ResponseParseError, UARTConnector


@dataclass
class LampStatus:
  lamp: str
  color: tuple[int, int, int]
  brightness: int
  mode: str
  timer_s: int

  @property
  def is_on(self) -> bool:
    return self.lamp == 'on'


class LampController:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

  def on(self) -> list[str]:
    return self._connector.execute_command('lamp on', until=('[BEACON]', '[LAMP]', 'E50', 'E51'))

  def off(self) -> list[str]:
    return self._connector.execute_command('lamp off', until=('[BEACON]', '[LAMP]', 'W510', 'E50', 'E51'))
  
  def status_raw(self) -> list[str]:
    return self._connector.execute_command('lamp status', until=('mode', 'E003', 'E005'))

  def status(self) -> LampStatus:
    return self._parse_status(self.status_raw())

  def set_color(self, name: str) -> list[str]:
    return self._connector.execute_command(f'lamp color {name}', until=('[BEACON]', '[LAMP]', 'E50', 'E51'))

  def set_rgb(self, red: int, green: int, blue: int) -> list[str]:
    return self._connector.execute_command(f'lamp color {red} {green} {blue}', until=('[BEACON]', '[LAMP]', 'E50', 'E51'))

  def set_brightness(self, brightness: int) -> list[str]:
    return self._connector.execute_command(f'lamp brightness {brightness}', until=('[BEACON]', '[LAMP]', 'E50', 'E51'))

  def set_mode(self, mode: str) -> list[str]:
    return self._connector.execute_command(f'lamp mode {mode}', until=('[BEACON]', '[LAMP]', 'E50', 'E51'))

  def set_timer(self, seconds: int) -> list[str]:
    return self._connector.execute_command(f'lamp timer {seconds}', until=('[BEACON]', '[LAMP]', 'E50', 'E51'))

  def save_scene(self, scene: int) -> list[str]:
    return self._connector.execute_command(f'lamp scene save {scene}', until=('[BEACON]', '[LAMP]', 'E50', 'E51'))

  def load_scene(self, scene: int) -> list[str]:
    return self._connector.execute_command(f'lamp scene load {scene}', until=('[BEACON]', '[LAMP]', 'E50', 'E51'))

  def execute(self, subcommand: str) -> list[str]:
    """Execute a raw lamp subcommand for protocol-level validation."""
    # Keep a generic escape hatch for protocol-level negative tests such as
    # `lamp blabla` without exposing the UART connector to the test layer.
    return self._connector.execute_command(f'lamp {subcommand}', until=('E50', 'E51', '[BEACON]', '[LAMP]'))  

  # region Service Methods

  def _parse_status(self, response: list[str]) -> LampStatus:
    payload = None

    for line in response:
      line = line.strip()

      if not line.startswith('{'):
        continue

      try:
        candidate = json.loads(line)
      except json.JSONDecodeError as exc:
        raise ResponseParseError(
          f'Lamp status contains invalid JSON: {line}'
        ) from exc

      if isinstance(candidate, dict) and candidate.get('lamp') in ('on', 'off'):
        payload = candidate
        break

    if payload is None:
      # fw_7 documents a text status, not the fw_1.x JSON contract.
      text = '\n'.join(response)
      state = re.search(r'\b(ON|off)\b\s*,?\s*color', text, re.I)
      rgb = re.search(r'color\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', text, re.I)
      bright = re.search(r'brightness\s*:?\s*(\d+)\s*%', text, re.I)
      mode = re.search(r'mode\s*:?\s*(solid|blink|breathe|rainbow)\b', text, re.I)
      timer = re.search(r'timer\s*:?\s*(\d+)\s*s\s*(?:left)?', text, re.I)
      if not (state and rgb and bright and mode):
        raise ResponseParseError(f'Lamp status format was not recognized: {response}')
      return LampStatus(
        lamp=state.group(1).lower(),
        color=tuple(int(n) for n in rgb.groups()),
        brightness=int(bright.group(1)),
        mode=mode.group(1).lower(),
        timer_s=int(timer.group(1)) if timer else 0,
      )

    required_fields = ('lamp', 'color', 'brightness', 'mode', 'timer_s')
    missing_fields = [field for field in required_fields if field not in payload]

    if missing_fields:
      raise ResponseParseError(
        f'Lamp status is missing fields {missing_fields}: {payload}'
      )

    color = payload['color']

    if (
      not isinstance(color, list)
      or len(color) != 3
      or not all(isinstance(value, int) for value in color)
    ):
      raise ResponseParseError(f'Invalid lamp color in status: {color}')

    brightness = payload['brightness']
    mode = payload['mode']
    timer_s = payload['timer_s']

    if not isinstance(brightness, int):
      raise ResponseParseError(f'Invalid lamp brightness in status: {brightness}')

    if not isinstance(mode, str):
      raise ResponseParseError(f'Invalid lamp mode in status: {mode}')

    if not isinstance(timer_s, int):
      raise ResponseParseError(f'Invalid lamp timer in status: {timer_s}')

    return LampStatus(
      lamp=payload['lamp'],
      color=tuple(color),
      brightness=brightness,
      mode=mode,
      timer_s=timer_s,
    )

  # endregion
