import re

from lib import UARTConnector


class AuthController:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

  def register(self, login: str, password: str) -> bool:
    response = self._connector.execute_command(f'register {login} {password}')

    # fw_7 does not specify a fixed registration-success message. The caller
    # confirms success by logging in and checking the documented whoami output.
    return bool(response) and not any(re.search(r'\bE\d{3}\b', line) for line in response)

  def login(self, login: str, password: str) -> bool:
    response = self._connector.execute_command(f'login {login} {password}')

    if any(re.search(r'\bE20[679]\b|\bE210\b', line) for line in response):
      return False

    # fw_7 specifies whoami, but not a fixed success message for login.
    whoami = '\n'.join(self.whoami())
    return bool(re.search(rf'user:\s*{re.escape(login)}(?:,|\s)', whoami))

  def whoami(self) -> list[str]:
    return self._connector.execute_command(
      'whoami', until=('user:', 'not logged in', 'E003'), timeout=5,
    )
