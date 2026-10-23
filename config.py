import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SSID = os.getenv('SSID')
PASSWORD = os.getenv('PASSWORD')

HIL_PORT = os.getenv('HIL_PORT')

OTA_INVALID_IMAGE_HEADERS = {
  '2.1.0': os.getenv('OTA_INVALID_IMAGE_HEADER_2_1_0'),
  '2.3.0': os.getenv('OTA_INVALID_IMAGE_HEADER_2_3_0'),
}

OTA_CORRUPTED_IMAGES = {
  '2.1.0': os.getenv('OTA_CORRUPTED_IMAGE_2_1_0'),
  '2.3.0': os.getenv('OTA_CORRUPTED_IMAGE_2_3_0'),
}

OTA_HTTPS_URL = os.getenv('OTA_HTTPS_URL')
OTA_HTTPS_VERSION = os.getenv('OTA_HTTPS_VERSION')

OTA_SAME_VERSION_URL = os.getenv('OTA_SAME_VERSION_URL')
OTA_MISSING_CHANNEL_SERVER = os.getenv('OTA_MISSING_CHANNEL_SERVER')
OTA_OTHER_PROJECT_IMAGE_URL = os.getenv('OTA_OTHER_PROJECT_IMAGE_URL')
OTA_DOWNLOAD_START_FAILURE_URL = os.getenv('OTA_DOWNLOAD_START_FAILURE_URL')
OTA_PRISTINE_SINGLE_SLOT = os.getenv('OTA_PRISTINE_SINGLE_SLOT')
OTA_THROTTLED_TRANSFER = os.getenv('OTA_THROTTLED_TRANSFER')
OTA_GUARD_CURRENT_PIN = os.getenv('OTA_GUARD_CURRENT_PIN')
OTA_GUARD_TEST_PIN = os.getenv('OTA_GUARD_TEST_PIN')

ROOT_DIR = Path(__file__).resolve().parent
# flash_device.py writes the image at 0x0, so this must be a merged fw_7 image.
# Supply FW7_FLASH_IMAGE if the merged binary has a different location/name.
FIRMWARE_PATH = Path(os.getenv('FW7_FLASH_IMAGE') or (
  ROOT_DIR / 'artifacts' / 'firmware' / 'device' / 'sentry_fw7_v2.1.0_merged.bin'
)).expanduser()

LAMP_DEFAULT_COLOR = 'white'
LAMP_DEFAULT_RGB = (255, 255, 255)
LAMP_DEFAULT_BRIGHTNESS = 50
LAMP_DEFAULT_MODE = 'solid'
