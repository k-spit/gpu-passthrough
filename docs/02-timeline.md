# Chronology: original experiments to accepted switching

All times are local Central European Summer Time, 2026-10-12/13. The record describes actual observed work rather than an executable playbook.

| Phase | Observation / action / decision |
| --- | --- |
| Baseline | Old single-GPU VFIO probe stopped GDM and terminated graphical apps, incompatible with the user's preservation requirement. Dedicated GTX1070 chosen for the Ubuntu graphical session. |
| Early NVIDIA testing | `nouveau` triggered channel traps in Chat On Steroids. Signed proprietary NVIDIA driver 580 was installed; Secure Boot retained. A reboot/user login transition was supervised. |
| Wayland/Mutter | GNOME 46 on GTX1070 HDMI2; AMD KMS excluded using narrowly scoped `mutter-device-ignore`; NVIDIA tagged preferred-primary. One explicitly approved GNOME restart activated rules. No routine restart thereafter. |
| Radeon DRM clients | Chrome/COS initially retained AMD render-node handles; a guarded app relaunch put them on NVIDIA. Readiness gate inspected every process; read-only FUSE AppImage FDs were carefully distinguished from unsafe inaccessible DRM handles. |
| First AMD PCI detach | AMD GPU and audio successfully detached to `vfio-pci` with original GNOME/Chrome running, then reattached to Linux drivers and restored ACLs. |
| Original Mutter reattach incident | With Radeon DP managed by GNOME, Mutter logged `ENODEV` and `device already present`, failed to restore its DP output logically after rebind. Adopted **Option A** instead of patching Mutter. |
| 01:23 | Final Option A Radeon-only detach/reattach passed with NVIDIA HDMI2 GNOME identity intact. |
| 01:24 | First actual Windows guest acceptance: user could log in and operate screen/mouse/keyboard. Radeon+audio PCI and Logitech USB passed through; physical Windows SSD verified read-only and qcow2 writable. Graceful shutdown and root host recovery passed. |
| 01:33 | Dell DDC reversible HDMI2 -> DP1 -> HDMI2 smoke passed with independent root return watchdog. |
| 01:37-01:39 | Real desktop-launcher daily Windows session used persistent overlay; DDC selected DP1 automatically. Bounded *test-only* host ACPI shutdown followed by correct Radeon/ACL/HDMI2 recovery and original GNOME/Chrome PIDs. A 12-second delayed HDMI2 recheck was then installed and tested synthetically. |
| 02:06 onward | Added user-requested live Ctrl+Alt+NumPad1/2 system focus. Windows stays running; offline COM1 host watcher binds intent to exact guest and moves keyboard/mouse with verified Dell source. |
| 02:40-02:47 | Added independent NumPad3 live-only Scarlett USB audio move and Ubuntu default sink restoration; H570e mic remained Linux. User installed Focusrite Windows driver after crackling playback; driver fixed output but required guest reboot. |
| Guest reboot incident | First Windows reboot left live hotkeys unavailable despite DDM restart. User gracefully shut down; Radeon+audio returned cleanly. Host COM1 records showed no guest requests following reboot. |
| 03:12 | Host-controlled Dell HDMI2 path accepted Windows COM1 NumPad1 without needing Dell Display Manager and returned Logitech receivers, leaving Windows running. |
| 03:25 | Observed a stale PowerShell listener still executing old DDM calls after a file update; secondary listener was blocked by mutex. Added precise owner/PID/creation-time replacement with fresh ready-log verification. |
| 03:27-03:34 | Found Windows installer registry bug: two `New-Item -Force` calls recreated same HKCU Run key, erasing video startup entry and possibly unrelated entries. Corrected named per-value .NET registry writes, preservation verification, current-key backup. |
| 03:37-03:39 | **Windows-only reboot acceptance passed**. Video and audio listeners auto-started, both HKCU Run and Startup shortcuts verified. Windows COM1 NumPad1 at 03:39:16; host returned HDMI2+Logitech at 03:39:23; **same Windows VM stayed running**, original GNOME/Chrome/COS survived. |

The raw chronological evidence and explicitly unresolved caveats are indexed under [acceptance](09-acceptance-evidence.md) and [incidents](08-incidents.md). The project contains experiments and discarded approaches; those are history, not production steps.
