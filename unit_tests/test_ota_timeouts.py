import pytest

from framework.device.controllers.ota_controller import OtaController


class FakeConnector:
  def __init__(self, response):
    self.response = response
    self.calls = []

  def execute_command(self, command, until=None, timeout=None):
    self.calls.append((command, until, timeout))
    return self.response


@pytest.mark.parametrize('method,args,expected_timeout', [
  ('install', ('2.3.0',), 120),
  ('update', (), 120),
  ('url', ('https://example.test/fw.bin',), 120),
  ('broken', (), 120),
  ('rollback', (), 30),
])
def test_default_timeout_is_bounded(method, args, expected_timeout):
  connector = FakeConnector(['E414 invalid request'])
  getattr(OtaController(connector), method)(*args)
  assert connector.calls[0][2] == expected_timeout
  assert 'E414' in connector.calls[0][1]


def test_negative_command_can_use_short_timeout():
  connector = FakeConnector(['E414 invalid version'])
  OtaController(connector).install('abc', timeout=10)
  assert connector.calls[0][2] == 10


def test_access_errors_are_terminal():
  connector = FakeConnector(['E003 login required'])
  OtaController(connector).install('2.3.0')
  assert 'E003' in connector.calls[0][1]
  assert 'E002' in connector.calls[0][1]
