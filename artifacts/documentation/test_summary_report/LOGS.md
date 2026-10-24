# Firmware fw_7 — UART command logs and automation evidence

The first command is `ota`; all subsequent UART commands use the same **command + fenced raw output** format. The UART output below is preserved from the provided `LOGS.md` (including unsolicited telemetry and reboot messages); formatting does not constitute a new test run. The automation failures that follow are taken from the supplied firmware-matrix terminal output.

## Manual UART command session

### 1. `ota`

```text
I (3253813) sentry: [OTA] running:  v2.1.0 in ota_0 (valid)
I (3253813) sentry: [OTA] previous: none (ota_1 is empty)
```

### 2. `ota status`

```text
I (3262843) sentry: [OTA] running:  v2.1.0 in ota_0 (valid)
I (3262843) sentry: [OTA] previous: none (ota_1 is empty)
I (3275843) sentry: [TELEMETRY #1] 18:26:40 up 00:54:35 heap 258KB rssi -64 temp 37.0C depth 42.3m hull 5.2bar batt 24.1V valve closed sonar - state NORMAL
```

### 3. `ota check`

```text
I (3364403) esp-x509-crt-bundle: Certificate validated
I (3365873) sentry: [TELEMETRY #4] 18:28:10 up 00:56:05 heap 209KB rssi -65 temp 38.0C depth 41.9m hull 5.2bar batt 24.1V valve closed sonar - state NORMAL
I (3365913) esp-x509-crt-bundle: Certificate validated
I (3366803) sentry: [OTA] current: v2.1.0
I (3366803) sentry: [OTA] stable:  v2.1.0
I (3366803) sentry: [OTA] beta:    v2.3.0
I (3366803) sentry: [OTA] up to date (stable)
```

### 4. `ota update`

```text
I (3434393) esp-x509-crt-bundle: Certificate validated
I (3435033) sentry: [OTA] stable channel: v2.1.0, current: v2.1.0
I (3435403) esp-x509-crt-bundle: Certificate validated
I (3436433) sentry: [OTA] current v2.1.0 (ota_0) -> target partition ota_1
I (3436433) sentry: [OTA] downloading https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/fw7/v2.1.0/sentry_fw7.bin
I (3436873) esp-x509-crt-bundle: Certificate validated
I (3437493) esp_https_ota: Starting OTA...
I (3437493) esp_https_ota: Writing to <ota_1> partition at offset 0x1a0000
I (3437513) sentry: [OTA] image: sentry_fw7 v2.1.0 (build Oct  6 2026 02:14:57)
W (3437513) sentry: W409 same version v2.1.0 - reinstalling
I (3439683) sentry: [OTA]  10%
I (3441403) sentry: [OTA]  20%
I (3443493) sentry: [OTA]  30%
I (3445363) sentry: [OTA]  40%
I (3447463) sentry: [OTA]  50%
I (3449103) sentry: [OTA]  60%
I (3451103) sentry: [OTA]  70%
I (3452923) sentry: [ACU] ambient noise 65 dB re 1uPa, sea state 2, water 8.1 C
I (3452983) sentry: [OTA]  80%
I (3454893) sentry: [OTA]  90%
I (3456113) sentry: [TELEMETRY #7] 18:29:40 up 00:57:35 heap 216KB rssi -67 temp 44.0C depth 42.0m hull 5.2bar batt 24.1V valve closed sonar - state NORMAL
I (3456613) sentry: [OTA] 100%
I (3456613) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=378a8h (227496) map
I (3456653) esp_image: segment 1: paddr=001d78d0 vaddr=3fc97200 size=05188h ( 20872) 
I (3456653) esp_image: segment 2: paddr=001dca60 vaddr=40374000 size=035b8h ( 13752) 
I (3456653) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9b1c0h (635328) map
I (3456743) esp_image: segment 4: paddr=0027b1e8 vaddr=403775b8 size=0fb58h ( 64344) 
I (3456753) esp_image: segment 5: paddr=0028ad48 vaddr=50000000 size=00024h (    36) 
I (3456753) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=378a8h (227496) map
I (3456783) esp_image: segment 1: paddr=001d78d0 vaddr=3fc97200 size=05188h ( 20872) 
I (3456793) esp_image: segment 2: paddr=001dca60 vaddr=40374000 size=035b8h ( 13752) 
I (3456793) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9b1c0h (635328) map
I (3456883) esp_image: segment 4: paddr=0027b1e8 vaddr=403775b8 size=0fb58h ( 64344) 
I (3456893) esp_image: segment 5: paddr=0028ad48 vaddr=50000000 size=00024h (    36) 
I (3456933) sentry: [OTA] success: v2.1.0 -> v2.1.0 in 19 s. Rebooting...
I (3457433) wifi:state: run -> init (0x0)
I (3457433) wifi:pm stop, total sleep time: 2460601380 us / 2977854905 us

I (3457433) wifi:<ba-del>idx:1, tid:0
I (3457433) wifi:<ba-del>idx:0, tid:5
I (3457433) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (3457473) wifi:flush txq
I (3457473) wifi:stop sw txq
I (3457473) wifi:lmac stop hw txq
ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d344
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Oct  6 2026 02:15:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 4MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (67) boot:  1 otadata          OTA data         01 00 0000f000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00020000 00180000
I (80) boot:  3 ota_1            OTA app          00 11 001a0000 00180000
I (87) boot: End of partition table
I (116) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=378a8h (227496) map
I (157) esp_image: segment 1: paddr=001d78d0 vaddr=3fc97200 size=05188h ( 20872) load
I (162) esp_image: segment 2: paddr=001dca60 vaddr=40374000 size=035b8h ( 13752) load
I (165) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9b1c0h (635328) map
I (282) esp_image: segment 4: paddr=0027b1e8 vaddr=403775b8 size=0fb58h ( 64344) load
I (297) esp_image: segment 5: paddr=0028ad48 vaddr=50000000 size=00024h (    36) load
I (305) boot: Loaded app from partition at offset 0x1a0000
I (305) boot: Disabling RNG early entropy source...
I (316) cpu_start: Multicore app
I (324) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (325) cpu_start: Pro cpu start user code
I (325) cpu_start: cpu freq: 160000000 Hz
I (327) app_init: Application information:
I (330) app_init: Project name:     sentry_fw7
I (334) app_init: App version:      2.1.0
I (338) app_init: Compile time:     Oct  6 2026 02:14:57
I (343) app_init: ELF file SHA256:  c9460b826...
I (348) app_init: ESP-IDF:          v6.0.1
I (351) efuse_init: Min chip rev:     v0.0
I (355) efuse_init: Max chip rev:     v0.99 
I (359) efuse_init: Chip rev:         v0.2
I (363) heap_init: Initializing. RAM available for dynamic allocation:
I (369) heap_init: At 3FCA0950 len 00048DC0 (291 KiB): RAM
I (374) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (380) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (385) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (391) spi_flash: detected chip: mxic
I (394) spi_flash: flash io: dio
W (397) spi_flash: Detected size(16384k) larger than the size in the binary image header(4096k). Using the size in the binary image header.
I (409) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (415) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (422) main_task: Started on CPU0
I (442) main_task: Calling app_main()
I (452) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (462) sentry: ==============================================
I (462) sentry:   SENTRY SWM-2  sonar watch module  fw v2.1.0
I (462) sentry:   bow sonar array / perimeter watch / CIC link
I (472) sentry: ==============================================
I (472) pp: pp rom version: e7ae62f
I (482) net80211: net80211 rom version: e7ae62f
I (492) wifi:wifi driver task: 3fced484, prio:23, stack:6656, core=0
I (492) wifi:wifi firmware version: b37c951
I (492) wifi:wifi certification version: v7.0
I (492) wifi:config NVS flash: enabled
I (502) wifi:config nano formatting: disabled
I (502) wifi:Init data frame dynamic rx buffer num: 32
I (512) wifi:Init static rx mgmt buffer num: 5
I (512) wifi:Init management short buffer num: 32
I (512) wifi:Init dynamic tx buffer num: 32
I (522) wifi:Init static tx FG buffer num: 2
I (522) wifi:Init static rx buffer size: 1600
I (532) wifi:Init static rx buffer num: 10
I (532) wifi:Init dynamic rx buffer num: 32
I (542) wifi_init: rx ba win: 6
I (542) wifi_init: accept mbox: 6
I (542) wifi_init: tcpip mbox: 32
I (542) wifi_init: udp mbox: 6
I (552) wifi_init: tcp mbox: 6
I (552) wifi_init: tcp tx win: 5760
I (552) wifi_init: tcp rx win: 5760
I (562) wifi_init: tcp mss: 1440
I (562) wifi_init: WiFi IRAM OP enabled
I (562) wifi_init: WiFi RX IRAM OP enabled
I (572) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (622) wifi:mode : sta (90:70:69:31:a6:8c)
I (622) wifi:enable tsf
I (622) sentry: [LINK] known network 'antony_g5'. Type 'reconnect' to connect
I (622) sentry: [AUTH] profile 'ant' registered
I (622) sentry: last reset: software reboot
I (632) sentry: build tag: c3VkbyBzM250cnktcjAwdA==
I (632) sentry: [HW] transducer array: 1 ch, 40 kHz, driver OK
I (642) sentry: [HW] hull penetrator seal: OK, pressure sensor: OK
W (642) sentry: [NAV] depth sensor offline (lab mode) - using simulator
I (652) sentry: [NAV] carrier: SSK 'Skat', bow sonar bay #2, depth 41.8 m
I (662) sentry: [OTA] running v2.1.0 from ota_1
W (662) sentry: [OTA] new firmware, PENDING_VERIFY - self-check...
I (702) sentry: [OTA] self-check passed, firmware marked VALID
```

### 5. `ota install 2.1.0`

