# SENTRY SWM-2 (fw_7) — Confirmed Firmware Bug Reports

**Basis:** firmware matrix failure log (stages `2.1.0: first`, `2.1.0: suite`, `2.3.0: suite`) and SENTRY SWM-2 PRD. Only behavior directly contradicted by a PRD requirement and demonstrated in device UART output is included. Severity/Priority are suggested triage values. No tickets have been submitted to an issue tracker.

---

## BUG-FW7-002 — `lamp timer` reports milliseconds instead of seconds

| Field | Value |
| --- | --- |
| Firmware found | **2.1.0 (Stable)** |
| Other version | **2.3.0:** not confirmed; no direct device response from 2.3.0 provided for these commands |
| Severity | **Minor** for incorrect message/units only |
| Priority | **P2** |
| Requirement | **LM-5** — `lamp timer <1-3600>` is in seconds; message must be `[BEACON] auto-off in N s`; `lamp status` shows `timer N s left` |
| Checklist / tests | `TC-LAMP-019` → `tests/lamp/test_06_lamp_timer.py::test_timer_expires_and_turns_lamp_off`; `TC-LAMP-021` → `test_timer_accepts_boundary_values[1]` and `[3600]` |

**Preconditions:** FW 2.1.0, Wi-Fi connected, account logged in, lamp switched ON. UART console accessible.

**Steps to reproduce:**
1. Execute `lamp timer 2` and capture the entire UART response.
2. Cancel/reset the timer as needed, then execute `lamp timer 1` and capture the response.
3. Cancel/reset again, execute `lamp timer 3600`, and capture the response.
4. Compare the reported units with PRD LM-5.

**Expected:** `[BEACON] auto-off in 2 s`, `[BEACON] auto-off in 1 s`, and `[BEACON] auto-off in 3600 s` respectively.

**Actual:** firmware explicitly prints `ms` for all three values, contrary to LM-5.

**Evidence — UART fragments:**

```text
lamp timer 2
I (71343) sentry: [BEACON] auto-off in 2 ms

lamp timer 1
I (78093) sentry: [BEACON] auto-off in 1 ms

lamp timer 3600
I (79543) sentry: [BEACON] auto-off in 3600 ms
```

**Photo / video:** Not provided. The mismatch is directly shown in UART messages.

**Reproducibility:** **3/3 checked input values in one test run** on FW 2.1.0. This is *not* 3 independent test runs.

**Scope restriction:** This report confirms **incorrect units in the status message only**. The failed assertions prevented observing the actual expiration delay. Do not claim the timer internally uses milliseconds without a stopwatch/HIL check. Follow-up `VERIFY-FW7-005` covers timing and FW 2.3.0.

---

## BUG-FW7-005 — `ota update` reinstalls the already installed stable image without `force`

| Field | Value |
| --- | --- |
| Firmware found | **2.1.0 (Stable)**, observed twice |
| Other version | **2.3.0:** not established; the second failing test occurred during the beta suite but the DUT had been switched to 2.1.0 before the command |
| Severity | **Major** — unintended flash write and device reboot |
| Priority | **P1** |
| Requirement | **OTA-4** — when the selected channel already matches the installed version, log `[OTA] already up to date`, do not download, write flash, or reboot. Compare **OTA-5**, where explicit force reinstall is allowed and logs W409 |
| Checklist / test | `TC-OTA-005` → `tests/ota/test_03_update.py::test_channel_up_to_date_no_reboot[stable]` |

**Preconditions:** Device firmware v2.1.0, `stable.txt` resolves to v2.1.0; network and OTA server accessible. Run the command **without `force`**.

**Steps to reproduce:**
1. Execute `version` and confirm current firmware is v2.1.0.
2. Execute `ota check` or inspect the configured stable channel and confirm it is v2.1.0.
3. Execute `ota update` (no `force`).
4. Capture the UART messages and observe whether the image downloads, the inactive partition is written, and the device reboots.

**Expected (OTA-4):** Message `[OTA] already up to date`; **no** image download, flash write, or reboot.

**Actual:** Firmware downloads v2.1.0 again, writes the inactive partition, logs `W409` for a same-version reinstall, and reboots even though `force` was not specified.

**Evidence — two independent failing executions on actual FW 2.1.0:**

```text
# 2.1.0 suite
[OTA] stable channel: v2.1.0, current: v2.1.0
[OTA] current v2.1.0 (ota_1) -> target partition ota_0
[OTA] downloading http://192.168.68.109:8000/fw7/v2.1.0/sentry_fw7.bin
W409 same version v2.1.0 - reinstalling
[OTA] success: v2.1.0 -> v2.1.0 in 22 s. Rebooting...

# beta-suite stage, DUT actually v2.1.0 at time of command
[OTA] stable channel: v2.1.0, current: v2.1.0
[OTA] current v2.1.0 (ota_0) -> target partition ota_1
[OTA] downloading http://192.168.68.109:8000/fw7/v2.1.0/sentry_fw7.bin
W409 same version v2.1.0 - reinstalling
[OTA] success: v2.1.0 -> v2.1.0 in 14 s. Rebooting...
```

**Photo / video:** Not provided. Full OTA transfer/reboot is captured in the supplied UART logs.

**Reproducibility:** **2/2 executions on actual FW 2.1.0**, in two suite stages. No confirmed 2.3.0 reproduction.

**Scope restriction:** Do not claim `ota update beta` performs a no-op incorrectly on v2.3.0 unless tested on that running firmware. Follow-up `VERIFY-FW7-006` covers this.

---

**Disposition:** The four other failure groups are **NOT confirmed firmware defects** and are listed in `MANUAL_VERIFICATION_FW7.md`. Existing candidate IDs `BUG-FW7-001`, `003`, `004`, `006` should not be filed as firmware bugs based on the current evidence.
