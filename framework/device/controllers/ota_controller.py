from lib import UARTConnector


class OtaController:
  # Stop at command completion, not intermediate progress/telemetry lines.
  _ERRORS = ('E002', 'E003') + tuple(f'E{code}' for code in (401, 402, 403, 405, 406, 407, 408, 410, 411, 412, 414, 415, 416, 417, 418))
  _SUCCESS = ('[OTA] success:', '[OTA] already up to date', '[OTA] up to date')
  _STATUS_COMPLETE = ('previous', 'Previous', 'other', 'Other', 'inactive', 'Inactive', 'E002', 'E003')

  def __init__(self, connector: UARTConnector):
    self._connector = connector

  def execute(self, subcommand: str = '', until=None, timeout=60) -> list[str]:
    command = 'ota' if not subcommand else f'ota {subcommand}'
    if not subcommand and until is None:
      until = self._STATUS_COMPLETE
    return self._connector.execute_command(command, until=until, timeout=timeout)

  def status(self, until=None, timeout=10) -> list[str]:
    # OTA-2 requires a previous/inactive slot. Do not stop on command echo.
    return self.execute('status', until=self._STATUS_COMPLETE if until is None else until, timeout=timeout)

  def check(self, until=None, timeout=60) -> list[str]:
    return self.execute(
      'check',
      until=until if until is not None else (
        'update available', 'up to date (stable)', 'running newer than stable',
        *self._ERRORS,
      ),
      timeout=timeout,
    )

  def install(self, version: str, force: bool = False, until=None, timeout=120) -> list[str]:
    command = f'install {version}' + (' force' if force else '')
    return self.execute(
      command,
      until=until if until is not None else (*self._SUCCESS, *self._ERRORS),
      timeout=timeout,
    )

  def update(self, beta: bool = False, until=None, timeout=120) -> list[str]:
    return self.execute(
      'update beta' if beta else 'update',
      until=until if until is not None else (*self._SUCCESS, 'running newer than stable', *self._ERRORS),
      timeout=timeout,
    )

  def url(self, url: str, force: bool = False, until=None, timeout=120) -> list[str]:
    return self.execute(
      f'url {url}' + (' force' if force else ''),
      until=until if until is not None else (*self._SUCCESS, *self._ERRORS),
      timeout=timeout,
    )

  def broken(self, until=None, timeout=120, wait: bool = True) -> list[str] | None:
    if not wait:
      self._connector.write_command('ota broken')
      return None
    return self.execute(
      'broken',
      until=until if until is not None else (*self._SUCCESS, *self._ERRORS),
      timeout=timeout,
    )

  def rollback(self, until=None, timeout=30) -> list[str]:
    return self.execute(
      'rollback',
      until=until if until is not None else (*self._SUCCESS, 'Rebooting...', *self._ERRORS),
      timeout=timeout,
    )

  def server(self, url: str | None = None, until=None, timeout=60) -> list[str]:
    return self.execute(
      'server' + (f' {url}' if url is not None else ''),
      until=until,
      timeout=timeout,
    )
