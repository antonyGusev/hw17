"""Shared step metadata and safe value formatting; independent of report backends."""

import inspect
import os
import re
from collections.abc import Callable

_SECRET_FIELDS = ('password', 'passwd', 'pwd', 'pin', 'token', 'secret', 'credential', 'api_key')
_SECRET_COMMAND = re.compile(r"(?i)\b(login|register|passwd|sudo)\s+([^\s'\",]+)(?:\s+([^\s'\",]+))?")
_GUARD_COMMAND = re.compile(r"(?i)\b(guard\s+(?:disarm|pin))\s+([^\s'\",]+)(?:\s+([^\s'\",]+))?")
_FIELD_VALUE = re.compile(r'(?i)\b(password|passwd|pwd|pin|token|secret|api_key)\s*[:=]\s*(\S+)')


def _redact(text: str, secrets: list[str]) -> str:
  for secret in sorted(set(secrets), key=len, reverse=True):
    if len(secret) >= 4:
      text = text.replace(secret, '***')

  text = _SECRET_COMMAND.sub(
    lambda match: f'{match.group(1)} ***' if match.group(1).lower() in ('sudo', 'passwd')
    else f'{match.group(1)} {match.group(2)} ***', text,
  )
  text = _GUARD_COMMAND.sub(
    lambda match: f'{match.group(1)} *** ***' if match.group(3) else f'{match.group(1)} ***', text,
  )
  return _FIELD_VALUE.sub(lambda match: f'{match.group(1)}=***', text)


def _display(value: object, secrets: list[str]) -> str:
  # Debugging video must not stringify complete NumPy frames into memory/logs.
  if hasattr(value, 'shape') and hasattr(value, 'dtype'):
    return f'<{type(value).__name__} shape={value.shape} dtype={value.dtype}>'
  try:
    raw = repr(value)
  except Exception:
    raw = f'<{type(value).__name__}>'
  return _redact(raw, secrets)


def _arguments(signature: inspect.Signature, args: tuple, kwargs: dict, inherited: tuple[str, ...] = ()) -> tuple[str, list[str]]:
  try:
    bound = signature.bind_partial(*args, **kwargs)
  except TypeError:
    return '<invalid arguments>', list(inherited)

  secrets = list(inherited)
  for name, value in bound.arguments.items():
    if any(field in name.lower() for field in _SECRET_FIELDS):
      secrets.append(str(value))
    elif signature.parameters[name].kind == inspect.Parameter.VAR_KEYWORD:
      for key, item in value.items():
        if any(field in key.lower() for field in _SECRET_FIELDS):
          secrets.append(str(item))

  fields = []
  for name, value in bound.arguments.items():
    if name in ('self', 'cls'):
      continue
    if any(field in name.lower() for field in _SECRET_FIELDS):
      shown = '***'
    elif signature.parameters[name].kind == inspect.Parameter.VAR_KEYWORD:
      shown = _display({key: '***' if any(f in key.lower() for f in _SECRET_FIELDS) else val for key, val in value.items()}, secrets)
    else:
      shown = _display(value, secrets)
    fields.append(f'{name}={shown}')
  return ', '.join(fields), secrets


def _method_name(func: Callable, args: tuple) -> str:
  owner = getattr(args[0], '_log_path', None) if args else None
  if isinstance(owner, str) and owner:
    return f'{owner}.{func.__name__}'
  return func.__qualname__


def _max_length() -> int:
  try:
    return max(100, int(os.getenv('STEP_LOG_MAX_LENGTH', '1200')))
  except ValueError:
    return 1200


def _layer(func: Callable) -> str:
  module = func.__module__
  if module in ('framework.device.device_driver', 'framework.hil.hil_driver'):
    return 'driver'
  if module.startswith('framework.hil.controllers.modules.'):
    return 'module'
  if module.startswith(('framework.device.controllers.', 'framework.hil.controllers.')):
    return 'controller'
  if module.startswith('lib.connectors.'):
    return 'connector'
  # Standalone/decorated test helpers keep their historical verbose behavior.
  return 'controller'