```text
I (228842) esp-x509-crt-bundle: Certificate validated
I (229522) sentry: [OTA] current v2.1.0 (ota_1) -> target partition ota_0
I (229522) sentry: [OTA] downloading https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/fw7/v2.1.0/sentry_fw7.bin
I (229902) esp-x509-crt-bundle: Certificate validated
I (230572) esp_https_ota: Starting OTA...
I (230572) esp_https_ota: Writing to <ota_0> partition at offset 0x20000
I (230732) sentry: [OTA] image: sentry_fw7 v2.1.0 (build Oct  6 2026 02:14:57)
W (230732) sentry: W409 same version v2.1.0 - reinstalling
I (232732) sentry: [OTA]  10%
I (234422) sentry: [OTA]  20%
I (235852) sentry: [NAV] depth 41.7 m, heading 274, speed 2.8 kn
I (236592) sentry: [OTA]  30%
I (238532) sentry: [OTA]  40%
I (240422) sentry: [OTA]  50%
I (241812) sentry: [TELEMETRY #1] 18:33:43 up 00:04:01 heap 214KB rssi -66 temp 43.0C depth 41.7m hull 5.2bar batt 24.2V valve closed sonar - state NORMAL
I (242332) sentry: [OTA]  60%
I (244242) sentry: [OTA]  70%
I (245982) sentry: [OTA]  80%
I (248022) sentry: [OTA]  90%
I (249662) sentry: [OTA] 100%
I (249662) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
I (249692) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) 
I (249692) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) 
I (249692) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
I (249782) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) 
I (249792) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) 
I (249802) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
I (249832) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) 
I (249832) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) 
I (249832) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
I (249932) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) 
I (249932) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) 
I (249982) sentry: [OTA] success: v2.1.0 -> v2.1.0 in 19 s. Rebooting...
I (250482) wifi:state: run -> init (0x0)
I (250482) wifi:pm stop, total sleep time: 177470774 us / 231327370 us

I (250482) wifi:<ba-del>idx:1, tid:0
I (250482) wifi:<ba-del>idx:0, tid:5
I (250482) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (250542) wifi:flush txq
I (250542) wifi:stop sw txq
I (250542) wifi:lmac stop hw txq
ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d344
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Oct  6 2026 02:15:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 4MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (67) boot:  1 otadata          OTA data         01 00 0000f000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00020000 00180000
I (80) boot:  3 ota_1            OTA app          00 11 001a0000 00180000
I (87) boot: End of partition table
I (114) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
I (155) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) load
I (160) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) load
I (163) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
I (281) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) load
I (295) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) load
I (304) boot: Loaded app from partition at offset 0x20000
I (304) boot: Disabling RNG early entropy source...
I (314) cpu_start: Multicore app
I (322) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (323) cpu_start: Pro cpu start user code
I (323) cpu_start: cpu freq: 160000000 Hz
I (325) app_init: Application information:
I (329) app_init: Project name:     sentry_fw7
I (333) app_init: App version:      2.1.0
I (337) app_init: Compile time:     Oct  6 2026 02:14:57
I (342) app_init: ELF file SHA256:  c9460b826...
I (346) app_init: ESP-IDF:          v6.0.1
I (350) efuse_init: Min chip rev:     v0.0
I (354) efuse_init: Max chip rev:     v0.99 
I (358) efuse_init: Chip rev:         v0.2
I (361) heap_init: Initializing. RAM available for dynamic allocation:
I (368) heap_init: At 3FCA0950 len 00048DC0 (291 KiB): RAM
I (373) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (378) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (383) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (389) spi_flash: detected chip: mxic
I (392) spi_flash: flash io: dio
W (395) spi_flash: Detected size(16384k) larger than the size in the binary image header(4096k). Using the size in the binary image header.
I (408) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (414) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (421) main_task: Started on CPU0
I (441) main_task: Calling app_main()
I (451) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (461) sentry: ==============================================
I (461) sentry:   SENTRY SWM-2  sonar watch module  fw v2.1.0
I (461) sentry:   bow sonar array / perimeter watch / CIC link
I (471) sentry: ==============================================
I (471) pp: pp rom version: e7ae62f
I (481) net80211: net80211 rom version: e7ae62f
I (491) wifi:wifi driver task: 3fced484, prio:23, stack:6656, core=0
I (491) wifi:wifi firmware version: b37c951
I (491) wifi:wifi certification version: v7.0
I (491) wifi:config NVS flash: enabled
I (501) wifi:config nano formatting: disabled
I (501) wifi:Init data frame dynamic rx buffer num: 32
I (511) wifi:Init static rx mgmt buffer num: 5
I (511) wifi:Init management short buffer num: 32
I (511) wifi:Init dynamic tx buffer num: 32
I (521) wifi:Init static tx FG buffer num: 2
I (521) wifi:Init static rx buffer size: 1600
I (531) wifi:Init static rx buffer num: 10
I (531) wifi:Init dynamic rx buffer num: 32
I (541) wifi_init: rx ba win: 6
I (541) wifi_init: accept mbox: 6
I (541) wifi_init: tcpip mbox: 32
I (541) wifi_init: udp mbox: 6
I (551) wifi_init: tcp mbox: 6
I (551) wifi_init: tcp tx win: 5760
I (551) wifi_init: tcp rx win: 5760
I (561) wifi_init: tcp mss: 1440
I (561) wifi_init: WiFi IRAM OP enabled
I (561) wifi_init: WiFi RX IRAM OP enabled
I (571) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (621) wifi:mode : sta (90:70:69:31:a6:8c)
I (621) wifi:enable tsf
I (621) sentry: [LINK] known network 'antony_g5'. Type 'reconnect' to connect
I (621) sentry: [AUTH] profile 'ant' registered
I (621) sentry: last reset: software reboot
I (631) sentry: build tag: c3VkbyBzM250cnktcjAwdA==
I (631) sentry: [HW] transducer array: 1 ch, 40 kHz, driver OK
I (641) sentry: [HW] hull penetrator seal: OK, pressure sensor: OK
W (641) sentry: [NAV] depth sensor offline (lab mode) - using simulator
I (651) sentry: [NAV] carrier: SSK 'Skat', bow sonar bay #2, depth 41.8 m
I (661) sentry: [OTA] running v2.1.0 from ota_0
W (661) sentry: [OTA] new firmware, PENDING_VERIFY - self-check...
I (701) sentry: [OTA] self-check passed, firmware marked VALID
```

### 6. `ota update beta`

```text
I (291781) esp-x509-crt-bundle: Certificate validated
I (292671) sentry: [OTA] beta channel: v2.3.0, current: v2.1.0
I (293061) esp-x509-crt-bundle: Certificate validated
I (293891) sentry: [OTA] current v2.1.0 (ota_0) -> target partition ota_1
I (293891) sentry: [OTA] downloading https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/fw7/v2.3.0/sentry_fw7.bin
I (294311) esp-x509-crt-bundle: Certificate validated
I (294951) esp_https_ota: Starting OTA...
I (294951) esp_https_ota: Writing to <ota_1> partition at offset 0x1a0000
I (294961) sentry: [OTA] image: sentry_fw7 v2.3.0 (build Oct  6 2026 02:15:26)
I (297321) sentry: [OTA]  10%
I (298031) sentry: [TELEMETRY #3] 18:38:50 up 00:04:57 heap 213KB rssi -48 temp 41.0C depth 42.1m hull 5.2bar batt 24.2V valve closed sonar - state NORMAL
I (299301) sentry: [OTA]  20%
I (300971) sentry: [OTA]  30%
I (302981) sentry: [OTA]  40%
I (305011) sentry: [OTA]  50%
I (307001) sentry: [OTA]  60%
I (308931) sentry: [OTA]  70%
I (310751) sentry: [OTA]  80%
I (312611) sentry: [OTA]  90%
I (314411) sentry: [OTA] 100%
I (314411) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=38158h (229720) map
I (314441) esp_image: segment 1: paddr=001d8180 vaddr=3fc97200 size=05198h ( 20888) 
I (314441) esp_image: segment 2: paddr=001dd320 vaddr=40374000 size=02cf8h ( 11512) 
I (314451) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9c08ch (639116) map
I (314541) esp_image: segment 4: paddr=0027c0b4 vaddr=40376cf8 size=10418h ( 66584) 
I (314551) esp_image: segment 5: paddr=0028c4d4 vaddr=50000000 size=00024h (    36) 
I (314551) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=38158h (229720) map
I (314581) esp_image: segment 1: paddr=001d8180 vaddr=3fc97200 size=05198h ( 20888) 
I (314591) esp_image: segment 2: paddr=001dd320 vaddr=40374000 size=02cf8h ( 11512) 
I (314591) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9c08ch (639116) map
I (314681) esp_image: segment 4: paddr=0027c0b4 vaddr=40376cf8 size=10418h ( 66584) 
I (314691) esp_image: segment 5: paddr=0028c4d4 vaddr=50000000 size=00024h (    36) 
I (314731) sentry: [OTA] success: v2.1.0 -> v2.3.0 in 19 s. Rebooting...
I (315231) wifi:state: run -> init (0x0)
I (315231) wifi:pm stop, total sleep time: 89916774 us / 123443639 us

I (315231) wifi:<ba-del>idx:1, tid:0
I (315231) wifi:<ba-del>idx:0, tid:5
I (315231) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (315251) wifi:flush txq
I (315251) wifi:stop sw txq
I (315251) wifi:lmac stop hw txq
ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d344
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Oct  6 2026 02:15:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 4MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (67) boot:  1 otadata          OTA data         01 00 0000f000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00020000 00180000
I (80) boot:  3 ota_1            OTA app          00 11 001a0000 00180000
I (87) boot: End of partition table
I (116) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=38158h (229720) map
I (157) esp_image: segment 1: paddr=001d8180 vaddr=3fc97200 size=05198h ( 20888) load
I (162) esp_image: segment 2: paddr=001dd320 vaddr=40374000 size=02cf8h ( 11512) load
I (165) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9c08ch (639116) map
I (283) esp_image: segment 4: paddr=0027c0b4 vaddr=40376cf8 size=10418h ( 66584) load
I (298) esp_image: segment 5: paddr=0028c4d4 vaddr=50000000 size=00024h (    36) load
I (307) boot: Loaded app from partition at offset 0x1a0000
I (307) boot: Disabling RNG early entropy source...
I (317) cpu_start: Multicore app
I (326) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (326) cpu_start: Pro cpu start user code
I (326) cpu_start: cpu freq: 160000000 Hz
I (328) app_init: Application information:
I (332) app_init: Project name:     sentry_fw7
I (336) app_init: App version:      2.3.0
I (340) app_init: Compile time:     Oct  6 2026 02:15:26
I (345) app_init: ELF file SHA256:  ab377c338...
I (349) app_init: ESP-IDF:          v6.0.1
I (353) efuse_init: Min chip rev:     v0.0
I (357) efuse_init: Max chip rev:     v0.99 
I (361) efuse_init: Chip rev:         v0.2
I (365) heap_init: Initializing. RAM available for dynamic allocation:
I (371) heap_init: At 3FCA1360 len 000483B0 (288 KiB): RAM
I (376) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (381) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (386) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (393) spi_flash: detected chip: mxic
I (395) spi_flash: flash io: dio
W (398) spi_flash: Detected size(16384k) larger than the size in the binary image header(4096k). Using the size in the binary image header.
I (411) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (417) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (424) main_task: Started on CPU0
I (444) main_task: Calling app_main()
I (454) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (464) sentry: ==============================================
I (464) sentry:   SENTRY SWM-2  sonar watch module  fw v2.3.0
I (464) sentry:   bow sonar array / perimeter watch / CIC link
I (474) sentry: ==============================================
I (474) pp: pp rom version: e7ae62f
I (484) net80211: net80211 rom version: e7ae62f
I (494) wifi:wifi driver task: 3fced484, prio:23, stack:6656, core=0
I (494) wifi:wifi firmware version: b37c951
I (494) wifi:wifi certification version: v7.0
I (494) wifi:config NVS flash: enabled
I (504) wifi:config nano formatting: disabled
I (504) wifi:Init data frame dynamic rx buffer num: 32
I (514) wifi:Init static rx mgmt buffer num: 5
I (514) wifi:Init management short buffer num: 32
I (514) wifi:Init dynamic tx buffer num: 32
I (524) wifi:Init static tx FG buffer num: 2
I (524) wifi:Init static rx buffer size: 1600
I (534) wifi:Init static rx buffer num: 10
I (534) wifi:Init dynamic rx buffer num: 32
I (534) wifi_init: rx ba win: 6
I (544) wifi_init: accept mbox: 6
I (544) wifi_init: tcpip mbox: 32
I (544) wifi_init: udp mbox: 6
I (554) wifi_init: tcp mbox: 6
I (554) wifi_init: tcp tx win: 5760
I (554) wifi_init: tcp rx win: 5760
I (564) wifi_init: tcp mss: 1440
I (564) wifi_init: WiFi IRAM OP enabled
I (564) wifi_init: WiFi RX IRAM OP enabled
I (574) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (624) wifi:mode : sta (90:70:69:31:a6:8c)
I (624) wifi:enable tsf
I (624) sentry: [LINK] known network 'antony_g5'. Type 'reconnect' to connect
I (624) sentry: [AUTH] profile 'ant' registered
I (624) sentry: last reset: software reboot
I (634) sentry: build tag: c3VkbyBzM250cnktcjAwdA==
I (634) sentry: [HW] transducer array: 1 ch, 40 kHz, driver OK
I (644) sentry: [HW] hull penetrator seal: OK, pressure sensor: OK
W (644) sentry: [NAV] depth sensor offline (lab mode) - using simulator
I (654) sentry: [NAV] carrier: SSK 'Skat', bow sonar bay #2, depth 41.8 m
I (664) sentry: [OTA] running v2.3.0 from ota_1
W (664) sentry: [OTA] new firmware, PENDING_VERIFY - self-check...
I (714) sentry: [OTA] self-check passed, firmware marked VALID
```

