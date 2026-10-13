# Windows keyboard helper, offline COM1 and independent USB audio

## NumPad1: host-led focus return

An existing offline ISA COM1 serial device carries one-shot NumPad1 messages from Windows. The Windows helper does not need to run Dell Display Manager. The Ubuntu root focus watcher verifies a running **exact** libvirt guest, current session identity, guest ownership of **both** Logitech receivers, root recovery protection, and GNOME/NVIDIA state. It allows Ctrl/Alt/key-up before moving input, uses DDC over NVIDIA HDMI to select and verify the Dell's `0x12` HDMI2 input, then releases only the receivers to Ubuntu via **live** libvirt USB changes.

A spontaneous Dell input switch is **not permission** to move keyboard/mouse. A stale serial message, duplicate nonce, absent authority marker, changed guest identity, partial USB ownership, unrecognized DDC state or stopped guest must block the request. Windows remains running with RX6900 assigned VFIO. Ubuntu NumPad2 reassigns both USB receivers to the same Windows VM and selects DP1; Windows-side NumPad2 is a no-op while it already shows Windows.

## NumPad3: no automatic audio follow

Focusrite Scarlett Solo (3rd Gen.) USB `1235:8211` is Ubuntu's default PipeWire analog-stereo playback. The exact USB serial is validated locally but is omitted publicly. NumPad3 tells a separate root controller to *live attach* Scarlett to the existing Windows guest at reserved USB port 4; it does not change the persistent guest XML, GPU PCI, monitor, keyboard or VM power state. A root-only active marker ties the move to exact guest/session/USB/sink identities. Pressing again detaches only Scarlett and restores the exact original Ubuntu default sink. The independent Logitech H570e microphone stays with Ubuntu. Audio returns on graceful Windows shutdown if still guest-owned.

Windows PCI HDMI audio `0000:0b:00.1` was already passed with the Radeon, but the physical **Scarlett USB** device is the desired playback path. The user observed crackling before installing the vendor Scarlett Solo 3rd Gen. Windows driver; driver installation eliminated that problem and required reboot.

## Guest helper files and launch registration

The guest's offline read-only `UBUNTU_RETURN` CD carries individual PowerShell listeners and per-user installers for video (`Live-Focus-Windows.ps1`) and audio (`Audio-Toggle-Windows.ps1`) plus `Repair-Live-Hotkeys.cmd`, `Check-Live-Hotkeys.cmd`, and the safe manual no-shutdown return. Windows PowerShell may block directly invoked unsigned scripts; `.cmd` launchers use a **single-process** execution-policy bypass, not a permanent system-wide policy relaxation. User Startup-folder shortcuts **and** per-user `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` entries provide redundant logon startup. Independent named mutexes ensure duplicate launch attempts exit without taking over the other listener's hotkeys.

When a script is updated, the prior running PowerShell process may retain old logic. The repaired video-only activation helper checks exact script path, executable, user/domain and process creation identity before stopping only that listener, then requires a new DDM-independent readiness log. The NumPad3 listener is separate and is not restarted by that helper.

## Corrected Windows registry safety bug

An earlier version of **both** Windows installers called `New-Item -Path $runKey -Force` on an existing shared `HKCU Run` key. Microsoft documents that this **replaces** that registry key with an empty key, clearing its values. Installing the audio listener after video therefore erased video's startup entry; unknown third-party per-user startup entries may also have been lost. The repaired installers instead use .NET RegistryKey.OpenSubKey/CreateSubKey as needed, SetValue/DeleteValue on *only* allowed names (`DualGpuLiveFocus`, `DualGpuAudioToggle`), and verify all pre-existing unrelated value names, types and data are preserved. Before repair they export the **current** Run key under `%LOCALAPPDATA%\DualGpuLiveFocus\registry-backups\`. That snapshot cannot recover entries already erased by the old version. Do not invent missing third-party values.

## Windows reboot acceptance

Following the corrected registration, Windows-only reboot at ~03:37 CEST started both listeners: video PID 10924, audio PID 10580, both verified `HKCU Run: True`, Startup present and one active process. Checker printed PASS. A fresh Windows NumPad1 request crossed host COM1 at 03:39:16 and host HDMI2+Logitech return finished 03:39:23 with the same Windows guest still running. Windows audio listener startup was proven after reboot; the full audible Scarlett playback sequence was not repeated in that final test, though earlier hardware audio round trips passed.
