# Embedded HIL Test Automation Framework

Python-based Hardware-in-the-Loop (HIL) test automation framework for testing an ESP32-S3 device.

The framework communicates with the Device Under Test (DUT) and a dedicated ESP32 HIL controller over UART. The HIL controller provides physical interaction with the DUT, including button press emulation, relay state monitoring, sensor emulation, and visual LED verification.

Computer vision is used to verify the physical WS2812 LED indication. An OV3660 camera connected to the HIL controller captures the DUT, while OpenCV-based HSV analysis dynamically detects the LED region and determines its actual color. A predefined fallback ROI is used when dynamic detection is unavailable, and camera artifacts are saved for test analysis.

The project currently covers Wi-Fi functionality, physical controls, relay behavior, sensor interaction, and WS2812 LED indication.

## Key Features

- UART communication with DUT and HIL controller
- Wi-Fi connect, disconnect, status, and scan testing
- Physical button press emulation
- Relay state monitoring
- HC-SR04 distance sensor emulation
- WS2812 LED verification using computer vision
- Dynamic LED ROI detection with fallback ROI
- HSV-based LED color analysis
- Automatic camera artifacts for test analysis
- Independent pytest fixtures for reliable test setup
- Pytest-based automated test execution

## Project Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -e .
```

### 4. Configure the environment

Create a `.env` file in the project root and provide the required test configuration.

Example:

```env
HIL_PORT=your_com_port
SSID=your_wifi_ssid
PASSWORD=your_wifi_password
HIL_CAMERA_URL=http://<hil-ip>/capture
```

## Running Tests

Run the complete regression suite:

```bash
poe regression
```

Run Wi-Fi positive tests:

```bash
poe positive_tests
```

Tests can also be executed directly with pytest:

```bash
pytest tests
```

Run a specific test:

```bash
pytest tests/wifi/test_wifi_positive.py::test_connect_using_ssid
```

Use verbose output:

```bash
pytest tests -v
```

## Project Structure

```text
project/
├── framework/
│   ├── device/
│   │   ├── controllers/
│   │   └── device_driver.py
│   │
│   └── hil/
│       ├── controllers/
│       └── hil_driver.py
│
├── lib/
│   ├── connectors/
│   │   └── uart_connector.py
│   └── utilities/
│       ├── exceptions.py
│       └── utilities.py
│
├── tests/
│   ├── wifi/
│   └── conftest.py
│
├── artifacts/
│   └── camera/
│
├── config.py
├── pyproject.toml
└── README.md
```

### `framework/device`

Contains the DUT abstraction and feature-specific controllers.

Controllers expose high-level operations such as Wi-Fi connection, disconnection, status, and scanning while hiding UART communication details from tests.

### `framework/hil`

Contains the Hardware-in-the-Loop abstraction and controllers responsible for physical interaction with the DUT.

The HIL controller provides functionality for button press emulation, hardware signal monitoring, sensor emulation, and camera-based verification.

`CameraController` handles image capture, dynamic ROI detection, HSV color analysis, and generation of camera artifacts.

### `lib`

Contains reusable low-level components shared by the framework, including:

- UART communication
- Custom framework exceptions
- Device discovery
- Polling and waiting utilities

### `tests`

Contains pytest test suites and fixtures.

Fixtures prepare the required DUT and HIL state so tests remain independent from execution order.

### `artifacts`

Contains artifacts generated during test execution.

Camera artifacts include full debug frames and detected LED regions:

These artifacts can be used to verify the selected ROI and troubleshoot computer-vision or DUT LED indication failures.

## Architecture

The framework separates DUT control from HIL interaction:

```text
                         Tests
                           │
              ┌────────────┴────────────┐
              │                         │
        DeviceDriver                HILDriver
              │                         │
      Device Controllers         HIL Controllers
              │                         │
        UARTConnector              UARTConnector
              │                         │
          ESP32-S3              ESP32 HIL Controller
             DUT                  + OV3660 Camera
```

### DUT communication

```text
Test
  ↓
DeviceDriver
  ↓
Device Controller
  ↓
UARTConnector
  ↓
ESP32-S3 DUT
```

### HIL interaction

```text
Test
  ↓
HILDriver
  ↓
HIL Controller
  ↓
UARTConnector / Camera
  ↓
ESP32 HIL Controller
  ↓