### 7. `ota install 2.1.0`

```text
I (222374) esp-x509-crt-bundle: Certificate validated
I (223254) sentry: [OTA] current v2.3.0 (ota_1) -> target partition ota_0
I (223254) sentry: [OTA] downloading https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/fw7/v2.1.0/sentry_fw7.bin
I (223654) esp-x509-crt-bundle: Certificate validated
I (224294) esp_https_ota: Starting OTA...
I (224294) esp_https_ota: Writing to <ota_0> partition at offset 0x20000
I (224304) sentry: [OTA] image: sentry_fw7 v2.1.0 (build Oct  6 2026 02:14:57)
E (224304) sentry: E408 downgrade blocked: v2.3.0 -> v2.1.0. Use 'ota install 2.1.0 force'
```

### 8. `ota install 2.1.0 force`

```text
I (263314) esp-x509-crt-bundle: Certificate validated
I (263954) sentry: [OTA] current v2.3.0 (ota_1) -> target partition ota_0
I (263954) sentry: [OTA] downloading https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/fw7/v2.1.0/sentry_fw7.bin
I (264354) esp-x509-crt-bundle: Certificate validated
I (264984) esp_https_ota: Starting OTA...
I (264984) esp_https_ota: Writing to <ota_0> partition at offset 0x20000
I (265144) sentry: [OTA] image: sentry_fw7 v2.1.0 (build Oct  6 2026 02:14:57)
I (267064) sentry: [OTA]  10%
I (268724) sentry: [OTA]  20%
I (270724) sentry: [OTA]  30%
I (272574) sentry: [OTA]  40%
I (274514) sentry: [OTA]  50%
I (276454) sentry: [OTA]  60%
I (278354) sentry: [OTA]  70%
I (280214) sentry: [OTA]  80%
I (282284) sentry: [OTA]  90%
I (283994) sentry: [OTA] 100%
I (283994) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
I (284024) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) 
I (284024) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) 
I (284024) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
I (284124) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) 
I (284124) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) 
I (284134) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
I (284164) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) 
I (284164) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) 
I (284174) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
I (284264) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) 
I (284274) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) 
I (284314) sentry: [OTA] success: v2.3.0 -> v2.1.0 in 19 s. Rebooting...
I (284814) wifi:state: run -> init (0x0)
I (284814) wifi:pm stop, total sleep time: 79186662 us / 117186436 us

I (284814) wifi:<ba-del>idx:1, tid:0
I (284814) wifi:<ba-del>idx:0, tid:5
I (284814) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (284864) wifi:flush txq
I (284864) wifi:stop sw txq
I (284864) wifi:lmac stop hw txq
��ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d344
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Oct  6 2026 02:15:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 4MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (67) boot:  1 otadata          OTA data         01 00 0000f000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00020000 00180000
I (80) boot:  3 ota_1            OTA app          00 11 001a0000 00180000
I (87) boot: End of partition table
I (114) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
I (155) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) load
I (160) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) load
I (163) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
I (281) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) load
I (295) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) load
I (304) boot: Loaded app from partition at offset 0x20000
I (304) boot: Disabling RNG early entropy source...
I (314) cpu_start: Multicore app
I (322) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (323) cpu_start: Pro cpu start user code
I (323) cpu_start: cpu freq: 160000000 Hz
I (325) app_init: Application information:
I (328) app_init: Project name:     sentry_fw7
I (333) app_init: App version:      2.1.0
I (336) app_init: Compile time:     Oct  6 2026 02:14:57
I (341) app_init: ELF file SHA256:  c9460b826...
I (346) app_init: ESP-IDF:          v6.0.1
I (350) efuse_init: Min chip rev:     v0.0
I (353) efuse_init: Max chip rev:     v0.99 
I (357) efuse_init: Chip rev:         v0.2
I (361) heap_init: Initializing. RAM available for dynamic allocation:
I (368) heap_init: At 3FCA0950 len 00048DC0 (291 KiB): RAM
I (373) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (378) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (383) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (389) spi_flash: detected chip: mxic
I (392) spi_flash: flash io: dio
W (395) spi_flash: Detected size(16384k) larger than the size in the binary image header(4096k). Using the size in the binary image header.
I (408) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (413) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (420) main_task: Started on CPU0
I (440) main_task: Calling app_main()
I (450) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (460) sentry: ==============================================
I (460) sentry:   SENTRY SWM-2  sonar watch module  fw v2.1.0
I (460) sentry:   bow sonar array / perimeter watch / CIC link
I (470) sentry: ==============================================
I (470) pp: pp rom version: e7ae62f
I (480) net80211: net80211 rom version: e7ae62f
I (490) wifi:wifi driver task: 3fced484, prio:23, stack:6656, core=0
I (490) wifi:wifi firmware version: b37c951
I (490) wifi:wifi certification version: v7.0
I (490) wifi:config NVS flash: enabled
I (500) wifi:config nano formatting: disabled
I (500) wifi:Init data frame dynamic rx buffer num: 32
I (510) wifi:Init static rx mgmt buffer num: 5
I (510) wifi:Init management short buffer num: 32
I (510) wifi:Init dynamic tx buffer num: 32
I (520) wifi:Init static tx FG buffer num: 2
I (520) wifi:Init static rx buffer size: 1600
I (530) wifi:Init static rx buffer num: 10
I (530) wifi:Init dynamic rx buffer num: 32
I (540) wifi_init: rx ba win: 6
I (540) wifi_init: accept mbox: 6
I (540) wifi_init: tcpip mbox: 32
I (540) wifi_init: udp mbox: 6
I (550) wifi_init: tcp mbox: 6
I (550) wifi_init: tcp tx win: 5760
I (550) wifi_init: tcp rx win: 5760
I (560) wifi_init: tcp mss: 1440
I (560) wifi_init: WiFi IRAM OP enabled
I (560) wifi_init: WiFi RX IRAM OP enabled
I (570) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (620) wifi:mode : sta (90:70:69:31:a6:8c)
I (620) wifi:enable tsf
I (620) sentry: [LINK] known network 'antony_g5'. Type 'reconnect' to connect
I (620) sentry: [AUTH] profile 'ant' registered
I (620) sentry: last reset: software reboot
I (630) sentry: build tag: c3VkbyBzM250cnktcjAwdA==
I (630) sentry: [HW] transducer array: 1 ch, 40 kHz, driver OK
I (640) sentry: [HW] hull penetrator seal: OK, pressure sensor: OK
W (640) sentry: [NAV] depth sensor offline (lab mode) - using simulator
I (650) sentry: [NAV] carrier: SSK 'Skat', bow sonar bay #2, depth 41.8 m
I (660) sentry: [OTA] running v2.1.0 from ota_0
W (660) sentry: [OTA] new firmware, PENDING_VERIFY - self-check...
I (700) sentry: [OTA] self-check passed, firmware marked VALID
I (700) sentry: ready. state 1 NORMAL (patrol). Type 'help'
```

### 9. `ota broken`

