# Installed configuration inventory (as observed 2026-10-13)

These are path names and verified effective responsibilities, **not portable installers**. Some older experimental scripts are retained locally but not part of daily operations.

## Host OS and drivers

- Ubuntu 24.04, Linux kernel `7.0.0-38-generic` at final inspection; GNOME 46 Wayland, session seat0, host user session intentionally not restarted during daily switching.
- Signed proprietary NVIDIA 580.178.04 on GTX1070 (`0000:0c:00.0`); NVIDIA DRM KMS enabled, Secure Boot **enabled**. Do not install Pascal-incompatible `nvidia-driver-580-open` or switch back to unstable `nouveau`.
- RX6900 XT PCI `0000:0b:00.0` and HDMI audio `0000:0b:00.1` bind to `amdgpu`/`snd_hda_intel` when VM off, and both to `vfio-pci` while running.
- `/etc/udev/rules.d/61-mutter-preferred-primary-gpu.rules`: NVIDIA `10de:1b81` DRM card gets `mutter-device-preferred-primary`.
- `/etc/udev/rules.d/61-mutter-ignore-radeon-kms.rules`: Radeon `1002:73bf` DRM KMS card gets `mutter-device-ignore`; AMD render node/HDMI audio untouched. One-time GNOME relogin already completed.
- GNOME monitor layout saved under the user's `.config/monitors.xml`, originally verified as Dell 5120x1440 on NVIDIA HDMI2.

## Root controllers and systemd

| Installed file / unit | Verified role |
| --- | --- |
| `/usr/local/sbin/dual-gpu-option-a-run` | Strict guarded Radeon handoff and persistent Windows daily lifecycle (`--daily`); now tolerates transitional libvirt `in shutdown` while waiting for exact guest-off without auto-shutdown |
| `/etc/systemd/system/dual-gpu-option-a-daily.service` | Independent root `oneshot` invoking `...-run --daily`, `TimeoutStartSec=infinity` |
| `/usr/local/sbin/dual-gpu-option-a-recover` | Conditional root host PCI/ACL/audio/HDMI2 recovery, refuses running guest rebind |
| `dual-gpu-option-a-recover.service` and `.timer` | Recovery unit; timer armed only during handoff, root retry independent of desktop/UI |
| `/usr/local/sbin/dual-gpu-option-a-ddc` | Exact Dell identity/ancestry-checked input read/HDMI2/DP1 operations |
| `/usr/local/sbin/dual-gpu-option-a-focus` | Offline Windows COM1 watcher and live Logitech + Dell focus switching |
| `dual-gpu-option-a-focus-watch.service` | Root watcher with bounded failure restart |
| `/usr/local/sbin/dual-gpu-option-a-audio` | Independent Scarlett USB transfer and PipeWire default playback restoration |
| `option-a-preflight.py` | Read-only exact VM/GPU/disk, Wayland, Mutter ignore and verified **local** recovery checks; Fedora SSH prerequisite removed after user approval |
| `local_recovery_readiness.py` | Read-only root-owned systemd helper/timer identity, integrity and handoff marker/armed-state gate shared by first and final release preflights |
| `radeon-release-readiness.py` | Last-moment all-process DRM FD zero-client gate and **second local recovery timer gate**; conservative read-only FUSE exception |
| `option-a-display-check.py` | Live GNOME HDMI-only logical monitor check |

Source copies are under the owner's local dual-gpu project folder. Installed root helpers were compared byte-for-byte with sources after the 2026-10-13 SSH retirement. The **original** source hash inventory is at `reference/source-inventory.md`; the **post-retirement** snapshot is at `reference/source-inventory-after-ssh-retirement.md`. The inbound OpenSSH server, SFTP server and their dedicated Fedora-only server drop-in were removed, while `openssh-client` remained installed.

## User-facing programs and monitor

- Trusted Ubuntu desktop shortcut `~/Schreibtisch/dual-gpu-switch-to-windows.desktop` plus GNOME application-menu launcher `~/.local/share/applications/dual-gpu-switch-to-windows.desktop`.
- User command `~/.local/bin/switch-to-windows` with `--start`, read-only `--check` and `--status`; the launcher starts a fixed root service asynchronously and rejects duplicate handoffs.
- Ubuntu hotkeys `Ctrl+Alt+KP_1`, `KP_2`, `KP_3` registered with GNOME. Real keys must be number-pad keys with NumLock on.
- Dell U4919DW HDMI2 `0x12`, DisplayPort1 `0x0f`; monitor input via DDC/CI `0x60`, Ubuntu NVIDIA-connected I2C path. A 12-second delayed HDMI2 recheck handles observed Dell transient source changes.

## Windows guest helpers

An existing read-only ISO labeled `UBUNTU_RETURN` is provided to the **offline** guest. It contains separate Windows per-user PowerShell hotkey listeners for NumPad1/2 (display/input) and NumPad3 (Scarlett audio), plus diagnostic, repair and manual return tools. Windows `HKCU Run` and Startup-folder entries are both installed and use process mutexes to prevent duplicates. The safe current version writes only its own Run values; old destructive install versions are documented under incidents.

## Native Windows storage

The guest COW path is `/var/lib/libvirt/images/win11-physical-safety-overlay.qcow2`. The backing Windows Samsung 970 EVO Plus 1TB block device must remain **unmounted/unchanged** and QEMU `O_RDONLY`. Its full EUI by-id path is intentionally omitted publicly. Do not clone/publish actual VM XML with embedded unique IDs without review.

### Post-retirement Windows helper media

The source `windows-focus/Return-Ubuntu-Without-Shutdown.ps1` and canonical read-only `UBUNTU_RETURN` optical image now describe the **local Ubuntu console** rather than the removed Fedora SSH service. Only that source file changed in the 19-file ISO; the canonical helper path, guest XML, source storage, existing Windows-profile-installed listener binaries and VM overlay were unchanged. A future deliberate in-guest repair could refresh the user's installed fallback wording, but no Windows boot was performed for this cosmetic change.
