"""Compatibility imports for tests written against the old Wi-Fi API."""

from .buoy_controller import (
  BuoyConnectResult as WifiConnectResult,
  BuoyController as WifiController,
  BuoyNetwork as WifiNetwork,
  BuoyStatus as WifiStatus,
)

__all__ = ['WifiConnectResult', 'WifiController', 'WifiNetwork', 'WifiStatus']
