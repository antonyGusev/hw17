"""Opt-in console steps for synchronous device and HIL driver methods."""

import inspect
import itertools
import os
import re
import sys
import time
from collections.abc import Callable
from datetime import datetime
from functools import wraps
from typing import Literal, ParamSpec, TypeVar

LogLevel = Literal['verbose', 'warning', 'error', 'silent']

P = ParamSpec('P')
R = TypeVar('R')

_STEP_NUMBERS = itertools.count(1)
_ERROR_CODE = re.compile(r'\bE\d{3}\b')
_WARNING_CODE = re.compile(r'\bW\d{3}\b')
_SECRET_FIELDS = ('password', 'passwd', 'pwd', 'pin', 'token', 'secret', 'credential', 'api_key')
_SECRET_COMMAND = re.compile(r"(?i)\b(login|register|passwd|sudo)\s+([^\s'\",]+)(?:\s+([^\s'\",]+))?")
_GUARD_COMMAND = re.compile(r"(?i)\b(guard\s+(?:disarm|pin))\s+([^\s'\",]+)(?:\s+([^\s'\",]+))?")
_FIELD_VALUE = re.compile(r'(?i)\b(password|passwd|pwd|pin|token|secret|api_key)\s*[:=]\s*(\S+)')


def _log_level() -> LogLevel:
  level = os.getenv('STEP_LOG_LEVEL', 'verbose').strip().lower()
  if level not in ('verbose', 'warning', 'error', 'silent'):
    raise ValueError(f'Invalid STEP_LOG_LEVEL: {level!r}. Use verbose, warning, error or silent.')
  return level


def _redact(text: str, secrets: list[str]) -> str:
  for secret in sorted(set(secrets), key=len, reverse=True):
    if len(secret) >= 4:
      text = text.replace(secret, '***')

  text = _SECRET_COMMAND.sub(
    lambda match: f'{match.group(1)} ***' if match.group(1).lower() in ('sudo', 'passwd')
    else f'{match.group(1)} {match.group(2)} ***', text,
  )
  text = _GUARD_COMMAND.sub(lambda match: f'{match.group(1)} ***', text)
  return _FIELD_VALUE.sub(lambda match: f'{match.group(1)}=***', text)


def _display(value: object, secrets: list[str]) -> str:
  try:
    raw = repr(value)
  except Exception:
    raw = f'<{type(value).__name__}>'
  return _redact(raw, secrets)


def _arguments(signature: inspect.Signature, args: tuple, kwargs: dict) -> tuple[str, list[str]]:
  try:
    bound = signature.bind_partial(*args, **kwargs)
  except TypeError:
    return '<invalid arguments>', []

  secrets = []
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
  # Pytest normally captures sys.stdout. Write to the original console so
  # steps stay visible during `poe lamp` and subprocess-driven `poe full_cycle`.
  stream = sys.__stdout__ or sys.stdout
  if stream is not None:
    print(f'[{datetime.now():%H:%M:%S}] {message}', file=stream, flush=True)


def log_step(func: Callable[P, R]) -> Callable[P, R]:
  """Log arguments/results; STEP_LOG_LEVEL controls output globally via env."""
  signature = inspect.signature(func)
  method = func.__qualname__

  @wraps(func)
  def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
    level = _log_level()
    if level == 'silent':
      return func(*args, **kwargs)

    number = next(_STEP_NUMBERS)
    arguments, secrets = _arguments(signature, args, kwargs)
    call = f'#{number} {method}({arguments})'
    if level == 'verbose':
      _emit(f'[STEP] {call}')

    started = time.monotonic()
    try:
      result = func(*args, **kwargs)
    except Exception as exc:
      elapsed = time.monotonic() - started
      detail = _display(exc, secrets)[:_max_length()]
      _emit(f'[ERROR] {call} -> {type(exc).__name__}: {detail} ({elapsed:.2f}s)')
      raise

    detail = _display(result, secrets)
    severity = 'ERROR' if result is False or _ERROR_CODE.search(detail) else 'WARNING' if _WARNING_CODE.search(detail) else 'OK'
    if level == 'verbose' or severity == 'ERROR' or (level == 'warning' and severity == 'WARNING'):
      elapsed = time.monotonic() - started
      _emit(f'[{severity}] {call} -> {detail[:_max_length()]} ({elapsed:.2f}s)')
    return result

  return wrapper