```text
W (120750) sentry: [OTA] installing intentionally broken build (rollback test)
I (120750) sentry: [OTA] current v2.1.0 (ota_0) -> target partition ota_1
I (120750) sentry: [OTA] downloading https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/fw7/broken/sentry_fw7.bin
I (121160) esp-x509-crt-bundle: Certificate validated
I (122120) esp_https_ota: Starting OTA...
I (122120) esp_https_ota: Writing to <ota_1> partition at offset 0x1a0000
I (122120) sentry: [OTA] image: sentry_fw7 v2.9.0-broken (build Oct  6 2026 02:15:55)
I (124200) sentry: [OTA]  10%
I (126020) sentry: [OTA]  20%
I (127700) sentry: [OTA]  30%
I (129450) sentry: [OTA]  40%
I (131190) sentry: [OTA]  50%
I (133150) sentry: [OTA]  60%
I (134880) sentry: [OTA]  70%
I (136760) sentry: [OTA]  80%
I (137070) sentry: [TELEMETRY #1] 18:46:09 up 00:02:16 heap 214KB rssi -52 temp 43.0C depth 42.2m hull 5.2bar batt 24.2V valve closed sonar - state NORMAL
I (138650) sentry: [OTA]  90%
I (140190) sentry: [OTA] 100%
I (140190) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=38128h (229672) map
I (140220) esp_image: segment 1: paddr=001d8150 vaddr=3fc97200 size=05198h ( 20888) 
I (140220) esp_image: segment 2: paddr=001dd2f0 vaddr=40374000 size=02d28h ( 11560) 
I (140220) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9c04ch (639052) map
I (140310) esp_image: segment 4: paddr=0027c074 vaddr=40376d28 size=103e8h ( 66536) 
I (140320) esp_image: segment 5: paddr=0028c464 vaddr=50000000 size=00024h (    36) 
I (140330) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=38128h (229672) map
I (140360) esp_image: segment 1: paddr=001d8150 vaddr=3fc97200 size=05198h ( 20888) 
I (140360) esp_image: segment 2: paddr=001dd2f0 vaddr=40374000 size=02d28h ( 11560) 
I (140370) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9c04ch (639052) map
I (140460) esp_image: segment 4: paddr=0027c074 vaddr=40376d28 size=103e8h ( 66536) 
I (140470) esp_image: segment 5: paddr=0028c464 vaddr=50000000 size=00024h (    36) 
I (140510) sentry: [OTA] success: v2.1.0 -> v2.9.0-broken in 18 s. Rebooting...
I (141010) wifi:state: run -> init (0x0)
I (141010) wifi:pm stop, total sleep time: 24662662 us / 47297809 us

I (141010) wifi:<ba-del>idx:1, tid:0
I (141010) wifi:<ba-del>idx:0, tid:5
I (141010) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (141060) wifi:flush txq
I (141060) wifi:stop sw txq
I (141060) wifi:lmac stop hw txq
��ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d344
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Oct  6 2026 02:15:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 4MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (67) boot:  1 otadata          OTA data         01 00 0000f000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00020000 00180000
I (80) boot:  3 ota_1            OTA app          00 11 001a0000 00180000
I (87) boot: End of partition table
I (116) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=38128h (229672) map
I (157) esp_image: segment 1: paddr=001d8150 vaddr=3fc97200 size=05198h ( 20888) load
I (162) esp_image: segment 2: paddr=001dd2f0 vaddr=40374000 size=02d28h ( 11560) load
I (165) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9c04ch (639052) map
I (283) esp_image: segment 4: paddr=0027c074 vaddr=40376d28 size=103e8h ( 66536) load
I (298) esp_image: segment 5: paddr=0028c464 vaddr=50000000 size=00024h (    36) load
I (307) boot: Loaded app from partition at offset 0x1a0000
I (307) boot: Disabling RNG early entropy source...
I (317) cpu_start: Multicore app
I (326) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (326) cpu_start: Pro cpu start user code
I (326) cpu_start: cpu freq: 160000000 Hz
I (328) app_init: Application information:
I (332) app_init: Project name:     sentry_fw7
I (336) app_init: App version:      2.9.0-broken
I (340) app_init: Compile time:     Oct  6 2026 02:15:55
I (345) app_init: ELF file SHA256:  62e41e73c...
I (350) app_init: ESP-IDF:          v6.0.1
I (354) efuse_init: Min chip rev:     v0.0
I (357) efuse_init: Max chip rev:     v0.99 
I (361) efuse_init: Chip rev:         v0.2
I (365) heap_init: Initializing. RAM available for dynamic allocation:
I (372) heap_init: At 3FCA1360 len 000483B0 (288 KiB): RAM
I (377) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (382) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (387) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (393) spi_flash: detected chip: mxic
I (396) spi_flash: flash io: dio
W (399) spi_flash: Detected size(16384k) larger than the size in the binary image header(4096k). Using the size in the binary image header.
I (412) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (417) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (424) main_task: Started on CPU0
I (444) main_task: Calling app_main()
I (454) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (464) sentry: ==============================================
I (464) sentry:   SENTRY SWM-2  sonar watch module  fw v2.9.0-broken
I (464) sentry:   bow sonar array / perimeter watch / CIC link
I (474) sentry: ==============================================
I (474) pp: pp rom version: e7ae62f
I (484) net80211: net80211 rom version: e7ae62f
I (494) wifi:wifi driver task: 3fced484, prio:23, stack:6656, core=0
I (494) wifi:wifi firmware version: b37c951
I (494) wifi:wifi certification version: v7.0
I (494) wifi:config NVS flash: enabled
I (504) wifi:config nano formatting: disabled
I (504) wifi:Init data frame dynamic rx buffer num: 32
I (514) wifi:Init static rx mgmt buffer num: 5
I (514) wifi:Init management short buffer num: 32
I (524) wifi:Init dynamic tx buffer num: 32
I (524) wifi:Init static tx FG buffer num: 2
I (524) wifi:Init static rx buffer size: 1600
I (534) wifi:Init static rx buffer num: 10
I (534) wifi:Init dynamic rx buffer num: 32
I (544) wifi_init: rx ba win: 6
I (544) wifi_init: accept mbox: 6
I (544) wifi_init: tcpip mbox: 32
I (544) wifi_init: udp mbox: 6
I (554) wifi_init: tcp mbox: 6
I (554) wifi_init: tcp tx win: 5760
I (554) wifi_init: tcp rx win: 5760
I (564) wifi_init: tcp mss: 1440
I (564) wifi_init: WiFi IRAM OP enabled
I (564) wifi_init: WiFi RX IRAM OP enabled
I (574) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (624) wifi:mode : sta (90:70:69:31:a6:8c)
I (624) wifi:enable tsf
I (624) sentry: [LINK] known network 'antony_g5'. Type 'reconnect' to connect
I (624) sentry: [AUTH] profile 'ant' registered
I (624) sentry: last reset: software reboot
I (634) sentry: build tag: c3VkbyBzM250cnktcjAwdA==
I (634) sentry: [HW] transducer array: 1 ch, 40 kHz, driver OK
I (644) sentry: [HW] hull penetrator seal: OK, pressure sensor: OK
W (644) sentry: [NAV] depth sensor offline (lab mode) - using simulator
I (654) sentry: [NAV] carrier: SSK 'Skat', bow sonar bay #2, depth 41.8 m
I (664) sentry: [OTA] running v2.9.0-broken from ota_1
W (664) sentry: [OTA] new firmware, PENDING_VERIFY - self-check...
E (674) sentry: [OTA] self-check FAILED: core module init error. Rolling back...
I (1334) esp_ota_ops: Rollback to previously worked partition.
I (1334) wifi:flush txq
I (1334) wifi:stop sw txq
I (1334) wifi:lmac stop hw txq
���ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d344
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Oct  6 2026 02:15:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 4MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (67) boot:  1 otadata          OTA data         01 00 0000f000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00020000 00180000
I (80) boot:  3 ota_1            OTA app          00 11 001a0000 00180000
I (87) boot: End of partition table
I (90) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
I (138) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) load
I (143) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) load
I (146) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
I (263) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) load
I (278) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) load
I (286) boot: Loaded app from partition at offset 0x20000
I (287) boot: Disabling RNG early entropy source...
I (297) cpu_start: Multicore app
I (305) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (306) cpu_start: Pro cpu start user code
I (306) cpu_start: cpu freq: 160000000 Hz
I (308) app_init: Application information:
I (311) app_init: Project name:     sentry_fw7
I (316) app_init: App version:      2.1.0
I (319) app_init: Compile time:     Oct  6 2026 02:14:57
I (324) app_init: ELF file SHA256:  c9460b826...
I (329) app_init: ESP-IDF:          v6.0.1
I (332) efuse_init: Min chip rev:     v0.0
I (336) efuse_init: Max chip rev:     v0.99 
I (340) efuse_init: Chip rev:         v0.2
I (344) heap_init: Initializing. RAM available for dynamic allocation:
I (350) heap_init: At 3FCA0950 len 00048DC0 (291 KiB): RAM
I (356) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (361) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (366) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (372) spi_flash: detected chip: mxic
I (375) spi_flash: flash io: dio
W (378) spi_flash: Detected size(16384k) larger than the size in the binary image header(4096k). Using the size in the binary image header.
I (390) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (396) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (403) main_task: Started on CPU0
I (423) main_task: Calling app_main()
I (433) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (443) sentry: ==============================================
I (443) sentry:   SENTRY SWM-2  sonar watch module  fw v2.1.0
I (443) sentry:   bow sonar array / perimeter watch / CIC link
I (453) sentry: ==============================================
I (453) pp: pp rom version: e7ae62f
I (463) net80211: net80211 rom version: e7ae62f
I (473) wifi:wifi driver task: 3fced484, prio:23, stack:6656, core=0
I (473) wifi:wifi firmware version: b37c951
I (473) wifi:wifi certification version: v7.0
I (473) wifi:config NVS flash: enabled
I (483) wifi:config nano formatting: disabled
I (483) wifi:Init data frame dynamic rx buffer num: 32
I (493) wifi:Init static rx mgmt buffer num: 5
I (493) wifi:Init management short buffer num: 32
I (493) wifi:Init dynamic tx buffer num: 32
I (503) wifi:Init static tx FG buffer num: 2
I (503) wifi:Init static rx buffer size: 1600
I (513) wifi:Init static rx buffer num: 10
I (513) wifi:Init dynamic rx buffer num: 32
I (523) wifi_init: rx ba win: 6
I (523) wifi_init: accept mbox: 6
I (523) wifi_init: tcpip mbox: 32
I (523) wifi_init: udp mbox: 6
I (533) wifi_init: tcp mbox: 6
I (533) wifi_init: tcp tx win: 5760
I (533) wifi_init: tcp rx win: 5760
I (543) wifi_init: tcp mss: 1440
I (543) wifi_init: WiFi IRAM OP enabled
I (543) wifi_init: WiFi RX IRAM OP enabled
I (553) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (603) wifi:mode : sta (90:70:69:31:a6:8c)
I (603) wifi:enable tsf
I (603) sentry: [LINK] known network 'antony_g5'. Type 'reconnect' to connect
I (603) sentry: [AUTH] profile 'ant' registered
I (603) sentry: last reset: software reboot
I (613) sentry: build tag: c3VkbyBzM250cnktcjAwdA==
I (613) sentry: [HW] transducer array: 1 ch, 40 kHz, driver OK
I (623) sentry: [HW] hull penetrator seal: OK, pressure sensor: OK
W (623) sentry: [NAV] depth sensor offline (lab mode) - using simulator
I (633) sentry: [NAV] carrier: SSK 'Skat', bow sonar bay #2, depth 41.8 m
I (643) sentry: [OTA] running v2.1.0 from ota_0
I (643) sentry: ready. state 1 NORMAL (patrol). Type 'help'
```

### 10. `ota rollback`

