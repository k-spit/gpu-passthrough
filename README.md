# Ubuntu / Windows 11 dual-GPU passthrough: actual build record

**Status (2026-10-13):** this is the documented result of a working installation on one Ubuntu workstation, **not** an automated installer or reproducible deployment recipe. No GitHub Actions or setup automation is part of this repository.

## Preserved old repository

The earlier Ubuntu 19.10 / Windows 10 GPU passthrough tutorial, old screenshots, XML, and full Git history are unchanged on [archive/legacy-gpu-passthrough-2020](https://github.com/k-spit/gpu-passthrough/tree/archive/legacy-gpu-passthrough-2020), original commit `2f739b9c91d4e3532d6a5762c027ea04f2144551`. The preexisting `focus_feature` branch is untouched. The old 2020 VFIO device IDs, second-NVIDIA-GPU procedure, and initramfs hook are *not* the current setup.

## Current result

The NVIDIA GTX 1070 permanently owns Ubuntu's GNOME Wayland desktop on **Dell U4919DW HDMI 2**. The AMD RX 6900 XT plus HDMI audio is switched to an **offline** Windows 11 libvirt guest shown on the same Dell's **DisplayPort**. GNOME, Chromium, and Chat On Steroids keep running. Windows changes persist in a qcow2 copy-on-write overlay backed by a **read-only** physical Windows SSD.

With NumLock enabled:

| Hotkey | What happens |
| --- | --- |
| `Ctrl+Alt+NumPad1` | Display Ubuntu on HDMI 2 and return Logitech keyboard/mouse; **Windows stays running**. |
| `Ctrl+Alt+NumPad2` | Start/focus Windows on DP; transfer Logitech keyboard/mouse. |
| `Ctrl+Alt+NumPad3` | Independently toggle **Focusrite Scarlett Solo** USB audio between Ubuntu (initial owner) and a running Windows VM. |

**Audio does not follow screen focus.** Ubuntu music or Discord may continue while Windows is shown. The separate H570e microphone remains with Ubuntu. The correct Focusrite Windows audio driver was needed to eliminate crackling.

## Documentation

- [Scope, provenance and privacy](docs/00-scope-provenance.md)
- [Hardware and architecture](docs/01-architecture.md)
- [Chronology of changes and decisions](docs/02-timeline.md)
- [Installed configuration inventory](docs/03-configuration-inventory.md)
- [Manual implementation record](docs/04-manual-build-record.md)
- [Daily operation and hotkeys](docs/05-daily-operation.md)
- [Windows listener and audio implementation](docs/06-windows-hotkeys-audio.md)
- [Safety and recovery rules](docs/07-safety-recovery.md)
- [Failures and lessons](docs/08-incidents.md)
- [Verified acceptance and local evidence](docs/09-acceptance-evidence.md)
- [Recovery SSH decommissioning](docs/10-ssh-retirement.md)
- [Local source and configuration map](reference/source-inventory.md)

## Critical limitations

Never boot native Windows and modify the backing SSD while keeping the existing qcow2 overlay: a changed backing device makes the VM overlay unsafe. Windows VM changes do **not** write back to physical Windows. Never reset the overlay casually, force-rebind Radeon while a guest owns it, detach a device while Linux clients hold DRM nodes, or run the old single-GPU probe (it stops GDM).

**Public repo:** machine-unique SSD, monitor, USB serials, VM UUIDs, Fedora LAN addresses, secrets and raw logs are deliberately omitted. Original scripts, configs and evidence stay on the desktop. The original safety preflight depended on Fedora SSH; check [SSH retirement](docs/10-ssh-retirement.md) before assuming new Windows starts are still permitted after server removal.
