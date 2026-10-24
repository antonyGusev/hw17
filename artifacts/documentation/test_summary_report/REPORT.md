# SENTRY SWM-2 (fw_7) — Firmware 2.1.0 / 2.3.0 Test Report

**Project:** `hw17` — ESP32-S3 HIL test automation  
**Command:** `poe full_cycle` → `python run_firmware_matrix.py`  
**Firmware matrix:** full flash **2.1.0 (Stable)** → clean-device `first` tests → 2.1.0 OTA gatekeeper → 2.1.0 suite → OTA upgrade to **2.3.0 (Beta)** → beta gatekeeper → 2.3.0 suite  
**Environment (shown in screenshots):** Windows, Python 3.11.4, pytest 9.1.1, ESP32-S3 rev. v0.2, COM4, HIL and UART, local OTA server on port 8000.  
**Execution date:** not independently confirmed in the provided logs.  
**Sources:** [matrix failures and manual UART evidence](LOGS.md), [checklist](../CHECK_LIST.md), [confirmed bugs](BUG_REPORTS.md), [bug–requirement matrix](BUG_REQUIREMENTS_MATRIX.md), screenshots under `screenshots/`.

## 1. Executive summary

**Release recommendation: NO-GO for accepting fw_7 as fully validated.** The suite reports 11 failing pytest items across the initial and two main stages. Of those failures, **two distinct firmware deviations** have direct evidence against the PRD:

- [BUG-FW7-002](BUG_REPORTS.md) — **LM-5**: `lamp timer` reports `ms` instead of `s` on firmware 2.1.0; actual timer duration is not yet proven wrong.
- [BUG-FW7-005](BUG_REPORTS.md) — **OTA-4**: on firmware 2.1.0, same-version `ota update` **without `force`** downloads, rewrites flash, and reboots. This is a major release risk.

**Four more groups of automated failures remain unconfirmed as firmware defects**: clean-state `time`, post-upgrade login persistence, Wi-Fi `scan` completion, and concurrent OTA E401. They require the targeted manual checks in the [verification plan](MANUAL_VERIFICATION_FW7.md). In particular, the failed Wi-Fi scan may be a framework parsing issue, and the concurrent OTA test did not observe an echo of the second command.

Although beta-stage automated results are stronger than those on stable, the suite still fails and beta-only functions such as Guard/Alert/K4 are not fully covered by automation; the checklist contains outstanding manual cases. No blanket claim of all-requirement pass is supported.

## 2. Actual matrix execution

### Pytest results from the supplied terminal output

| Stage | Passed | Failed | Skipped | Deselected | Executed pass rate¹ | Duration | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| **2.1.0 — first** | 4 | 1 | 0 | 137 | 80.0% | 30.18 s | FAIL |
| **2.1.0 — suite** | 120 | 7 | 5 | 10 | 94.5% | 23m 13.75s | FAIL |
| **2.3.0 — suite** | 123 | 3 | 6 | 10 | 97.6% | 20m 41.55s | FAIL |
| **Totals (these 3 stages only)** | **247** | **11** | **11** | **157** | **95.7%** | — | **FAIL** |

¹ PASS / (PASS + FAIL), excluding skipped and deselected pytest items. Numbers count **parameterized executions**, not unique TC IDs. The project collects **142 pytest items**; each suite includes 10 deselected gatekeeper/first-only items.

### Separately executed OTA gatekeepers

| Stage | Passed | Failed | Deselected | Evidence |
| --- | ---: | ---: | ---: | --- |
| 2.1.0 OTA gatekeeper | **4** | 0 | 138 | [Screenshot](screenshots/Gatekeeper%202.1.0.png) |
| 2.3.0 OTA gatekeeper | **1** | 0 | 141 | [Screenshot](screenshots/Gatekeeper%202.3.0.png) |

These are **additional executions of already collected items**; do not add them as unique coverage. The runner reported unsuccessful stages `2.1.0: first`, `2.1.0: suite`, `2.3.0: suite` and stopped its local OTA server at the end.

### Initialization evidence

The screenshot shows that the fw_7 **2.1.0** image was erased/flashed, followed by `Hard resetting via RTS pin...`. The runner then logged `DUT is not responding. Performing HIL power cycle...` and `DUT recovered after power cycle`. This is an **observation requiring diagnosis**, not an additional confirmed firmware bug.

![2.1.0 flash and power-cycle recovery](screenshots/Flashing.png)

![Initial clean-device test execution](screenshots/Default%20states.png)

## 3. Failures by requirement and test case