```text
I (44475) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
I (44505) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) 
I (44505) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) 
I (44505) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
I (44595) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) 
I (44605) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) 
W (44645) sentry: [OTA] rollback: v2.3.0 -> v2.1.0 (ota_0). Rebooting...
I (45145) wifi:state: run -> init (0x0)
I (45145) wifi:pm stop, total sleep time: 25182913 us / 30166450 us

I (45145) wifi:<ba-del>idx:1, tid:0
I (45145) wifi:<ba-del>idx:0, tid:5
I (45145) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (45155) wifi:flush txq
I (45155) wifi:stop sw txq
I (45155) wifi:lmac stop hw txq
ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4202ed10
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Oct  6 2026 02:15:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 4MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (67) boot:  1 otadata          OTA data         01 00 0000f000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00020000 00180000
I (80) boot:  3 ota_1            OTA app          00 11 001a0000 00180000
I (87) boot: End of partition table
I (116) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
I (157) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) load
I (162) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) load
I (165) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
I (283) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) load
I (297) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) load
I (306) boot: Loaded app from partition at offset 0x20000
I (306) boot: Disabling RNG early entropy source...
I (316) cpu_start: Multicore app
I (325) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (325) cpu_start: Pro cpu start user code
I (325) cpu_start: cpu freq: 160000000 Hz
I (327) app_init: Application information:
I (331) app_init: Project name:     sentry_fw7
I (335) app_init: App version:      2.1.0
I (339) app_init: Compile time:     Oct  6 2026 02:14:57
I (344) app_init: ELF file SHA256:  c9460b826...
I (348) app_init: ESP-IDF:          v6.0.1
I (352) efuse_init: Min chip rev:     v0.0
I (356) efuse_init: Max chip rev:     v0.99 
I (360) efuse_init: Chip rev:         v0.2
I (364) heap_init: Initializing. RAM available for dynamic allocation:
I (370) heap_init: At 3FCA0950 len 00048DC0 (291 KiB): RAM
I (375) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (380) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (385) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (392) spi_flash: detected chip: mxic
I (394) spi_flash: flash io: dio
W (397) spi_flash: Detected size(16384k) larger than the size in the binary image header(4096k). Using the size in the binary image header.
I (410) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (416) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (423) main_task: Started on CPU0
I (443) main_task: Calling app_main()
I (453) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (463) sentry: ==============================================
I (463) sentry:   SENTRY SWM-2  sonar watch module  fw v2.1.0
I (463) sentry:   bow sonar array / perimeter watch / CIC link
I (473) sentry: ==============================================
I (473) pp: pp rom version: e7ae62f
I (483) net80211: net80211 rom version: e7ae62f
I (493) wifi:wifi driver task: 3fced484, prio:23, stack:6656, core=0
I (493) wifi:wifi firmware version: b37c951
I (493) wifi:wifi certification version: v7.0
I (493) wifi:config NVS flash: enabled
I (503) wifi:config nano formatting: disabled
I (503) wifi:Init data frame dynamic rx buffer num: 32
I (513) wifi:Init static rx mgmt buffer num: 5
I (513) wifi:Init management short buffer num: 32
I (513) wifi:Init dynamic tx buffer num: 32
I (523) wifi:Init static tx FG buffer num: 2
I (523) wifi:Init static rx buffer size: 1600
I (533) wifi:Init static rx buffer num: 10
I (533) wifi:Init dynamic rx buffer num: 32
I (543) wifi_init: rx ba win: 6
I (543) wifi_init: accept mbox: 6
I (543) wifi_init: tcpip mbox: 32
I (543) wifi_init: udp mbox: 6
I (553) wifi_init: tcp mbox: 6
I (553) wifi_init: tcp tx win: 5760
I (553) wifi_init: tcp rx win: 5760
I (563) wifi_init: tcp mss: 1440
I (563) wifi_init: WiFi IRAM OP enabled
I (563) wifi_init: WiFi RX IRAM OP enabled
I (573) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (623) wifi:mode : sta (90:70:69:31:a6:8c)
I (623) wifi:enable tsf
I (623) sentry: [LINK] known network 'antony_g5'. Type 'reconnect' to connect
I (623) sentry: [AUTH] profile 'ant' registered
I (623) sentry: last reset: software reboot
I (633) sentry: build tag: c3VkbyBzM250cnktcjAwdA==
I (633) sentry: [HW] transducer array: 1 ch, 40 kHz, driver OK
I (643) sentry: [HW] hull penetrator seal: OK, pressure sensor: OK
W (643) sentry: [NAV] depth sensor offline (lab mode) - using simulator
I (653) sentry: [NAV] carrier: SSK 'Skat', bow sonar bay #2, depth 41.8 m
I (663) sentry: [OTA] running v2.1.0 from ota_0
W (663) sentry: [OTA] new firmware, PENDING_VERIFY - self-check...
I (703) sentry: [OTA] self-check passed, firmware marked VALID
I (703) sentry: ready. state 1 NORMAL (patrol). Type 'help'
```

### 11. `ota url https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/fw7/v2.3.0/sentry_fw7.bin`

```text
I (253353) sentry: [OTA] current v2.1.0 (ota_0) -> target partition ota_1
I (253353) sentry: [OTA] downloading https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/fw7/v2.3.0/sentry_fw7.bin
I (253773) esp-x509-crt-bundle: Certificate validated
I (254673) esp_https_ota: Starting OTA...
I (254673) esp_https_ota: Writing to <ota_1> partition at offset 0x1a0000
I (254683) sentry: [OTA] image: sentry_fw7 v2.3.0 (build Oct  6 2026 02:15:26)
I (256813) sentry: [OTA]  10%
I (258653) sentry: [OTA]  20%
I (260363) sentry: [OTA]  30%
I (262253) sentry: [OTA]  40%
I (263943) sentry: [OTA]  50%
I (265743) sentry: [OTA]  60%
I (267633) sentry: [OTA]  70%
I (269473) sentry: [OTA]  80%
I (271293) sentry: [OTA]  90%
I (272943) sentry: [OTA] 100%
I (272943) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=38158h (229720) map
I (272973) esp_image: segment 1: paddr=001d8180 vaddr=3fc97200 size=05198h ( 20888) 
I (272973) esp_image: segment 2: paddr=001dd320 vaddr=40374000 size=02cf8h ( 11512) 
I (272983) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9c08ch (639116) map
I (273073) esp_image: segment 4: paddr=0027c0b4 vaddr=40376cf8 size=10418h ( 66584) 
I (273083) esp_image: segment 5: paddr=0028c4d4 vaddr=50000000 size=00024h (    36) 
I (273083) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=38158h (229720) map
I (273113) esp_image: segment 1: paddr=001d8180 vaddr=3fc97200 size=05198h ( 20888) 
I (273123) esp_image: segment 2: paddr=001dd320 vaddr=40374000 size=02cf8h ( 11512) 
I (273123) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9c08ch (639116) map
I (273213) esp_image: segment 4: paddr=0027c0b4 vaddr=40376cf8 size=10418h ( 66584) 
I (273223) esp_image: segment 5: paddr=0028c4d4 vaddr=50000000 size=00024h (    36) 
I (273263) sentry: [OTA] success: v2.1.0 -> v2.3.0 in 18 s. Rebooting...
I (273763) wifi:state: run -> init (0x0)
I (273763) wifi:pm stop, total sleep time: 149585316 us / 190094270 us

I (273763) wifi:<ba-del>idx:1, tid:0
I (273763) wifi:<ba-del>idx:0, tid:5
I (273763) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (273823) wifi:flush txq
I (273823) wifi:stop sw txq
I (273823) wifi:lmac stop hw txq
��ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d344
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Oct  6 2026 02:15:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 4MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (67) boot:  1 otadata          OTA data         01 00 0000f000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00020000 00180000
I (80) boot:  3 ota_1            OTA app          00 11 001a0000 00180000
I (87) boot: End of partition table
I (117) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=38158h (229720) map
I (159) esp_image: segment 1: paddr=001d8180 vaddr=3fc97200 size=05198h ( 20888) load
I (163) esp_image: segment 2: paddr=001dd320 vaddr=40374000 size=02cf8h ( 11512) load
I (166) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9c08ch (639116) map
I (285) esp_image: segment 4: paddr=0027c0b4 vaddr=40376cf8 size=10418h ( 66584) load
I (300) esp_image: segment 5: paddr=0028c4d4 vaddr=50000000 size=00024h (    36) load
I (308) boot: Loaded app from partition at offset 0x1a0000
I (308) boot: Disabling RNG early entropy source...
I (318) cpu_start: Multicore app
I (327) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (328) cpu_start: Pro cpu start user code
I (328) cpu_start: cpu freq: 160000000 Hz
I (329) app_init: Application information:
I (333) app_init: Project name:     sentry_fw7
I (337) app_init: App version:      2.3.0
I (341) app_init: Compile time:     Oct  6 2026 02:15:26
I (346) app_init: ELF file SHA256:  ab377c338...
I (351) app_init: ESP-IDF:          v6.0.1
I (354) efuse_init: Min chip rev:     v0.0
I (358) efuse_init: Max chip rev:     v0.99 
I (362) efuse_init: Chip rev:         v0.2
I (366) heap_init: Initializing. RAM available for dynamic allocation:
I (372) heap_init: At 3FCA1360 len 000483B0 (288 KiB): RAM
I (377) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (383) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (388) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (394) spi_flash: detected chip: mxic
I (397) spi_flash: flash io: dio
W (399) spi_flash: Detected size(16384k) larger than the size in the binary image header(4096k). Using the size in the binary image header.
I (412) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (418) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (425) main_task: Started on CPU0
I (445) main_task: Calling app_main()
I (455) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (465) sentry: ==============================================
I (465) sentry:   SENTRY SWM-2  sonar watch module  fw v2.3.0
I (465) sentry:   bow sonar array / perimeter watch / CIC link
I (475) sentry: ==============================================
I (475) pp: pp rom version: e7ae62f
I (485) net80211: net80211 rom version: e7ae62f
I (495) wifi:wifi driver task: 3fced484, prio:23, stack:6656, core=0
I (495) wifi:wifi firmware version: b37c951
I (495) wifi:wifi certification version: v7.0
I (495) wifi:config NVS flash: enabled
I (505) wifi:config nano formatting: disabled
I (505) wifi:Init data frame dynamic rx buffer num: 32
I (515) wifi:Init static rx mgmt buffer num: 5
I (515) wifi:Init management short buffer num: 32
I (515) wifi:Init dynamic tx buffer num: 32
I (525) wifi:Init static tx FG buffer num: 2
I (525) wifi:Init static rx buffer size: 1600
I (535) wifi:Init static rx buffer num: 10
I (535) wifi:Init dynamic rx buffer num: 32
I (535) wifi_init: rx ba win: 6
I (545) wifi_init: accept mbox: 6
I (545) wifi_init: tcpip mbox: 32
I (545) wifi_init: udp mbox: 6
I (555) wifi_init: tcp mbox: 6
I (555) wifi_init: tcp tx win: 5760
I (555) wifi_init: tcp rx win: 5760
I (565) wifi_init: tcp mss: 1440
I (565) wifi_init: WiFi IRAM OP enabled
I (565) wifi_init: WiFi RX IRAM OP enabled
I (575) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (625) wifi:mode : sta (90:70:69:31:a6:8c)
I (625) wifi:enable tsf
I (625) sentry: [LINK] known network 'antony_g5'. Type 'reconnect' to connect
I (625) sentry: [AUTH] profile 'ant' registered
I (625) sentry: last reset: software reboot
I (635) sentry: build tag: c3VkbyBzM250cnktcjAwdA==
I (635) sentry: [HW] transducer array: 1 ch, 40 kHz, driver OK
I (645) sentry: [HW] hull penetrator seal: OK, pressure sensor: OK
W (645) sentry: [NAV] depth sensor offline (lab mode) - using simulator
I (655) sentry: [NAV] carrier: SSK 'Skat', bow sonar bay #2, depth 41.8 m
I (665) sentry: [OTA] running v2.3.0 from ota_1
W (665) sentry: [OTA] new firmware, PENDING_VERIFY - self-check...
I (705) sentry: [OTA] self-check passed, firmware marked VALID
```

### 12. `ota url https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/fw7/v2.1.0/sentry_fw7.bin`

```text
I (166985) sentry: [OTA] current v2.3.0 (ota_1) -> target partition ota_0
I (166985) sentry: [OTA] downloading https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/fw7/v2.1.0/sentry_fw7.bin
I (167355) esp-x509-crt-bundle: Certificate validated
I (168205) sentry: [PWR] battery bus 24.19 V, load 1.8 A
I (168215) esp_https_ota: Starting OTA...
I (168215) esp_https_ota: Writing to <ota_0> partition at offset 0x20000
I (168225) sentry: [OTA] image: sentry_fw7 v2.1.0 (build Oct  6 2026 02:14:57)
E (168225) sentry: E408 downgrade blocked: v2.3.0 -> v2.1.0. Use 'ota install 2.1.0 force'
```

