# SENTRY SWM-2 fw_7 — Bug–Requirement Matrix

**Firmware versions:** Stable **2.1.0**, Beta **2.3.0**. **Basis:** [confirmed bug reports](BUG_REPORTS.md), [full raw logs](LOGS.md), [test checklist](../CHECK_LIST.md), and `poe full_cycle` screenshots. This document replaces the obsolete matrix for firmware 1.3.0–1.5.0.

Only issues supported by firmware UART behavior and a specific PRD requirement are classified as **confirmed firmware bugs**. Failing pytest items requiring manual validation are listed separately, without Bug IDs.

## Confirmed firmware defects mapped to PRD

| PRD | Expected behavior | Confirmed Bug ID | Checklist TC | Stable 2.1.0 | Beta 2.3.0 | Severity / Priority | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **LM-5** | `lamp timer N` interprets N as seconds and reports `auto-off in N s` | [BUG-FW7-002](BUG_REPORTS.md) | `TC-LAMP-019`, `TC-LAMP-021` | **CONFIRMED**: prints `ms` for `1`, `2`, `3600` (3/3 checked values in one run) | Matching automation PASS; not manually checked | Minor / P2 (displayed units only) | [UART and pytest](LOGS.md), [report](BUG_REPORTS.md) |
| **OTA-4** | Same-version `ota update` without `force` must return `already up to date`, with no download, flash write or reboot | [BUG-FW7-005](BUG_REPORTS.md) | `TC-OTA-005` (`stable` parameter) | **CONFIRMED**: forced reinstall-like behavior without `force`, observed twice | **NOT CONFIRMED on 2.3.0**: beta-stage test first changed DUT to 2.1.0 | Major / P1 | [UART and pytest](LOGS.md), [report](BUG_REPORTS.md) |

**Scope:** BUG-FW7-002 proves a wrong text unit, **not** that the timer internally expires in milliseconds. BUG-FW7-005 is attributable to the **running DUT firmware 2.1.0** in both observations.

## Failed automated checks pending triage — not filed as firmware bugs

| PRD | Verification ID | Checklist / test | Observation / stage | Why it is not yet confirmed | Required next check |
| --- | --- | --- | --- | --- | --- |
| **WF-4**, potential **AC-1** access interaction | `VERIFY-FW7-001` | `TC-WIFI-025` / `test_time_unavailable_before_first_ntp_sync` | 2.1.0 clean first-stage: `E002 Wi-Fi required`, test expected `E121`; 1/1 failed | Access restriction may take precedence over unsynchronized-time error | Inspect `help` `[wifi]` marker; compare disconnected vs connected-but-NTP-blocked `time` responses on 2.1.0 and 2.3.0 |
| **OTA-10**, **AU-5** (account persistence) | `VERIFY-FW7-002` | `TC-OTA-042` / `test_changed_password_persists_upgrade_downgrade_rollback` | 2.1.0 suite, after 2.1.0 → 2.3.0 upgrade: `login_ok=False`, `whoami=not logged in`; 1/1 failed | Raw `login` reply and device readiness are missing; failure occurred during an OTA transition | Verify password change works before OTA; after upgrade capture raw redacted `login`, version, status and `whoami` |
| **WF-4** | `VERIFY-FW7-003` | `TC-WIFI-008` / `test_scan_includes_reference_ssid_and_rssi` | Timeout in both 2.1.0 and 2.3.0 (2/2 stages), **but UART listed 19/20 networks** | `BuoyController.scan()` waits for `networks:` or `E108`; no such terminator appears; likely a framework response-completion problem | Run raw `scan` and follow immediately with `help` on both versions; correct parser if output valid |
| **OTA-9** | `VERIFY-FW7-004` | `TC-OTA-035` / `test_concurrent_ota_rejected` | E401 not observed in either suite (2/2 stages); first OTA completed | Logs say `command_echo_seen=False`: second command might never have reached firmware | Verify real UART injection during active download, capture second-command echo and first OTA state |

For exact, reproducible manual steps, see [Manual verification plan](MANUAL_VERIFICATION_FW7.md). These four groups **must not** be counted as additional confirmed firmware bugs.

## Related validation of confirmed defects

| PRD | Checklist | Scope to check | Status |
| --- | --- | --- | --- |
| LM-5 | `TC-LAMP-019`, `TC-LAMP-021` | Measure **actual** lamp timer duration and output unit in both firmware versions | 2.1.0 displayed-unit defect confirmed; physical timing not established |
| OTA-4 | `TC-OTA-005` (`beta` parameter) | With **2.3.0 still installed**, execute same-version `ota update beta` without `force`; check for no reboot | Not established by the failed beta-stage `stable` parameter |

## Execution and applicability context

| Stage | PASS items | FAIL items | SKIPPED items | Deselected items |
| --- | ---: | ---: | ---: | ---: |
| 2.1.0 first | 4 | 1 | 0 | 137 |
| 2.1.0 suite | 120 | 7 | 5 | 10 |
| 2.3.0 suite | 123 | 3 | 6 | 10 |

OTA gatekeepers: **4 PASS on 2.1.0**, **1 PASS on 2.3.0** (separate screenshot evidence). All three above main/first stages have failures; the total across those stages is **247 PASS, 11 FAIL, 11 SKIPPED**. Items executed in multiple stages are not unique test cases, and three timer-related failures are mapped to a single confirmed bug.

**Manual system CLI (Stable 2.1.0):** user-reported PASS for all 15 `TC-SYSTEM-001`–`TC-SYSTEM-015` cases, without device execution logs attached. Beta CLI manual results are not reported.

## Source documents

- [Full-cycle report](REPORT.md)
- [Confirmed firmware bug reports](BUG_REPORTS.md)
- [UART command logs and complete pytest failures](LOGS.md)
- [Manual verification plan](MANUAL_VERIFICATION_FW7.md)
- [Checklist and per-firmware results](../CHECK_LIST.md)
