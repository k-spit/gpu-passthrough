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
| `post-reboot-cold-login-regression-20261013.md` | Two failed early post-reboot starts, corrective cold-login controller changes, guarded application relaunch and subsequent successful end-to-end Windows cycle. |
| `radeon-acl-app-relaunch-20261013T142353.log`, `app-nvidia-restart-20261013T142353.log` | User-approved independent-root/user recovery guards, browser session preservation, no Radeon process handles after restart, successful strict GPU preflight. |
| `option-a-20261013T142828-daily.log` | Later guarded Windows hotkey startup, exact read-only source/writable qcow2 FD proof, DP selection, user-controlled guest shutdown and independent root recovery. |
| `MUTTER-HOT-REATTACH-INCIDENT.md` | Failing Radeon secondary GPU re-registration was **not** fixed; explains Option A choice. |
| `nvidia-580/ROLLBACK.md`, `baseline.txt`, `install.log` | Historical proprietary NVIDIA installation and rollback/signed-driver verification. Logs remain private. |

## Final live cross-check (2026-10-13 around 03:39 CEST)

The user supplied Windows `Check-Live-Hotkeys.cmd` output **after a Windows-only restart**: video listener PID 10924 ready ~03:37:54, audio PID 10580 ready ~03:37:52. Both showed installed script, Startup shortcut and **HKCU Run: True**, one resident listener each, with final `PASS: Both Windows hotkey listeners are running with redundant logon startup.` Duplicate launch attempts were blocked by the named mutex.

The Ubuntu host independently logged an exact Windows COM1 NumPad1 request **03:39:16**, completed verified Dell HDMI2 `0x12` + both Logitech receiver return **03:39:23**, and then stable Ubuntu focus **03:39:31**. Same `win11-physical-vfio-check` guest **continued running**, Radeon+audio PCI remained VFIO, Scarlett stayed Ubuntu default. GNOME Shell PID 21358, Chromium PID 23563 and Chat On Steroids PID 23356 survived these cycles. Those PIDs are historical acceptance evidence, **not** reusable authority constants.

## Automated unit test scope versus real hardware

By the final Windows repair, 29 offline host focus/audio tests plus 9 additional Windows-script contract tests were passing (**38 total**). Those are source validations and do not replace human-verified Windows video/input/audio. Separate live Scarlett USB attach/detach passed with guest running and no display/keyboard change. Scarlett audible crackling was corrected by the user's Windows vendor driver installation; complete audible sound testing was **not** repeated after the final reboot. The 12-second delayed Dell HDMI retry was separately tested synthetically, not exercised in a third full Windows run immediately after installation.

## New 2026-10-13 no-SSH retirement evidence (~04:00-04:06 CEST)

The owner gracefully shut down Windows. Both domains became `shut off`, Radeon GPU/audio returned to `amdgpu`/`snd_hda_intel`, NVIDIA/GNOME PID persisted, USB input and Scarlett stayed on Ubuntu, Dell VCP `0x60=0x12`, root recovery timer and transaction markers were retired. The Windows qcow2 overlay had grown to approximately **58 GiB**; its data were preserved, not reset or exported to GitHub.

The old daily controller reported an intermediate `in shutdown` as failure; the independent root watchdog correctly completed recovery by 03:59:46. The code now waits through this transitional state; no real guest reboot/shutdown was repeated after that fix.

The new local root recovery helper passed idle readiness, strict unit/source/service/timer integrity checks and an actual safe timer arm/disarm smoke while both VM domains were off. An active timer **without** a marker was correctly rejected by the idle gate. There were **50 passing offline tests**: original 38 plus 12 targeted local recovery/watchdog/shutdown tests. The full strict preflight and normal launcher `--check` both returned PASS with inbound SSH disabled and again after the SSH server package purge, including the last-moment zero-Radeon-client scan. No guest boot was performed during SSH retirement; this is **preflight validation**, not a new full hardware round trip.

