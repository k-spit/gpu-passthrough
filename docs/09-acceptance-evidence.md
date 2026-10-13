# Actual acceptance evidence and its limits

The full unredacted logs are **local**, not copied into this public Git repository. They reside in the existing dual-GPU project's `evidence/` directory. Exact hardware/guest identities and private connection information are in those local records.

| Evidence (local filename) | What it proved |
| --- | --- |
| `option-a-20261013T012324-detach-only.log` | Radeon+HDMI audio VFIO detach/8-second hold/rebind with same GNOME/Chrome and NVIDIA HDMI2. |
| `option-a-20261013T012435-windows.log` | First actual Windows guest start, exact PCI+USB passthrough, QEMU physical SSD read-only and qcow2 writable; user-confirmed Windows video/input; graceful recovery. |
| `option-a-ddc-switch-20261013T013356.log` | Real independent HDMI2 -> DP1 -> HDMI2 DDC switching without guest, root time-bounded recovery. |
| `option-a-20261013T013742-daily.log` | Actual installed Ubuntu desktop launcher started offline Windows using preserved overlay; DDC selected DP; test-only ACPI shutdown, host Radeon/ACL/GNOME recovered. |
| `option-a-recovery.log` | Conditional root recovery attempts, original ACLs, Dell HDMI2, marker/watchdog retirement. |
| `live-focus-20261013-acceptance.md` | Initial live display/Logitech focus acceptance evidence. |
| `option-a-audio-20261013-live.md` | Real Scarlett USB live-attach to the running VM and return to original Ubuntu PipeWire default sink; H570e unaffected; marker cleared. |
| `windows-hotkey-postreboot-20261013.md` | COM1/DDM-dependency investigation, Windows listener and registry bug fix, separate post-reboot listener autostart and host-driven NumPad1 return. |
| `MUTTER-HOT-REATTACH-INCIDENT.md` | Failing Radeon secondary GPU re-registration was **not** fixed; explains Option A choice. |
| `nvidia-580/ROLLBACK.md`, `baseline.txt`, `install.log` | Historical proprietary NVIDIA installation and rollback/signed-driver verification. Logs remain private. |

## Final live cross-check (2026-10-13 around 03:39 CEST)

The user supplied Windows `Check-Live-Hotkeys.cmd` output **after a Windows-only restart**: video listener PID 10924 ready ~03:37:54, audio PID 10580 ready ~03:37:52. Both showed installed script, Startup shortcut and **HKCU Run: True**, one resident listener each, with final `PASS: Both Windows hotkey listeners are running with redundant logon startup.` Duplicate launch attempts were blocked by the named mutex.

The Ubuntu host independently logged an exact Windows COM1 NumPad1 request **03:39:16**, completed verified Dell HDMI2 `0x12` + both Logitech receiver return **03:39:23**, and then stable Ubuntu focus **03:39:31**. Same `win11-physical-vfio-check` guest **continued running**, Radeon+audio PCI remained VFIO, Scarlett stayed Ubuntu default. GNOME Shell PID 21358, Chromium PID 23563 and Chat On Steroids PID 23356 survived these cycles. Those PIDs are historical acceptance evidence, **not** reusable authority constants.

## Automated unit test scope versus real hardware

By the final Windows repair, 29 offline host focus/audio tests plus 9 additional Windows-script contract tests were passing (**38 total**). Those are source validations and do not replace human-verified Windows video/input/audio. Separate live Scarlett USB attach/detach passed with guest running and no display/keyboard change. Scarlett audible crackling was corrected by the user's Windows vendor driver installation; complete audible sound testing was **not** repeated after the final reboot. The 12-second delayed Dell HDMI retry was separately tested synthetically, not exercised in a third full Windows run immediately after installation.

## State after last accepted focus test

The original Windows VM was still running in the background, Dell HDMI2 showed Ubuntu, Logitech receivers and Scarlett were on Ubuntu, independent GPU recovery watcher/timer remained active (expected while VM owns Radeon), and unrelated Ubuntu graphical applications were alive. That is **not** the same as a fully idle host; AMD PCI was still assigned to VFIO.

Tests never authorized converting the Windows native SSD to direct-write, resetting/committing qcow2, enabling virtual NIC networking, patching Mutter, installing a generalized automatic redeployer, or restarting GDM during daily switching.
