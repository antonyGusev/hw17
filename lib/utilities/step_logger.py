"""Layer-aware console step logging for device and HIL operations."""

import inspect
import itertools
import logging
import os
import re
import sys
import time
from datetime import datetime
from contextvars import ContextVar
from functools import wraps
from typing import Callable, Literal, ParamSpec, TypeVar

LogLevel = Literal['debug', 'verbose', 'warning', 'error', 'silent']

P = ParamSpec('P')
R = TypeVar('R')

_STEP_NUMBERS = itertools.count(1)
_STEP_LOGGER = logging.getLogger('embedded.step')
_STEP_LOGGER.setLevel(logging.INFO)
_STEP_LAYERS: ContextVar[tuple[str, ...]] = ContextVar('step_layers', default=())
_STEP_SECRETS: ContextVar[tuple[str, ...]] = ContextVar('step_secrets', default=())
_ERROR_CODE = re.compile(r'\bE\d{3}\b')
_WARNING_CODE = re.compile(r'\bW\d{3}\b')
_SECRET_FIELDS = ('password', 'passwd', 'pwd', 'pin', 'token', 'secret', 'credential', 'api_key')
_SECRET_COMMAND = re.compile(r"(?i)\b(login|register|passwd|sudo)\s+([^\s'\",]+)(?:\s+([^\s'\",]+))?")
_GUARD_COMMAND = re.compile(r"(?i)\b(guard\s+(?:disarm|pin))\s+([^\s'\",]+)(?:\s+([^\s'\",]+))?")
_FIELD_VALUE = re.compile(r'(?i)\b(password|passwd|pwd|pin|token|secret|api_key)\s*[:=]\s*(\S+)')


def _log_level() -> LogLevel:
  level = os.getenv('STEP_LOG_LEVEL', 'silent').strip().lower()
  if level not in ('debug', 'verbose', 'warning', 'error', 'silent'):
    raise ValueError(f'Invalid STEP_LOG_LEVEL: {level!r}. Use debug, verbose, warning, error or silent.')
  return level


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


def _max_length() -> int:
  try:
    return max(100, int(os.getenv('STEP_LOG_MAX_LENGTH', '1200')))
  except ValueError:
    return 1200


def _emit(message: str) -> None:
  # pytest's live-logging handler owns the console while capture is active.
  # Avoid sys.__stdout__ here: it may have an invalid handle on Windows.
  line = f'[{datetime.now():%H:%M:%S}] {message}'
  if 'PYTEST_CURRENT_TEST' in os.environ:
    severity = logging.ERROR if '[ERROR]' in message else logging.WARNING if '[WARNING]' in message else logging.INFO
    try:
      _STEP_LOGGER.log(severity, line)
    except Exception:
      pass
    return

  # Outside pytest (flash, matrix runner), write directly to the console.
  # A broken console must never interrupt a device/HIL operation.
  for stream in (sys.__stdout__, sys.__stderr__, sys.stdout, sys.stderr):
    if stream is None:
      continue
    try:
      print(line, file=stream, flush=True)
      return
    except (OSError, ValueError):
      continue


def _layer(func: Callable) -> str:
  module = func.__module__
  if module in ('framework.device.device_driver', 'framework.hil.hil_driver'):
    return 'driver'
  if module.startswith('framework.hil.controllers.modules.'):
    return 'module'
  if module.startswith('framework.device.controllers.') or module.startswith('framework.hil.controllers.'):
    return 'controller'
  if module.startswith('lib.connectors.'):
    return 'connector'
  # Standalone/decorated test helpers keep their historical verbose behavior.
  return 'controller'


def log_step(func: Callable[P, R]) -> Callable[P, R]:
  """Log public methods; debug includes all layers, verbose drivers/controllers."""
  signature = inspect.signature(func)
  method = func.__qualname__
  layer = _layer(func)

  @wraps(func)
  def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
    level = _log_level()
    if level == 'silent':
      return func(*args, **kwargs)

    layers = _STEP_LAYERS.get()
    token = _STEP_LAYERS.set((*layers, layer))
    secret_token = None
    try:
      visible = level == 'debug' or (level == 'verbose' and layer in ('driver', 'controller'))
      # Only decorated driver/controller calls affect verbose indentation.
      depth = len(layers) if level == 'debug' else sum(
        item in ('driver', 'controller') for item in layers
      )
      indent = '  ' * depth if visible else ''
      number = next(_STEP_NUMBERS) if visible or level in ('warning', 'error') else None
      arguments, secrets = _arguments(signature, args, kwargs, _STEP_SECRETS.get())
      secret_token = _STEP_SECRETS.set(tuple(secrets))
      call = f'#{number} {method}({arguments})'
      prefix = f'{indent}' if visible else ''
      if visible:
        _emit(f'{prefix}[STEP] [{layer.upper()}] {call}')

      started = time.monotonic()
      try:
        result = func(*args, **kwargs)
      except Exception as exc:
        if visible or level in ('warning', 'error'):
          elapsed = time.monotonic() - started
          detail = _display(exc, secrets)[:_max_length()]
          _emit(f'{prefix}[ERROR] [{layer.upper()}] {call} -> {type(exc).__name__}: {detail} ({elapsed:.2f}s)')
        raise

      if visible or level in ('warning', 'error'):
        detail = _display(result, secrets)
        severity = 'ERROR' if result is False or _ERROR_CODE.search(detail) else 'WARNING' if _WARNING_CODE.search(detail) else 'OK'
        if visible or severity == 'ERROR' or (level == 'warning' and severity == 'WARNING'):
          elapsed = time.monotonic() - started
          _emit(f'{prefix}[{severity}] [{layer.upper()}] {call} -> {detail[:_max_length()]} ({elapsed:.2f}s)')
      return result
    finally:
      if secret_token is not None:
        _STEP_SECRETS.reset(secret_token)
      _STEP_LAYERS.reset(token)

  return wrapper
