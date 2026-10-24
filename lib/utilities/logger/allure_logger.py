"""Allure test steps and camera attachments (always verbose, no log levels)."""

import inspect
from collections.abc import Callable
from contextvars import ContextVar
from functools import wraps
from pathlib import Path
from typing import ParamSpec, TypeVar

from .common import _arguments, _display, _layer, _max_length, _method_name

try:
  import allure
except ImportError:
  allure = None

P = ParamSpec('P')
R = TypeVar('R')
_SECRETS: ContextVar[tuple[str, ...]] = ContextVar('allure_step_secrets', default=())


def _allure():
  if allure is None:
    raise RuntimeError('Allure reporting requires allure-pytest. Install project dependencies.')
  return allure


def _attach_text(name: str, value: str) -> None:
  try:
    reporter = _allure()
    reporter.attach(value[:_max_length()], name=name, attachment_type='text/plain', extension='txt')
  except Exception:
    # Reporting must not change the outcome of an actual device operation.
    pass


def log_step(func: Callable[P, R]) -> Callable[P, R]:
  """Record only driver/controller calls, including parameters and results."""
  if _layer(func) not in ('driver', 'controller'):
    return func

  signature = inspect.signature(func)

  @wraps(func)
  def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
    reporter = _allure()
    arguments, secrets = _arguments(signature, args, kwargs, _SECRETS.get())
    token = _SECRETS.set(tuple(secrets))
    try:
      with reporter.step(f'{_method_name(func, args)}({arguments})'):
        try:
          result = func(*args, **kwargs)
        except Exception as exc:
          _attach_text('Exception', f'{type(exc).__name__}: {_display(exc, secrets)}')
          raise
        _attach_text('Result', _display(result, secrets))
        return result
    finally:
      _SECRETS.reset(token)

  return wrapper


def attach_artifact(path: str | Path) -> None:
  """Attach an existing JPEG/PNG/MP4 to the current Allure test or step."""
  source = Path(path)
  if not source.is_file():
    return
  media_types = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.mp4': 'video/mp4'}
  mime_type = media_types.get(source.suffix.lower())
  if mime_type is None:
    return
  try:
    reporter = _allure()
    reporter.attach.file(str(source), name=source.name, attachment_type=mime_type, extension=source.suffix[1:])
  except Exception:
    # A reporting failure must not fail an otherwise successful camera check.
    pass
