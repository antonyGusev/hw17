"""WF-1/WF-2/WF-3: predictable CLI errors and recovery."""

import pytest

from config import PASSWORD, SSID


UNKNOWN_SSID = 'QA_NONEXISTENT_98AC31'
WRONG_PASSWORD = 'incorrect_qa_password_2026'


def assert_error(result, error):
  assert result.error == error, f'Expected {error}, got: {result.response}'


@pytest.mark.tc('TC-WIFI-014')
@pytest.mark.regression
@pytest.mark.negative
def test_reject_incorrect_password(wifi_disconnected):
  assert_error(wifi_disconnected.wifi.connect(SSID, WRONG_PASSWORD), 'E101')
  assert not wifi_disconnected.wifi.status().connected


@pytest.mark.tc('TC-WIFI-015')
@pytest.mark.regression
@pytest.mark.negative
def test_reject_short_password(wifi_disconnected):
  assert_error(wifi_disconnected.wifi.connect(SSID, '1234567'), 'E112')
  assert not wifi_disconnected.wifi.status().connected


@pytest.mark.tc('TC-WIFI-016')
@pytest.mark.regression
@pytest.mark.negative
def test_unknown_ssid_does_not_hang_cli(wifi_disconnected):
  assert_error(wifi_disconnected.wifi.connect(UNKNOWN_SSID, PASSWORD), 'E102')
  assert not wifi_disconnected.wifi.status().connected
  response = wifi_disconnected._connector.execute_command(
    'help', until='Commands (', timeout=10,
  )
  assert any('Commands (' in line for line in response), response


@pytest.mark.tc('TC-WIFI-017')
@pytest.mark.regression
@pytest.mark.negative
def test_connect_recovers_after_several_rejections(wifi_disconnected):
  for ssid, password, error in (
    (SSID, WRONG_PASSWORD, 'E101'),
    (SSID, '1234567', 'E112'),
    (UNKNOWN_SSID, PASSWORD, 'E102'),
  ):
    assert_error(wifi_disconnected.wifi.connect(ssid, password), error)
    assert not wifi_disconnected.wifi.status().connected

  result = wifi_disconnected.wifi.connect(SSID, PASSWORD)
  assert result.connected, result.response
  assert wifi_disconnected.wifi.status().ssid == SSID


@pytest.mark.tc('TC-WIFI-018')
@pytest.mark.regression
@pytest.mark.negative
def test_reject_empty_ssid(wifi_disconnected):
  assert_error(wifi_disconnected.wifi.connect('', PASSWORD), 'E111')
  assert not wifi_disconnected.wifi.status().connected


@pytest.mark.tc('TC-WIFI-019')
@pytest.mark.regression
@pytest.mark.positive
def test_forget_removes_saved_credentials(wifi_connected):
  device = wifi_connected
  device.wifi.forget()
  device.reboot()
  result = device.wifi.reconnect()
  assert_error(result, 'E113')
  assert not device.wifi.status().connected
  # wifi_device fixture reconnects the known lab AP on teardown.



@pytest.mark.tc('TC-WIFI-021')
@pytest.mark.regression
@pytest.mark.negative
def test_reconnect_already_connected_warns(wifi_connected):
  before = wifi_connected.wifi.status()
  result = wifi_connected.wifi.reconnect()
  assert any('W114' in line for line in result.response), result.response
  after = wifi_connected.wifi.status()
  assert after.connected and after.ssid == before.ssid and after.ip == before.ip


@pytest.mark.tc('TC-WIFI-022')
@pytest.mark.regression
@pytest.mark.negative
def test_disconnect_when_already_disconnected_warns(wifi_disconnected):
  response = wifi_disconnected._connector.execute_command(
    'disconnect', until='W115', timeout=10,
  )
  assert any('W115' in line for line in response), response
  assert not wifi_disconnected.wifi.status().connected
