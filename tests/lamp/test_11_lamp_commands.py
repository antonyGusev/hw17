import re

import pytest


@pytest.mark.tc('TC-LAMP-034')
@pytest.mark.regression
@pytest.mark.negative
def test_reject_unknown_lamp_command(lamp_device):
  before = lamp_device.lamp.status()
  response = '\n'.join(lamp_device.lamp.execute('blabla'))
  assert 'unknown' in response.lower() or re.search(r'\bE\d{3}\b', response), response
  assert lamp_device.lamp.status() == before
