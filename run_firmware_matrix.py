"""Run the fw_7 HIL matrix: 2.1.0 stable -> 2.3.0 beta.

Full flash: python run_firmware_matrix.py
Already flashed with 2.1.0: python run_firmware_matrix.py --no-flash
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

from packaging.version import Version

from framework import DeviceDriver
from lib import (
  SERVER_MANAGED_ENV,
  UARTConnector,
  find_device_port,
  ota_success,
  read_firmware,
  require_login,
  running_ota_server,
  wait_boot,
)

ROOT = Path(__file__).resolve().parent
VERSIONS = (Version('2.1.0'), Version('2.3.0'))



FAILURE_REPORTS = []
ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')


def print_failure_reports() -> None:
  if not FAILURE_REPORTS:
    return

  print('\n=== Pytest failure reports (all firmware stages) ===', flush=True)
  for label, report in FAILURE_REPORTS:
    print(f'\n=== {label} ===', flush=True)
    print(report, end='\n' if not report.endswith('\n') else '', flush=True)


def run_pytest(label: str, args: list[str], allow_failures: bool = True) -> bool:
  print(f'\n=== {label} ===', flush=True)
  process = subprocess.Popen(
    [sys.executable, '-m', 'pytest', '--color=yes', '-rs', *args],
    cwd=ROOT,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    errors='replace',
    bufsize=1,
  )

  report_lines = []
  collecting_report = False
  assert process.stdout is not None
  for line in process.stdout:
    if re.match(r'^=+ (FAILURES|ERRORS|short test summary info) =+', ANSI_ESCAPE.sub('', line)):
      collecting_report = True
    if collecting_report:
      report_lines.append(line)
    else:
      print(line, end='', flush=True)

  returncode = process.wait()
  if report_lines:
    report = ''.join(report_lines)
    skipped = [
      line for line in report.splitlines() if re.match(r'^SKIPPED\s+', ANSI_ESCAPE.sub('', line))
    ]
    if skipped:
      print(f'\nSkipped tests in {label}:', flush=True)
      for line in skipped:
        print(line, flush=True)
    FAILURE_REPORTS.append((label, report))
  if returncode == 0:
    return True
  if returncode == 1 and allow_failures:
    summary = re.findall(r'\b(\d+) failed\b', ANSI_ESCAPE.sub('', ''.join(report_lines)))
    count = f'{summary[-1]} FAILED tests' if summary else 'FAILED tests'
    print(f'{count} in {label}; continuing to collect results.', flush=True)
    return False
  raise RuntimeError(f'{label}: pytest exited with code {returncode}')


def get_version() -> Version:
  connector = UARTConnector(find_device_port())
  connector.open()
  try:
    device = DeviceDriver(connector)
    current, _, state = read_firmware(device)
    assert state.lower() == 'valid', f'Firmware {current} state is {state}'
    return current
  finally:
    connector.close()


def check_version(expected: Version) -> None:
  current = get_version()
  assert current == expected, f'Expected firmware {expected}, got {current}'


def install_version(expected: Version, target: Version) -> None:
  print(f'\n=== OTA {expected} -> {target} ===', flush=True)
  connector = UARTConnector(find_device_port())
  connector.open()
  try:
    device = DeviceDriver(connector)
    current, _, state = read_firmware(device)
    assert current == expected, f'Expected {expected} before OTA, got {current}'
    assert state.lower() == 'valid', f'Unexpected firmware state: {state}'

    require_login(device)
    response = device.ota.install(str(target))
    ota_success(response, current, target)
    wait_boot(device)

    current, _, state = read_firmware(device)
    assert current == target, f'Expected {target} after OTA, got {current}'
    assert state.lower() == 'valid', f'Firmware {current} state is {state}'
  finally:
    connector.close()


def main(no_flash: bool = False) -> int:
  if no_flash:
    print('=== Using already flashed fw_7 v2.1.0 ===', flush=True)
  else:
    # flash_device.py validates the image *before* erasing flash.
    print('=== Full flash: fw_7 v2.1.0 ===', flush=True)
    subprocess.run([sys.executable, 'flash_device.py'], cwd=ROOT, check=True)

  check_version(VERSIONS[0])
  failed_stages = []

  # Tests tagged 'first' need the just-flashed default device state.
  if not no_flash:
    previous_flag = os.environ.get('OTA_PRISTINE_SINGLE_SLOT')
    os.environ['OTA_PRISTINE_SINGLE_SLOT'] = '1'
    try:
      if not run_pytest(f'{VERSIONS[0]}: first', ['-m', 'first']):
        failed_stages.append(f'{VERSIONS[0]}: first')
    finally:
      if previous_flag is None:
        os.environ.pop('OTA_PRISTINE_SINGLE_SLOT', None)
      else:
        os.environ['OTA_PRISTINE_SINGLE_SLOT'] = previous_flag
    check_version(VERSIONS[0])

  # Run the stable-applicable gatekeepers before the first firmware transition.
  # The beta-only downgrade gatekeeper runs after installing 2.3.0.
  run_pytest(f'{VERSIONS[0]}: OTA gatekeeper', ['-m', 'ota_gatekeeper and not fw_only'], allow_failures=False)
  check_version(VERSIONS[0])

  for index, version in enumerate(VERSIONS):
    if index:
      check_version(VERSIONS[index - 1])
      install_version(VERSIONS[index - 1], version)

    print(f'\n######## Firmware {version} ########', flush=True)
    check_version(version)

    if version == VERSIONS[1]:
      run_pytest(f'{version}: OTA gatekeeper', ['-m', 'ota_gatekeeper and fw_only'], allow_failures=False)
      check_version(version)

    # Existing pytest_collection_modifyitems orders smoke, positive regression,
    # negative regression and remaining tests exactly as in the reference project.
    if not run_pytest(f'{version}: suite', ['-m', 'not first and not ota_gatekeeper']):
      failed_stages.append(f'{version}: suite')

    # Each OTA pytest process restores its own entry firmware in fixture teardown.
    # Never silently accept a different firmware at the next matrix stage.
    check_version(version)

  print('\n=== Firmware matrix finished ===', flush=True)
  if failed_stages:
    print('Stages with failed tests:', ', '.join(failed_stages), flush=True)
    return 1
  print('All executed stages passed.', flush=True)
  return 0


if __name__ == '__main__':
  try:
    parser = argparse.ArgumentParser(description='fw_7 firmware test matrix')
    parser.add_argument('--no-flash', action='store_true', help='Start from an already flashed v2.1.0 DUT; skip first-state tests')
    args = parser.parse_args()
    with running_ota_server():
      os.environ[SERVER_MANAGED_ENV] = '1'
      try:
        sys.exit(main(no_flash=args.no_flash))
      finally:
        os.environ.pop(SERVER_MANAGED_ENV, None)
  except (AssertionError, OSError, RuntimeError, subprocess.CalledProcessError) as error:
    print(f'Runner stopped: {error}', file=sys.stderr, flush=True)
    sys.exit(2)
  finally:
    print_failure_reports()