### 13. `ota url https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/fw7/v2.1.0/sentry_fw7.bin force`

```text
I (205495) sentry: [OTA] current v2.3.0 (ota_1) -> target partition ota_0
I (205495) sentry: [OTA] downloading https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/fw7/v2.1.0/sentry_fw7.bin
I (205865) esp-x509-crt-bundle: Certificate validated
I (206525) esp_https_ota: Starting OTA...
I (206525) esp_https_ota: Writing to <ota_0> partition at offset 0x20000
I (206725) sentry: [OTA] image: sentry_fw7 v2.1.0 (build Oct  6 2026 02:14:57)
I (208715) sentry: [OTA]  10%
I (210595) sentry: [OTA]  20%
I (212505) sentry: [OTA]  30%
I (214365) sentry: [OTA]  40%
I (216535) sentry: [OTA]  50%
I (218345) sentry: [OTA]  60%
I (220315) sentry: [OTA]  70%
I (222165) sentry: [OTA]  80%
I (222345) sentry: [TELEMETRY #2] 18:58:17 up 00:03:41 heap 215KB rssi -66 temp 43.0C depth 42.3m hull 5.2bar batt 24.2V valve closed sonar - watch disarmed alerts 0 state NORMAL
I (224055) sentry: [OTA]  90%
I (225705) sentry: [OTA] 100%
I (225705) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
I (225735) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) 
I (225735) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) 
I (225735) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
I (225825) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) 
I (225835) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) 
I (225845) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
I (225875) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) 
I (225875) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) 
I (225875) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
I (225965) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) 
I (225975) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) 
I (226015) sentry: [OTA] success: v2.3.0 -> v2.1.0 in 19 s. Rebooting...
I (226515) wifi:state: run -> init (0x0)
I (226515) wifi:pm stop, total sleep time: 41369716 us / 70410836 us

I (226515) wifi:<ba-del>idx:1, tid:0
I (226515) wifi:<ba-del>idx:0, tid:5
I (226515) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (226555) wifi:flush txq
I (226555) wifi:stop sw txq
I (226555) wifi:lmac stop hw txq
��ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d344
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Oct  6 2026 02:15:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 4MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (67) boot:  1 otadata          OTA data         01 00 0000f000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00020000 00180000
I (80) boot:  3 ota_1            OTA app          00 11 001a0000 00180000
I (87) boot: End of partition table
I (116) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
I (157) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) load
I (161) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) load
I (165) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
I (282) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) load
I (297) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) load
I (305) boot: Loaded app from partition at offset 0x20000
I (305) boot: Disabling RNG early entropy source...
I (315) cpu_start: Multicore app
I (324) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (325) cpu_start: Pro cpu start user code
I (325) cpu_start: cpu freq: 160000000 Hz
I (326) app_init: Application information:
I (330) app_init: Project name:     sentry_fw7
I (334) app_init: App version:      2.1.0
I (338) app_init: Compile time:     Oct  6 2026 02:14:57
I (343) app_init: ELF file SHA256:  c9460b826...
I (347) app_init: ESP-IDF:          v6.0.1
I (351) efuse_init: Min chip rev:     v0.0
I (355) efuse_init: Max chip rev:     v0.99 
I (359) efuse_init: Chip rev:         v0.2
I (363) heap_init: Initializing. RAM available for dynamic allocation:
I (369) heap_init: At 3FCA0950 len 00048DC0 (291 KiB): RAM
I (374) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (379) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (385) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (391) spi_flash: detected chip: mxic
I (393) spi_flash: flash io: dio
W (396) spi_flash: Detected size(16384k) larger than the size in the binary image header(4096k). Using the size in the binary image header.
I (409) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (415) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (422) main_task: Started on CPU0
I (442) main_task: Calling app_main()
I (452) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (462) sentry: ==============================================
I (462) sentry:   SENTRY SWM-2  sonar watch module  fw v2.1.0
I (462) sentry:   bow sonar array / perimeter watch / CIC link
I (472) sentry: ==============================================
I (472) pp: pp rom version: e7ae62f
I (482) net80211: net80211 rom version: e7ae62f
I (492) wifi:wifi driver task: 3fced484, prio:23, stack:6656, core=0
I (492) wifi:wifi firmware version: b37c951
I (492) wifi:wifi certification version: v7.0
I (492) wifi:config NVS flash: enabled
I (502) wifi:config nano formatting: disabled
I (502) wifi:Init data frame dynamic rx buffer num: 32
I (512) wifi:Init static rx mgmt buffer num: 5
I (512) wifi:Init management short buffer num: 32
I (512) wifi:Init dynamic tx buffer num: 32
I (522) wifi:Init static tx FG buffer num: 2
I (522) wifi:Init static rx buffer size: 1600
I (532) wifi:Init static rx buffer num: 10
I (532) wifi:Init dynamic rx buffer num: 32
I (542) wifi_init: rx ba win: 6
I (542) wifi_init: accept mbox: 6
I (542) wifi_init: tcpip mbox: 32
I (542) wifi_init: udp mbox: 6
I (552) wifi_init: tcp mbox: 6
I (552) wifi_init: tcp tx win: 5760
I (552) wifi_init: tcp rx win: 5760
I (562) wifi_init: tcp mss: 1440
I (562) wifi_init: WiFi IRAM OP enabled
I (562) wifi_init: WiFi RX IRAM OP enabled
I (572) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (622) wifi:mode : sta (90:70:69:31:a6:8c)
I (622) wifi:enable tsf
I (622) sentry: [LINK] known network 'antony_g5'. Type 'reconnect' to connect
I (622) sentry: [AUTH] profile 'ant' registered
I (622) sentry: last reset: software reboot
I (632) sentry: build tag: c3VkbyBzM250cnktcjAwdA==
I (632) sentry: [HW] transducer array: 1 ch, 40 kHz, driver OK
I (642) sentry: [HW] hull penetrator seal: OK, pressure sensor: OK
W (642) sentry: [NAV] depth sensor offline (lab mode) - using simulator
I (652) sentry: [NAV] carrier: SSK 'Skat', bow sonar bay #2, depth 41.8 m
I (662) sentry: [OTA] running v2.1.0 from ota_0
W (662) sentry: [OTA] new firmware, PENDING_VERIFY - self-check...
I (702) sentry: [OTA] self-check passed, firmware marked VALID
```

## Firmware matrix — `poe full_cycle`

**Source:** supplied automation terminal report. These are actual pytest item outcomes. A `FAILED` item is not necessarily a confirmed firmware defect. During the `2.3.0: suite` failure of `test_channel_up_to_date_no_reboot[stable]`, the test had installed 2.1.0 before invoking the command; that failure is evidence for 2.1.0, not 2.3.0.

**Execution summary:**

| Stage | Passed | Failed | Skipped | Deselected |
| --- | ---: | ---: | ---: | ---: |
| 2.1.0 — first | 4 | 1 | 0 | 137 |
| 2.1.0 — suite | 120 | 7 | 5 | 10 |
| 2.3.0 — suite | 123 | 3 | 6 | 10 |

**Gatekeepers** (from screenshots): 2.1.0 **4 passed**; 2.3.0 **1 passed**. These are separate stages, not additional unique tests.

### Matrix terminal summary

```text
=== Firmware matrix finished ===
Stages with failed tests: 2.1.0: first, 2.1.0: suite, 2.3.0: suite
OTA server stopped.
```

### 2.1.0 — first (clean device) — full pytest failure and skip output

```text
=== 2.1.0: first ===
================================== FAILURES ===================================
_________________ test_time_unavailable_before_first_ntp_sync _________________
tests\wifi\test_00_clean.py:10: in test_time_unavailable_before_first_ntp_sync
    response = ota_device._connector.execute_command('time', until='E121', timeout=10)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lib\utilities\logger\step_logger.py:36: in wrapper
    return steps[selected](*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lib\utilities\logger\console_logger.py:72: in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
lib\connectors\uart_connector.py:72: in execute_command
    return self._read_response(
lib\connectors\uart_connector.py:115: in _read_response
    raise DeviceTimeoutError(
E   lib.utilities.exceptions.DeviceTimeoutError: Expected response ('E121',) was not received within 10s. Received: ['time', "E (2356) sentry: E002 Wi-Fi required. Use 'reconnect' or 'connect'"]
================ 1 failed, 4 passed, 137 deselected in 30.18s =================
```

### 2.1.0 — main suite — full pytest failure and skip output

