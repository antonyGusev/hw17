"""The dispatcher must not require a reporter that is not selected."""

import subprocess
import sys
from pathlib import Path
from shutil import copytree

import pytest


@pytest.mark.parametrize('reporter, removed', [
  ('console', 'allure_logger.py'),
  ('allure', 'console_logger.py'),
])
def test_selected_reporter_works_without_the_other(tmp_path, reporter, removed):
  source = Path(__file__).resolve().parents[1]/'lib/utilities/logger'
  destination = tmp_path/'logger'
  copytree(source, destination, ignore=lambda _, names: {'__pycache__'} & set(names))
  (destination/removed).unlink()

  script = '''
import os
import sys
import types
from contextlib import nullcontext

os.environ['STEP_LOG_REPORTER'] = sys.argv[1]
os.environ['STEP_LOG_LEVEL'] = 'silent'

fake_allure = types.ModuleType('allure')
fake_allure.step = lambda title: nullcontext()
fake_allure.attach = lambda *args, **kwargs: None
sys.modules['allure'] = fake_allure

from logger import log_step

@log_step
def ping(number):
  return number + 1

assert ping(41) == 42
'''
  result = subprocess.run([sys.executable, '-c', script, reporter], cwd=tmp_path, capture_output=True, text=True, timeout=10)
  assert result.returncode == 0, result.stderr
