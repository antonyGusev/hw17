# OTA tests — SENTRY SWM-2 (fw_7)

Run: `poe ota` or `pytest tests/ota`. Test matrix: **2.1.0 stable / 2.3.0 beta**. `ota_versions` verifies these values against `ota check` on the configured OTA server.

Configure `SSID` and `PASSWORD` for the Wi-Fi AP. After each reboot OTA tests explicitly reconnect: fw_7 does **not** autoconnect. Lamp/Relay/Health/Guard persistence tests use a dedicated `ota_qa` test profile. All OTA tests require Wi-Fi **and** login on fw_7: `ota check` returns `E003` when logged out. At first use the OTA fixture connects to Wi-Fi, runs `register ota_qa <test password>`, then `login ota_qa <test password>`. If NVS already contains this profile, registration returns E202; the fixture uses the existing profile and validates the login. After reboot/OTA it runs `reconnect` then `login` without registering again. OTA helpers restore both prerequisites before subsequent OTA commands. The gatekeeper now verifies the authenticated `ota check` path. No new credentials are required in `.env`. Because AU-1 permits only one NVS account, a DUT already registered with different credentials will **fail explicitly** rather than be wiped or silently skipped. Use a clean lab DUT for this suite.

Controlled test inputs (optional except for the auto-managed local OTA server):

- TC-OTA-022 (E406): uses the local server `/test/garbage.bin` for a non-firmware payload; no `.env` URL is required
- `OTA_CORRUPTED_IMAGE_2_1_0`, `OTA_CORRUPTED_IMAGE_2_3_0` — corrupted fw_7 image URL (E412)
- `OTA_HTTPS_URL`, `OTA_HTTPS_VERSION` — valid fw_7 image and version for HTTPS-only TC-OTA-023
- `OTA_SAME_VERSION_URL` — image with the **currently installed** firmware version
- `OTA_TEST_SERVER` — generated automatically when the local server starts; `ota_server_url` session fixture supplies the URL to tests (no `.env` setting needed)
- `OTA_OTHER_PROJECT_IMAGE_URL` — controlled E407 image from another project
- `OTA_PRISTINE_SINGLE_SLOT=1` — set automatically by `poe full_cycle` only for the post-flash `first` stage (TC-OTA-030, E416); do not put it in `.env` for ordinary runs
- TC-OTA-035 (E401): uses the local `/fw7/slow/` route (20 KB/s) and injects a second `ota install` during the first transfer; no server restart required
- TC-OTA-038 (E405): `/fw7/download-start-failure/v<version>/sentry_fw7.bin` accepts HEAD metadata but rejects GET with HTTP 503 before any firmware bytes; the normal route remains available for immediate retry. Firmware E405 mapping requires DUT verification; no `.env` URL required.
- `OTA_GUARD_CURRENT_PIN`, `OTA_GUARD_TEST_PIN` — four-digit Guard PINs for cross-version NVS retention

**Not implemented as automated tests:** TC-OTA-013 (AP outage during transfer), 040 (AP with internet unavailable), 041 (fault injection covering *every* E4xx failure class), 044 (HC-SR04 calibration/filter/alarm preservation), 047 (complete cross-feature NVS snapshot through rollback). These require controllable AP/internet, a fault-injecting OTA server, or sensor HIL support not present in the current framework. Some implemented TC IDs cover only the automatable subset of a larger checklist case (e.g. 017, 021, 043, 045, 050).

At the start of each OTA pytest session, the fixture configures the DUT to use the auto-managed local OTA server. Tests that temporarily switch servers restore this local URL in `finally`; TC-OTA-052 still checks the GitHub `default` setting during the test, but restores the local server afterward. After each OTA test, the OTA fixture checks the active firmware version and restores its starting version (forced install when needed). Tests that also modify persistent device settings retain their own configuration cleanup. The fixture does not restore an altered OTA partition when the firmware version has not changed.

`pytest --collect-only` checks test discovery only. The real UART responses, firmware transitions and timing **must be verified on fw_7 hardware** before assigning `Passed` in `CHECK_LIST.md`.

### Execution with the firmware matrix

Run `poe full_cycle` for full flash + gatekeeper + 2.1.0/2.3.0 stages, or
`poe full_cycle_no_flash` if the DUT already runs v2.1.0. Gatekeeper contains
TC-OTA-001, TC-OTA-003, TC-OTA-006 (upgrade to beta), and TC-OTA-008
(forced downgrade). The runner verifies v2.1.0 after gatekeeper and verifies
firmware at the end of every stage. Individual OTA pytest sessions use their
own starting version as the teardown baseline.