```text
=== 2.1.0: suite ===
================================== FAILURES ===================================
____________________ test_timer_expires_and_turns_lamp_off ____________________
tests\lamp\test_06_lamp_timer.py:11: in test_timer_expires_and_turns_lamp_off
    assert '[BEACON] auto-off in 2 s' in response, response
E   AssertionError: lamp timer 2
E     I (71343) sentry: [BEACON] auto-off in 2 ms
E   assert '[BEACON] auto-off in 2 s' in 'lamp timer 2\nI (71343) sentry: [BEACON] auto-off in 2 ms'
____________________ test_timer_accepts_boundary_values[1] ____________________
tests\lamp\test_06_lamp_timer.py:35: in test_timer_accepts_boundary_values
    assert f'[BEACON] auto-off in {seconds} s' in response, response
E   AssertionError: lamp timer 1
E     I (78093) sentry: [BEACON] auto-off in 1 ms
E   assert '[BEACON] auto-off in 1 s' in 'lamp timer 1\nI (78093) sentry: [BEACON] auto-off in 1 ms'
__________________ test_timer_accepts_boundary_values[3600] ___________________
tests\lamp\test_06_lamp_timer.py:35: in test_timer_accepts_boundary_values
    assert f'[BEACON] auto-off in {seconds} s' in response, response
E   AssertionError: lamp timer 3600
E     I (79543) sentry: [BEACON] auto-off in 3600 ms
E   assert '[BEACON] auto-off in 3600 s' in 'lamp timer 3600\nI (79543) sentry: [BEACON] auto-off in 3600 ms'
__________ test_changed_password_persists_upgrade_downgrade_rollback __________
tests\ota\test_13_extra_persistence.py:67: in test_changed_password_persists_upgrade_downgrade_rollback
    login_new_and_reject_old('after upgrade', check_old=True)
tests\ota\test_13_extra_persistence.py:44: in login_new_and_reject_old
    assert login_ok and re.search(rf'user:\s*{re.escape(login)}\b', who), (
E   AssertionError: after upgrade: login with new password failed; login_ok=False; whoami='whoami\nI (8864) sentry: not logged in'
E   assert (False)
---------------------------- Captured stdout call -----------------------------
OTA firmware restore: 2.3.0 -> 2.1.0
OTA firmware restored: 2.1.0
_________________ test_scan_includes_reference_ssid_and_rssi __________________
tests\wifi\test_02_status.py:41: in test_scan_includes_reference_ssid_and_rssi
    networks = wifi_device.buoy.scan()
               ^^^^^^^^^^^^^^^^^^^^^^^
lib\utilities\logger\step_logger.py:36: in wrapper
    return steps[selected](*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lib\utilities\logger\console_logger.py:72: in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
framework\device\controllers\buoy_controller.py:42: in scan
    response = self._connector.execute_command(
lib\utilities\logger\step_logger.py:36: in wrapper
    return steps[selected](*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lib\utilities\logger\console_logger.py:72: in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
lib\connectors\uart_connector.py:72: in execute_command
    return self._read_response(
lib\connectors\uart_connector.py:115: in _read_response
    raise DeviceTimeoutError(
E   lib.utilities.exceptions.DeviceTimeoutError: Expected response ('networks:', 'E108') was not received within 15s. Received: ['scan', 'I (18179) sentry: [LINK] scanning...', 'W (20659) sentry: [ACU] biologics detected (snapping shrimp), passive filter on', 'I (21079) sentry:   [ 1] antony_g5                         -52 dBm  ch  5  secured', 'I (21079) sentry:   [ 2] antony_g5                         -63 dBm  ch  5  secured', 'I (21079) sentry:   [ 3] TP-Link_D5DE                      -69 dBm  ch  2  secured', 'I (21089) sentry:   [ 4] Arming                            -72 dBm  ch  1  secured', 'I (21089) sentry:   [ 5] antony_g5                         -76 dBm  ch  5  secured', 'I (21099) sentry:   [ 6] netis_2.4G_BB7AAD                 -76 dBm  ch  3  secured', 'I (21109) sentry:   [ 7] _2.4G_virus2020                   -78 dBm  ch  6  secured', 'I (21119) sentry:   [ 8] Office            -80 dBm  ch  1  secured', 'I (21119) sentry:   [ 9] TP-Link_CEF1                      -82 dBm  ch  1  secured', 'I (21129) sentry:   [10] netis_2.4G_02E3A7  -82 dBm  ch 11  secured', 'I (21139) sentry:   [11] AB                                -84 dBm  ch  1  secured', 'I (21139) sentry:   [12] Arming                            -86 dBm ch  6  secured', 'I (21149) sentry:   [13] FH                                -86 dBm  ch 11  secured', 'I (21159) sentry:   [14] Peremoga                          -89 dBm  ch 11  secured', 'I (21169) sentry:   [15] IV                                -91 dBm  ch  3  secured', 'I (21169) sentry:   [16] FastFurious                       -92 dBm  ch  6  secured', 'I (21179) sentry:   [17] MERCUSYS_33D6                     -93 dBm  ch 11  open', 'I (21189) sentry:   [18] Umniah Mobile WiFi                -94 dBm  ch  1  secured', 'I (21199) sentry:   [19] jane                              -94 dBm  ch  1  secured']
__________________ test_channel_up_to_date_no_reboot[stable] __________________
tests\ota\test_03_update.py:40: in test_channel_up_to_date_no_reboot
    pytest.fail(f'OTA-4: same-version update unexpectedly flashed and rebooted:\n{response}')
E   Failed: OTA-4: same-version update unexpectedly flashed and rebooted:
E   ota update
E   I (49063) sentry: [OTA] stable channel: v2.1.0, current: v2.1.0
E   I (49153) sentry: [OTA] current v2.1.0 (ota_1) -> target partition ota_0
E   I (49153) sentry: [OTA] downloading http://192.168.68.109:8000/fw7/v2.1.0/sentry_fw7.bin
E   I (49263) esp_https_ota: Starting OTA...
E   I (49263) esp_https_ota: Writing to <ota_0> partition at offset 0x20000
E   I (49263) sentry: [OTA] image: sentry_fw7 v2.1.0 (build Oct  6 2026 02:14:57)
E   W (49263) sentry: W409 same version v2.1.0 - reinstalling
E   I (51453) sentry: [OTA]  10%
E   I (53423) sentry: [OTA]  20%
E   I (55403) sentry: [OTA]  30%
E   I (57703) sentry: [OTA]  40%
E   I (60003) sentry: [OTA]  50%
E   I (62333) sentry: [OTA]  60%
E   I (64563) sentry: [OTA]  70%
E   I (66793) sentry: [OTA]  80%
E   I (69193) sentry: [OTA]  90%
E   I (71393) sentry: [OTA] 100%
E   I (71393) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
E   I (71433) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) 
E   I (71433) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) 
E   I (71433) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
E   I (71523) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) 
E   I (71533) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) 
E   I (71543) esp_image: segment 0: paddr=00020020 vaddr=3c0a0020 size=378a8h (227496) map
E   I (71573) esp_image: segment 1: paddr=000578d0 vaddr=3fc97200 size=05188h ( 20872) 
E   I (71573) esp_image: segment 2: paddr=0005ca60 vaddr=40374000 size=035b8h ( 13752) 
E   I (71583) esp_image: segment 3: paddr=00060020 vaddr=42000020 size=9b1c0h (635328) map
E   I (71673) esp_image: segment 4: paddr=000fb1e8 vaddr=403775b8 size=0fb58h ( 64344) 
E   I (71673) esp_image: segment 5: paddr=0010ad48 vaddr=50000000 size=00024h (    36) 
E   I (71723) sentry: [OTA] success: v2.1.0 -> v2.1.0 in 22 s. Rebooting...
________________________ test_concurrent_ota_rejected _________________________
tests\ota\test_12_rollback_edgecases.py:90: in test_concurrent_ota_rejected
    assert 'E401' in stream, (
E   AssertionError: Expected E401 for second OTA install during active download; command_echo_seen=False; first_ota_completed=True; UART log:
E     I (20673) sentry: [NAV] depth 42.0 m, heading 275, speed 3.3 kn
E     I (21733) sentry: [OTA]  20%
E     I (26583) sentry: [OTA]  30%
E     I (31193) sentry: [OTA]  40%
E     I (36063) sentry: [OTA]  50%
E     I (40553) sentry: [OTA]  60%
E     I (40673) sentry: [TELEMETRY #1] 15:52:01 up 00:00:40 heap 245KB rssi -73 temp 48.0C depth 42.0m hull 5.2bar batt 24.2V valve closed sonar - state NORMAL
E     I (45383) sentry: [OTA]  70%
E     I (49993) sentry: [OTA]  80%
E     I (54943) sentry: [OTA]  90%
E     I (59283) sentry: [OTA] 100%
E     I (59283) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=378a8h (227496) map
E     I (59313) esp_image: segment 1: paddr=001d78d0 vaddr=3fc97200 size=05188h ( 20872) 
E     I (59313) esp_image: segment 2: paddr=001dca60 vaddr=40374000 size=035b8h ( 13752) 
E     I (59323) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9b1c0h (635328) map
E     I (59413) esp_image: segment 4: paddr=0027b1e8 vaddr=403775b8 size=0fb58h ( 64344) 
E     I (59423) esp_image: segment 5: paddr=0028ad48 vaddr=50000000 size=00024h (    36) 
E     I (59423) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=378a8h (227496) map
E     I (59453) esp_image: segment 1: paddr=001d78d0 vaddr=3fc97200 size=05188h ( 20872) 
E     I (59463) esp_image: segment 2: paddr=001dca60 vaddr=40374000 size=035b8h ( 13752) 
E     I (59463) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9b1c0h (635328) map
E     I (59553) esp_image: segment 4: paddr=0027b1e8 vaddr=403775b8 size=0fb58h ( 64344) 
E     I (59563) esp_image: segment 5: paddr=0028ad48 vaddr=50000000 size=00024h (    36) 
E     I (59603) sentry: [OTA] success: v2.1.0 -> v2.1.0 in 47 s. Rebooting...
E   assert 'E401' in 'I (20673) sentry: [NAV] depth 42.0 m, heading 275, speed 3.3 kn\nI (21733) sentry: [OTA]  20%\nI (26583) sentry: [OTA]  30%\nI (31193) sentry: [OTA]  40%\nI (36063) sentry: [OTA]  50%\nI (40553) sentry: [OTA]  60%\nI (40673) sentry: [TELEMETRY #1] 15:52:01 up 00:00:40 heap 245KB rssi -73 temp 48.0C depth 42.0m hull 5.2bar batt 24.2V valve closed sonar - state NORMAL\nI (45383) sentry: [OTA]  70%\nI (49993) sentry: [OTA]  80%\nI (54943) sentry: [OTA]  90%\nI (59283) sentry: [OTA] 100%\nI (59283) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=378a8h (227496) map\nI (59313) esp_image: segment 1: paddr=001d78d0 vaddr=3fc97200 size=05188h ( 20872) \nI (59313) esp_image: segment 2: paddr=001dca60 vaddr=40374000 size=035b8h ( 13752) \nI (59323) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9b1c0h (635328) map\nI (59413) esp_image: segment 4: paddr=0027b1e8 vaddr=403775b8 size=0fb58h ( 64344) \nI (59423) esp_image: segment 5: paddr=0028ad48 vaddr=50000000 size=00024h (    36) \nI (59423) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=378a8h (227496) map\nI (59453) esp_image: segment 1: paddr=001d78d0 vaddr=3fc97200 size=05188h ( 20872) \nI (59463) esp_image: segment 2: paddr=001dca60 vaddr=40374000 size=035b8h ( 13752) \nI (59463) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9b1c0h (635328) map\nI (59553) esp_image: segment 4: paddr=0027b1e8 vaddr=403775b8 size=0fb58h ( 64344) \nI (59563) esp_image: segment 5: paddr=0028ad48 vaddr=50000000 size=00024h (    36) \nI (59603) sentry: [OTA] success: v2.1.0 -> v2.1.0 in 47 s. Rebooting...'
=========================== short test summary info ===========================
SKIPPED [1] tests\ota\test_01_check.py:20: Requires firmware == 2.3.0, current firmware is 2.1.0
SKIPPED [1] tests\ota\test_06_persistence.py:74: Requires firmware == 2.3.0, current firmware is 2.1.0
SKIPPED [1] tests\ota\test_14_guard_persistence.py:24: Requires firmware == 2.3.0, current firmware is 2.1.0
SKIPPED [1] tests\ota\test_01_check.py:34: Requires firmware == 2.3.0, current firmware is 2.1.0
SKIPPED [1] tests\ota\test_02_install.py:21: Requires firmware == 2.3.0, current firmware is 2.1.0
==== 7 failed, 120 passed, 5 skipped, 10 deselected in 1393.75s (0:23:13) =====
```

### 2.3.0 — main suite — full pytest failure and skip output