Physical DUT
```

This separation keeps test cases focused on device behavior while UART protocol handling, hardware interaction, and computer-vision processing remain encapsulated inside the framework.

## Firmware matrix (fw_7)

The same execution policy as the reference `hw16.zip` is used:
`first` (after flash) -> blocking OTA `gatekeeper` -> `2.1.0` suite ->
OTA to `2.3.0` -> `2.3.0` suite. The suite orders smoke tests first,
positive regression next, then negative regression. A gatekeeper failure or skip
stops the entire matrix; other failures are reported by stage. Firmware is
verified between stages, and OTA tests restore the firmware they started with.

| Command | Purpose |
| --- | --- |
| `poe full_cycle` | Flash the fw_7 2.1.0 merged image, then run the matrix |
| `poe full_cycle_no_flash` | Run the matrix on an already flashed 2.1.0 device (skips `first`) |
| `poe default_state_tests` | Run the `first` tests on a fresh device |
| `poe gatekeeper` | Blocking critical OTA checks |
| `poe smoke` | Smoke tests |
| `poe regression` | Regression tests |
| `poe positive_tests` | Positive tests |
| `poe negative_tests` | Negative tests |
| `poe ota` | OTA tests only, using their entry firmware as the baseline |
| `poe unit` | Framework unit tests (no DUT, HIL or OTA server) |
| `poe wifi` | Wi-Fi HIL tests excluding `first` (requires configured SSID/PASSWORD) |

**Wi-Fi coverage (fw_7):** `poe wifi` runs the standalone Wi-Fi HIL suite
excluding clean-device scenarios. TC-WIFI-020 and TC-WIFI-025 run only in the
`first` stage immediately after a full flash erase. Wi-Fi tests restore the
lab SSID using `.env` values `SSID` and `PASSWORD`; `TC-WIFI-019` intentionally
forgets NVS credentials and restores them during fixture teardown. A controlled
AP/router is still required to automate E103/E104/E105/W106/W107/E108 and
network-loss retry scenarios (TC-WIFI-026–033). Ping and post-sync time cases
(TC-WIFI-023/024) await verified fw_7 UART examples for reliable assertions.

**Flashing:** the fw_7 v2.1.0 merged binary is included at
`artifacts/firmware/device/sentry_fw7_v2.1.0_merged.bin`.
`poe full_cycle` flashes this image at offset `0x0` by default. Set
`FW7_FLASH_IMAGE` in `.env` only if an alternative path is needed.
The old `station_WiFi_v1.3.0_merged.bin` is *not* a fw_7 image and is never
used for this matrix. `poe full_cycle_no_flash` runs against a DUT already
flashed with fw_7 v2.1.0 and cannot validate factory-default `first` tests.

The `tests/lamp` suite now uses fw_7 LM-1–LM-8 command expectations and a separate
`lamp_device` fixture. Existing camera photo/video analysis is unchanged. LM-8
priority cases that need unavailable fault injection remain manual.

**HIL long press:** Flash the updated `artifacts/firmware/hil-controller/hil-controller.ino`
to the HIL ESP32 before TC-LAMP-042. The firmware supports `hold k1 1.7`
(also k2–k4; duration in seconds, 0.05–30). In Python use
`hil.buttons.hold('k1', 1.7)`; existing `hil.buttons.k1()` stays a 150 ms press.
The HIL controller releases the selected button automatically.

### Framework unit tests

Framework-only tests live in `framework_tests/`, outside the device test tree.
Run them explicitly with `poe unit` (or `pytest framework_tests`).
`poe all`, `poe regression`, `poe ota`, and the firmware matrix run only
HIL/device tests in `tests/`.

### Local OTA test server

The local server in `lib/utilities/ota_server.py` is started **once** before HIL tests
and stopped after the run (also after test failures). During `poe full_cycle` or
`poe full_cycle_no_flash`, the matrix runner keeps **one server process** alive
across all pytest stages. `poe ota`, `poe regression` and direct pytest use the
pytest session hooks. Framework unit tests in `framework_tests/` are separate
from device tests and never start the server.

On the first run, if `lib/utilities/server_files/fw7` is empty, setup runs
`ota_server.py --download` to cache stable, beta and broken images from GitHub.
This requires Internet access. The server listens on port `8000` by default;
set `OTA_SERVER_PORT` to override it. Output goes to `artifacts/ota_server.log`.
An occupied port is an error; the framework never terminates an unrelated process.

The server URL is detected at startup and printed as
`OTA server URL: http://<computer-LAN-IP>:8000/fw7/`. It is automatically
shared with pytest stages through `OTA_TEST_SERVER` in the process environment;
`tests/ota/test_10_server.py` gets it from the session fixture `ota_server_url`.
Do not configure a static `OTA_TEST_SERVER` in `.env`. The ESP32 must be able
to reach the detected LAN IP. Starting the server does **not** implicitly
change the DUT's configured OTA source; the relevant tests configure it themselves.

### Console step logging

Every **public method** in the DUT/HIL drivers, feature controllers, camera modules,
and UART connector is annotated with `@log_step`. Constructors, private methods,
and property getters are excluded. Method signatures, return values and exception
behavior are unchanged.

Step logging is **off by default** (`silent`). Plain `poe full_cycle`, `poe wifi`,
and `poe lamp` do not emit step messages. Enable it explicitly with Poe or
`STEP_LOG_LEVEL` in the environment / `.env` (for example `STEP_LOG_LEVEL=verbose`):

```powershell
poe logged lamp --log-level debug
poe logged wifi --log-level verbose
poe logged ota --log-level warning
poe logged full_cycle --log-level error
poe logged full_cycle_no_flash --log-level silent
```

| Level | Output |
| --- | --- |
| `debug` | Full nested call chain: drivers, controllers, camera modules, UART connector |
| `verbose` | Calls, arguments and results from drivers and controllers only |
| `warning` | Firmware `W###`/`E###` results and Python exceptions from any layer |
| `error` | Firmware `E###` results and Python exceptions from any layer |
| `silent` | No step-logger messages |

Debug lines are indented according to call depth. The logger redacts common
password, PIN, token and authentication-command values; NumPy frames are
summarized by shape/dtype. `STEP_LOG_MAX_LENGTH` (default 1200) limits the
length of each logged result. Camera image/video **analysis logic is unchanged**;
only its public-method calls can now be traced in debug mode.

During pytest, step messages use pytest's live-logging handler (`log_cli` in
`pyproject.toml`), so they remain visible without `-s` even on Windows.
Outside pytest, the logger writes directly to the console. Masking is best-effort: do not return arbitrary plaintext secrets
from custom methods. Warnings and errors originating from nested calls may be
shown at more than one layer. Unhandled exceptions are re-raised unchanged.
