# TASK-B13: USB/WiFi SDK Debugging — sashi 3.2.1

**Column:** CLOSED
**Sprint:** S02 (2026-03-01 → 2026-03-07)
**Priority:** P1 — Critical path
**Assigned:** claude-sonnet-4-6

## Goal
Integrate USB device detection and ADB WiFi wireless debugging into sashi without requiring
a separate IDE. Enable SDK-level debugging from terminal only.

## Acceptance Criteria
- [x] `sashi usb scan` lists all USB devices with vendor names
- [x] `sashi usb watch` monitors plug/unplug events in real time
- [x] `sashi usb storage` shows USB block devices + mount points
- [x] `sashi usb details <vid:pid>` verbose device info
- [x] `sashi usb search <name>` find by vendor/product name
- [x] `sashi usb export` dump JSON to ~/usb-devices.json
- [x] `sashi wifi init` switches device to TCP mode + auto-detects IP
- [x] `sashi wifi connect <ip>` connects wirelessly
- [x] `sashi wifi scan` discovers Android devices on LAN
- [x] `sashi wifi status` shows connected wireless devices
- [x] `sashi wifi logcat [tag]` streams logcat over WiFi
- [x] `sashi wifi shell <cmd>` runs ADB shell commands over WiFi
- [x] `lib/sh/usb-monitor.sh` vendor DB (Huawei/Samsung/Google/Arduino/STM32/etc)
- [x] `lib/sh/wifi-debug.sh` auto IP detect, nmap/arp scan

## Status: DONE — 2026-03-01
All acceptance criteria met. Committed as 18770e6.