```text
=== 2.3.0: suite ===
================================== FAILURES ===================================
_________________ test_scan_includes_reference_ssid_and_rssi __________________
tests\wifi\test_02_status.py:41: in test_scan_includes_reference_ssid_and_rssi
    networks = wifi_device.buoy.scan()
               ^^^^^^^^^^^^^^^^^^^^^^^
lib\utilities\logger\step_logger.py:36: in wrapper
    return steps[selected](*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lib\utilities\logger\console_logger.py:72: in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
framework\device\controllers\buoy_controller.py:42: in scan
    response = self._connector.execute_command(
lib\utilities\logger\step_logger.py:36: in wrapper
    return steps[selected](*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lib\utilities\logger\console_logger.py:72: in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
lib\connectors\uart_connector.py:72: in execute_command
    return self._read_response(
lib\connectors\uart_connector.py:115: in _read_response
    raise DeviceTimeoutError(
E   lib.utilities.exceptions.DeviceTimeoutError: Expected response ('networks:', 'E108') was not received within 15s. Received: ['scan', 'I (19881) sentry: [LINK] scanning...', 'I (20651) sentry: [NAV] depth 41.8 m, heading 273, speed 2.9 kn', 'I (22781) sentry:   [ 1] antony_g5                         -47 dBm  ch  5  secured', 'I (22781) sentry:   [ 2] antony_g5                         -63 dBm  ch  5  secured', 'I (22781) sentry:   [ 3] Arming                            -71 dBm  ch  1  secured', 'I (22791) sentry:   [ 4] TP-Link_D5DE                -71 dBm  ch  2  secured', 'I (22791) sentry:   [ 5] _2.4G_virus2020                   -71 dBm  ch  6  secured', 'I (22801) sentry:   [ 6] netis_2.4G_BB7AAD      -74 dBm  ch  3  secured', 'I (22811) sentry:   [ 7] antony_g5                         -78 dBm  ch  5  secured', 'I (22821) sentry:   [ 8] TP-Link_CEF1                      -83dBm  ch  1  secured', 'I (22821) sentry:   [ 9] netis_2.4G_02E3A7                 -83 dBm  ch 11  secured', 'I (22831) sentry:   [10] Arming                            -84 dBm  ch  6  secured', 'I (22841) sentry:   [11] Xiaomi_DFF4                       -87 dBm  ch 10  secured', 'I (22851) sentry:   [12] Pautina74                         -88 dBm  ch  7  secured', 'I (22851) sentry:   [13] Keenetic-9851                     -88 dBm  ch  8  secured', 'I (22861) sentry:   [14] FH                                -88 dBm  ch 11  secured', 'I (22871) sentry:   [15] @Ruijie-guest-E0D5                -91 dBm  ch  1  secured', 'I (22871) sentry:   [16] Peremoga                          -92 dBm  ch 11  secured', 'I (22881) sentry:   [17] Xiaomi_06A9                       -92 dBm  ch 11  secured', 'I (22891) sentry:   [18] MERCUSYS_33D6                     -92 dBm  ch 11  open', 'I (22901) sentry:   [19] TP-Link_1A32                      -93 dBm  ch  8  secured', 'I (22901) sentry:   [20] deagle                            -93 dBm  ch 11  secured']
__________________ test_channel_up_to_date_no_reboot[stable] __________________
tests\ota\test_03_update.py:40: in test_channel_up_to_date_no_reboot
    pytest.fail(f'OTA-4: same-version update unexpectedly flashed and rebooted:\n{response}')
E   Failed: OTA-4: same-version update unexpectedly flashed and rebooted:
E   ota update
E   I (6762) sentry: [OTA] stable channel: v2.1.0, current: v2.1.0
E   I (6852) sentry: [OTA] current v2.1.0 (ota_0) -> target partition ota_1
E   I (6852) sentry: [OTA] downloading http://192.168.68.109:8000/fw7/v2.1.0/sentry_fw7.bin
E   I (6942) esp_https_ota: Starting OTA...
E   I (6942) esp_https_ota: Writing to <ota_1> partition at offset 0x1a0000
E   I (6952) sentry: [OTA] image: sentry_fw7 v2.1.0 (build Oct  6 2026 02:14:57)
E   W (6952) sentry: W409 same version v2.1.0 - reinstalling
E   I (8402) sentry: [OTA]  10%
E   I (9822) sentry: [OTA]  20%
E   I (11182) sentry: [OTA]  30%
E   I (12452) sentry: [OTA]  40%
E   I (13782) sentry: [OTA]  50%
E   I (15232) sentry: [OTA]  60%
E   I (16742) sentry: [OTA]  70%
E   I (18102) sentry: [OTA]  80%
E   I (19532) sentry: [OTA]  90%
E   I (20722) sentry: [NAV] depth 41.5 m, heading 274, speed 3.2 kn
E   I (21442) sentry: [OTA] 100%
E   I (21442) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=378a8h (227496) map
E   I (21472) esp_image: segment 1: paddr=001d78d0 vaddr=3fc97200 size=05188h ( 20872) 
E   I (21482) esp_image: segment 2: paddr=001dca60 vaddr=40374000 size=035b8h ( 13752) 
E   I (21482) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9b1c0h (635328) map
E   I (21572) esp_image: segment 4: paddr=0027b1e8 vaddr=403775b8 size=0fb58h ( 64344) 
E   I (21582) esp_image: segment 5: paddr=0028ad48 vaddr=50000000 size=00024h (    36) 
E   I (21582) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=378a8h (227496) map
E   I (21612) esp_image: segment 1: paddr=001d78d0 vaddr=3fc97200 size=05188h ( 20872) 
E   I (21622) esp_image: segment 2: paddr=001dca60 vaddr=40374000 size=035b8h ( 13752) 
E   I (21622) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9b1c0h (635328) map
E   I (21712) esp_image: segment 4: paddr=0027b1e8 vaddr=403775b8 size=0fb58h ( 64344) 
E   I (21722) esp_image: segment 5: paddr=0028ad48 vaddr=50000000 size=00024h (    36) 
E   I (21762) sentry: [OTA] success: v2.1.0 -> v2.1.0 in 14 s. Rebooting...
-------------------------- Captured stdout teardown ---------------------------
OTA firmware restore: 2.1.0 -> 2.3.0
OTA firmware restored: 2.3.0
________________________ test_concurrent_ota_rejected _________________________
tests\ota\test_12_rollback_edgecases.py:90: in test_concurrent_ota_rejected
    assert 'E401' in stream, (
E   AssertionError: Expected E401 for second OTA install during active download; command_echo_seen=False; first_ota_completed=True; UART log:
E     I (18685) sentry: [OTA]  20%
E     W (20655) sentry: [HW] transducer #1 impedance drift +2.1% (compensated)
E     I (23275) sentry: [OTA]  30%
E     I (28115) sentry: [OTA]  40%
E     I (32825) sentry: [OTA]  50%
E     I (37535) sentry: [OTA]  60%
E     I (37845) sentry: [TELEMETRY #1] 16:13:55 up 00:00:37 heap 234KB rssi -64 temp 46.0C depth 41.8m hull 5.2bar batt 24.2V valve closed sonar - watch disarmed alerts 0 state NORMAL
E     I (42345) sentry: [OTA]  70%
E     I (47055) sentry: [OTA]  80%
E     I (51875) sentry: [OTA]  90%
E     I (56475) sentry: [OTA] 100%
E     I (56475) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=38158h (229720) map
E     I (56505) esp_image: segment 1: paddr=001d8180 vaddr=3fc97200 size=05198h ( 20888) 
E     I (56505) esp_image: segment 2: paddr=001dd320 vaddr=40374000 size=02cf8h ( 11512) 
E     I (56515) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9c08ch (639116) map
E     I (56605) esp_image: segment 4: paddr=0027c0b4 vaddr=40376cf8 size=10418h ( 66584) 
E     I (56615) esp_image: segment 5: paddr=0028c4d4 vaddr=50000000 size=00024h (    36) 
E     I (56615) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=38158h (229720) map
E     I (56645) esp_image: segment 1: paddr=001d8180 vaddr=3fc97200 size=05198h ( 20888) 
E     I (56655) esp_image: segment 2: paddr=001dd320 vaddr=40374000 size=02cf8h ( 11512) 
E     I (56655) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9c08ch (639116) map
E     I (56745) esp_image: segment 4: paddr=0027c0b4 vaddr=40376cf8 size=10418h ( 66584) 
E     I (56755) esp_image: segment 5: paddr=0028c4d4 vaddr=50000000 size=00024h (    36) 
E     I (56795) sentry: [OTA] success: v2.3.0 -> v2.3.0 in 47 s. Rebooting...
E   assert 'E401' in 'I (18685) sentry: [OTA]  20%\nW (20655) sentry: [HW] transducer #1 impedance drift +2.1% (compensated)\nI (23275) sentry: [OTA]  30%\nI (28115) sentry: [OTA]  40%\nI (32825) sentry: [OTA]  50%\nI (37535) sentry: [OTA]  60%\nI (37845) sentry: [TELEMETRY #1] 16:13:55 up 00:00:37 heap 234KB rssi -64 temp 46.0C depth 41.8m hull 5.2bar batt 24.2V valve closed sonar - watch disarmed alerts 0 state NORMAL\nI (42345) sentry: [OTA]  70%\nI (47055) sentry: [OTA]  80%\nI (51875) sentry: [OTA]  90%\nI (56475) sentry: [OTA] 100%\nI (56475) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=38158h (229720) map\nI (56505) esp_image: segment 1: paddr=001d8180 vaddr=3fc97200 size=05198h ( 20888) \nI (56505)esp_image: segment 2: paddr=001dd320 vaddr=40374000 size=02cf8h ( 11512) \nI (56515) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9c08ch (639116) map\nI (56605) esp_image: segment 4: paddr=0027c0b4 vaddr=40376cf8 size=10418h ( 66584) \nI (56615) esp_image: segment 5: paddr=0028c4d4 vaddr=50000000 size=00024h (    36) \nI (56615) esp_image: segment 0: paddr=001a0020 vaddr=3c0a0020 size=38158h (229720) map\nI (56645) esp_image: segment 1: paddr=001d8180 vaddr=3fc97200 size=05198h ( 20888) \nI (56655) esp_image: segment 2: paddr=001dd320 vaddr=40374000 size=02cf8h ( 11512) \nI (56655) esp_image: segment 3: paddr=001e0020 vaddr=42000020 size=9c08ch (639116) map\nI (56745) esp_image: segment 4: paddr=0027c0b4 vaddr=40376cf8 size=10418h ( 66584) \nI (56755) esp_image: segment 5: paddr=0028c4d4 vaddr=50000000 size=00024h (    36) \nI (56795) sentry: [OTA] success: v2.3.0 -> v2.3.0 in 47 s. Rebooting...'
=========================== short test summary info ===========================
SKIPPED [1] tests\ota\test_06_persistence.py:8: Requires firmware == 2.1.0, current firmware is 2.3.0
SKIPPED [1] tests\ota\test_06_persistence.py:39: Requires firmware == 2.1.0, current firmware is 2.3.0
SKIPPED [1] tests\ota\test_09_url.py:22: Requires HTTPS target newer than 2.3.0, got 2.3.0
SKIPPED [1] tests\ota\test_13_extra_persistence.py:23: Requires firmware == 2.1.0, current firmware is 2.3.0
SKIPPED [1] tests\ota\test_13_extra_persistence.py:84: Requires firmware == 2.1.0, current firmware is 2.3.0
SKIPPED [1] tests\ota\test_13_extra_persistence.py:113: Requires firmware == 2.1.0, current firmware is 2.3.0
==== 3 failed, 123 passed, 6 skipped, 10 deselected in 1241.55s (0:20:41) =====
```
