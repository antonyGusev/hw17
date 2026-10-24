"""Route decorated steps to the console or Allure reporter."""

import os
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import ParamSpec, TypeVar


P = ParamSpec('P')
R = TypeVar('R')


def _reporter() -> str:
  reporter = os.getenv('STEP_LOG_REPORTER', 'console').strip().lower()
  if reporter not in ('console', 'allure'):
    raise ValueError(f'Invalid STEP_LOG_REPORTER: {reporter!r}. Use console or allure.')
  return reporter


def log_step(func: Callable[P, R]) -> Callable[P, R]:
  """Use the console logger's levels or Allure's fixed verbose steps."""
  steps: dict[str, Callable[P, R]] = {}

  @wraps(func)
  def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
    selected = _reporter()
    if selected not in steps:
      # Import only the selected reporter. Either implementation can be removed
      # without affecting use of the other one.
      if selected == 'allure':
        from .allure_logger import log_step as reporter_step
      else:
        from .console_logger import log_step as reporter_step
      steps[selected] = reporter_step(func)
    return steps[selected](*args, **kwargs)

  return wrapper


def attach_artifact(path: str | Path) -> None:
  """Attach an already-saved camera artifact when Allure is selected."""
  if _reporter() == 'allure':
    from .allure_logger import attach_artifact as attach_allure_artifact
    attach_allure_artifact(path)