OpenSSH server and SFTP server packages were purged, TCP port 22 closed, no `sshd` process, and outgoing `openssh-client` remained. The dedicated prior Fedora SSHD drop-in was backed up and removed. Local scripts, raw logs and private `/etc/ssh` backups were retained on the workstation, not posted publicly.

## Latest post-reboot live acceptance (2026-10-13 around 14:28-14:34 CEST)

After the guarded application relaunch, **65 offline tests passed** (previous 50, nine cold-login/startup safety tests and six app-relaunch/launcher contracts). The latest strict root readiness and normal desktop launcher checks passed with no AMD DRM clients. The running GNOME Wayland instance was preserved throughout.

An actual **Ubuntu NumPad2** at approximately **14:28** started the existing Windows guest through the supervised daily controller. Both AMD PCI functions moved to VFIO; the live QEMU process was verified to open the original physical Windows SSD **read-only** and the preserved qcow2 overlay **read/write**. Dell DisplayPort was selected, the independent root recovery timer armed and the exact offline COM1 focus watcher started. Windows kept running without an automatic daily shutdown deadline.

Windows **NumPad1** sent a valid guest/session-bound COM1 request at approximately **14:29:31**. By **14:29:39** the Ubuntu host had selected and verified Dell HDMI2 and returned both Logitech receivers while the *same Windows guest continued running*. Ubuntu **NumPad2** then positively verified the current protected guest, selected DP and returned both USB receivers to Windows without launching another guest. Additional NumPad1/NumPad2 transitions were observed. Occasional Dell DDC reads were temporarily uncertain; the watcher blocked those observations rather than treating them as USB-transfer consent, and subsequent explicitly authorized switches completed.

The user shut Windows down normally at approximately **14:33:27**. The root recovery path restored AMD graphics/audio drivers, the original GPU and physical-source SSD access controls, the borrowed input state, and Dell HDMI2 with its delayed confirmation. The original GNOME and Chromium processes survived; transaction markers and recovery timer were retired. The main daily service completed **status 0 at 14:33:47** without stopping GDM. Both Windows domains were off, Logitech/Scarlett were Ubuntu-owned and the normal strict preflight passed again afterward. This establishes a successful **SSH-free startup, bidirectional focus and graceful shutdown/recovery round trip**, not merely synthetic tests.

The Windows Scarlett audio **NumPad3** toggle was not independently exercised again during this particular cycle; earlier live audio round trips are the evidence for that feature. At the end of this successful guest session, the newly installed per-app NVIDIA launch preferences had **not yet** been tested by a further host reboot; their later negative result is recorded below. No guest image, disk backing, native Windows SSD, Secure Boot or host security changes were made as part of this acceptance.

**Later negative reboot acceptance (~14:39-14:44 CEST):** Ubuntu was rebooted again. Newly started Chat On Steroids and Chromium opened Radeon render-node descriptors even though their NVIDIA-preferring launchers were installed and verified unchanged. The strict scanner blocked another handoff with active AMD DRM clients. Both Windows guests were off and the host continued running on NVIDIA; no second VM launch was forced. The earlier full guarded cycle is a **pass for that actual session**, not a proof that app-launch hints alone guarantee repeatable startup after every host reboot. See [incident 18](08-incidents.md).

## Earlier state after the ~03:39 focus test

The original Windows VM was still running in the background, Dell HDMI2 showed Ubuntu, Logitech receivers and Scarlett were on Ubuntu, independent GPU recovery watcher/timer remained active (expected while VM owns Radeon), and unrelated Ubuntu graphical applications were alive. That is **not** the same as a fully idle host; AMD PCI was still assigned to VFIO.

Tests never authorized converting the Windows native SSD to direct-write, resetting/committing qcow2, enabling virtual NIC networking, patching Mutter, installing a generalized automatic redeployer, or restarting GDM during daily switching.

The post-retirement tools-CD update was performed while both guests were **off**, replacing only one read-only helper ISO PowerShell file's obsolete SSH guidance; all other 18 files remained identical and the canonical optical-media XML path was unchanged. No Windows profile data or native backing SSD contents were touched. This was a static media integrity check, not an extra guest acceptance.
