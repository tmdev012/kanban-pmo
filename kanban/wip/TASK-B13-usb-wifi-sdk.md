# TASK-B13: USB/WiFi SDK Debugging — sashi 3.2.1

**Column:** WIP
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
- [x] `sashi wifi init` switches device to TCP mode + auto-detects IP
- [x] `sashi wifi connect <ip>` connects wirelessly
- [x] `sashi wifi scan` discovers Android devices on LAN
- [x] `sashi wifi status` shows connected wireless devices
- [x] `sashi wifi logcat [tag]` streams logcat over WiFi
- [x] Works on Linux (lsusb) AND Termux (sysfs fallback)
- [x] No IDE required — pure terminal workflow

## Deliverables (DONE)
- `~/ollama-local/lib/sh/usb-monitor.sh` — USB detection library
- `~/ollama-local/lib/sh/wifi-debug.sh` — WiFi ADB library
- `~/ollama-local/sashi` v3.2.1 — usb/wifi/hf commands added
- `~/ollama-local/lib/sh/banner.sh` — restored (was 0 bytes)
- `~/ollama-local/lib/sh/aliases.sh` — restored with usb/wifi aliases

## Status: DONE — move to closed
Committed: 18770e6
Date completed: 2026-02-28