| Checklist ID | PRD | Stage where test FAILED | Observation / disposition |
| --- | --- | --- | --- |
| `TC-WIFI-025` | WF-4; check AC-1 | 2.1.0 first (1 item) | `time` returned `E002` instead of test-expected `E121`; access precondition requires manual confirmation — `VERIFY-FW7-001` |
| `TC-LAMP-019`, `TC-LAMP-021` | LM-5 | 2.1.0 suite (3 items) | `auto-off in 2 ms`, `1 ms`, `3600 ms`; [**BUG-FW7-002**](BUG_REPORTS.md) confirmed for printed units only |
| `TC-OTA-042` | OTA-10, AU-5 | 2.1.0 suite (1 item; DUT upgraded to 2.3.0) | New-password login unsuccessful after upgrade; raw login reply not captured — `VERIFY-FW7-002` |
| `TC-WIFI-008` | WF-4 | Both suites (1 item each) | UART contains indexed networks + RSSI; `BuoyController.scan()` timed out awaiting `networks:` — `VERIFY-FW7-003` |
| `TC-OTA-005` (`stable`) | OTA-4 | Both suites (1 item each; DUT **2.1.0** in both) | Unexpected same-version flash and reboot — [**BUG-FW7-005**](BUG_REPORTS.md) confirmed on 2.1.0 only |
| `TC-OTA-035` | OTA-9 | Both suites (1 item each) | No E401; second-command echo missing, so command delivery not proven — `VERIFY-FW7-004` |

These six grouped rows account for **all 11 failing pytest items** (1 + 3 + 1 + 2 + 2 + 2 = 11). The four `VERIFY-FW7-*` entries are **investigations, not bug reports**. See the [matrix](BUG_REQUIREMENTS_MATRIX.md) for requirements traceability and the [complete failure output](LOGS.md) for evidence.

**Firmware attribution warning:** `TC-OTA-005[stable]` failed again during `2.3.0: suite`, but its test setup had already installed stable **2.1.0** on the DUT. Do **not** treat that execution as confirmation that firmware 2.3.0 contains BUG-FW7-005.

### Raw suite evidence

![2.1.0 automated suite, part 1](screenshots/Smoke%20%2B%20Regression%202.1.0%20%281%29.png)

![2.1.0 automated suite, part 2](screenshots/Smoke%20%2B%20Regression%202.1.0%20%282%29.png)

![2.1.0 automated suite, failures and skips](screenshots/Smoke%20%2B%20Regression%202.1.0%20%283%29.png)

![2.3.0 automated suite, part 1](screenshots/Smoke%20%2B%20Regression%202.3.0%20%281%29.png)

![2.3.0 automated suite, part 2](screenshots/Smoke%20%2B%20Regression%202.3.0%20%282%29.png)

![2.3.0 automated suite, failures and skips](screenshots/Smoke%20%2B%20Regression%202.3.0%20%283%29.png)

## 4. Confirmed defects, other risks, and manual verification

| Type | Count | Action |
| --- | ---: | --- |
| **Confirmed firmware defects** | **2** | Fix LM-5 displayed time units and OTA-4 same-version handling; rerun affected scenarios and regression |
| **Unconfirmed failure groups** | **4** | Perform `VERIFY-FW7-001`–`004` as described in the [manual verification plan](MANUAL_VERIFICATION_FW7.md) |
| **Additional scope checks** | **2** | Measure timer's *physical* expiration delay; rerun beta same-version `ota update beta` while actually running v2.3.0 |

**Manual System & UART CLI:** The user reported a successful manual pass of **all 15 `TC-SYSTEM-001`–`TC-SYSTEM-015` cases on firmware 2.1.0**. This is a **user-reported manual result**, not a logged automation run, and has no independently attached per-command evidence. Manual execution on firmware 2.3.0 is not reported. See the [checklist](../CHECK_LIST.md).

**Coverage caveat:** The checklist contains **305 requirement-based scenarios** with automation classification independent of execution status. Neither 142 collected pytest items nor 247 PASS executions imply 142/247 distinct requirements were completely validated. Version-inapplicable scenarios remain `N/A`, not failures.

## 5. Release recommendation and exit conditions

**NO-GO pending remediation and confirmation.** A release-ready assessment requires fixing the verified OTA-4 behavior, correcting LM-5 output units, checking physical timer accuracy, resolving/triaging the four unconfirmed failure groups (especially account persistence across 2.1.0 → 2.3.0), and rerunning impacted suites with passing results. Close the Beta gaps with requirement-based Guard, CIC Alert Center, K4 and related manual verification where automation does not exist.

The present data **does not demonstrate** that any of the four unconfirmed failures are firmware bugs or that firmware 2.3.0 performs the same-version OTA reinstall improperly.

## 6. Evidence and deliverables

- [LOGS.md](LOGS.md) — original 13-command UART transcript, consistently formatted like the first `ota` command; appended complete firmware matrix failures and skip reasons
- [BUG_REQUIREMENTS_MATRIX.md](BUG_REQUIREMENTS_MATRIX.md) — **2 confirmed bugs** mapped to requirements plus 4 verification groups
- [BUG_REPORTS.md](BUG_REPORTS.md) — original detailed reports for BUG-FW7-002 and BUG-FW7-005
- [MANUAL_VERIFICATION_FW7.md](MANUAL_VERIFICATION_FW7.md) — explicit manual verification steps and acceptance criteria
- [CHECK_LIST.md](../CHECK_LIST.md) — 305 test cases and per-firmware execution outcomes, including the user-reported manual System CLI results
- `screenshots/` — ten source images for flashing, initial tests, gatekeepers and both main suites
