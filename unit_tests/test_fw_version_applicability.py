import ast
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest
from packaging.version import Version


ROOT = Path(__file__).resolve().parents[1]


def load_fixtures():
  spec = importlib.util.spec_from_file_location('fw_version_fixtures', ROOT / 'tests' / 'conftest.py')
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


@pytest.mark.parametrize(('case', 'version'), [
  ('TC-OTA-007', '2.3.0'), ('TC-OTA-008', '2.3.0'),
  ('TC-OTA-017', '2.3.0'), ('TC-OTA-034', '2.3.0'),
  ('TC-OTA-046', '2.3.0'), ('TC-OTA-053', '2.3.0'),
  ('TC-OTA-015', '2.1.0'), ('TC-OTA-016', '2.1.0'),
  ('TC-OTA-042', '2.1.0'), ('TC-OTA-043', '2.1.0'),
  ('TC-OTA-045', '2.1.0'),
])
def test_version_restricted_cases_have_correct_marker(case, version):
  markers = []
  for source in (ROOT / 'tests' / 'ota').glob('test_*.py'):
    for node in ast.parse(source.read_text(encoding='utf-8')).body:
      if not isinstance(node, ast.FunctionDef):
        continue
      tc = False
      restricted = None
      for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call):
          continue
        if not isinstance(decorator.func, ast.Attribute):
          continue
        if decorator.func.attr == 'tc' and decorator.args[0].value == case:
          tc = True
        if decorator.func.attr == 'fw_only':
          restricted = decorator.args[0].value
      if tc:
        markers.append(restricted)
  assert markers == [version], (case, markers)


@pytest.mark.parametrize(('actual', 'required', 'should_skip'), [
  ('2.1.0', '2.3.0', True),
  ('2.3.0', '2.1.0', True),
  ('2.1.0', '2.1.0', False),
  ('2.3.0', '2.3.0', False),
])
def test_version_guard_skips_only_incompatible_firmware(actual, required, should_skip):
  fixtures = load_fixtures()
  marker = SimpleNamespace(args=[required])
  node = SimpleNamespace(get_closest_marker=lambda name: marker if name == 'fw_only' else None)
  request = SimpleNamespace(node=node, getfixturevalue=lambda name: Version(actual))
  check = fixtures.check_firmware_version.__wrapped__

  if should_skip:
    with pytest.raises(pytest.skip.Exception, match=f'Requires firmware == {required}'):
      check(request)
    assert node._fw_version_skip is True
  else:
    check(request)
    assert not hasattr(node, '_fw_version_skip')


def test_version_detection_uses_driver_without_lamp_state_fixture():
  fixtures = load_fixtures()
  device = SimpleNamespace(version=lambda: [
    'SENTRY SWM-2 sonar watch module, fw v2.3.0 (build 2026-10-20)',
  ])
  assert fixtures.firmware_version.__wrapped__(device) == Version('2.3.0')


def test_expected_firmware_skip_does_not_abort_ota_gatekeeper():
  fixtures = load_fixtures()
  session = SimpleNamespace(shouldstop=None)
  item = SimpleNamespace(
    session=session,
    _fw_version_skip=True,
    get_closest_marker=lambda name: True if name == 'ota_gatekeeper' else None,
  )
  hook = fixtures.pytest_runtest_makereport(item, None)
  next(hook)
  with pytest.raises(StopIteration):
    hook.send(SimpleNamespace(get_result=lambda: SimpleNamespace(failed=False, skipped=True)))
  assert session.shouldstop is None


def test_unexpected_gatekeeper_skip_still_aborts():
  fixtures = load_fixtures()
  session = SimpleNamespace(shouldstop=None)
  item = SimpleNamespace(
    nodeid='tests/ota/test_02_install.py::test_forced_downgrade',
    session=session,
    get_closest_marker=lambda name: True if name == 'ota_gatekeeper' else None,
  )
  hook = fixtures.pytest_runtest_makereport(item, None)
  next(hook)
  with pytest.raises(StopIteration):
    hook.send(SimpleNamespace(get_result=lambda: SimpleNamespace(failed=False, skipped=True, outcome='skipped')))
  assert 'Gatekeeper failed' in session.shouldstop
