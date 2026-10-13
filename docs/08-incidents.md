# Incidents and lessons from the actual build

## 1. Original single-GPU probe interrupted GNOME

The old `single-gpu-vfio-probe.service` stopped GDM and thus closed working graphical apps. That conflicts with the user's core requirement. It is a historical probe, **not** the daily controller. Option A uses two GPUs and never stops GNOME to start Windows.

## 2. Nouveau crashed GTX 1070 graphics channels

`nouveau` logged GPU traps (including RT_HEIGHT_OVERRUN) and terminated a Chat On Steroids channel. Proprietary NVIDIA 580 with secure signed modules was installed and verified; it became the persistent GNOME GPU. Pascal GTX1070 does not use the NVIDIA open-kernel-module variant. Reverting to nouveau would reintroduce historical risk.

## 3. Mutter secondary Radeon hotplug failed

A prior mirrored NVIDIA HDMI + AMD DP Wayland configuration permitted initial detach/reattach, but Mutter later logged `Failed to hotplug secondary gpu ... ENODEV` and `device already present`. The kernel DP connector existed while GNOME no longer advertised it. A scoped udev add/change did not repair Mutter's internal GPU registry. Rather than patching Mutter, the user chose **Option A**: GNOME NVIDIA HDMI2 always; Radeon DP is Windows-only. The old incident is preserved locally in `MUTTER-HOT-REATTACH-INCIDENT.md`.

## 4. Chromium/COS retained AMD DRM render handles

Even with GNOME confined to NVIDIA, applications independently opened Radeon render nodes. Hard detach while these handles exist is forbidden. A temporary exact ACL guard and targeted app relaunch placed them on NVIDIA. After restoring original ACL, conservative scans passed. Avoid killing all Chromium/COS processes blindly during future app upgrades; if a new handle exists, **fail closed** and inspect its precise ownership.

## 5. AppImage FUSE inaccessible descriptor

The `/proc/*/fd` scanner initially failed with EACCES for read-only AppImage files that even root could not stat, owing to FUSE mount permissions. Scanner exception was restricted to **verified** read-only AppImage FUSE mount identity, target path, FD flags and mount namespace. Generalized `except PermissionError: continue` would hide real Radeon ownership and was rejected.

## 6. Dell transient auto-input selection

The Dell initially appeared to return HDMI2 after Windows shutdown but then reported DP once again. Six later paired reads stabilized on HDMI2. A delayed 12-second post-recovery HDMI2 re-read/return was added and separately tested on an already-safe host. The added delayed path was not retested with a third full Windows boot during its original installation; distinguish this from already-proven initial automatic return.

## 7. AppImage library shadowing `notify-send`

The COS AppImage injected incompatible GTK library environment values into the launcher, making `/usr/bin/notify-send` fail with a missing symbol. Notifications were invoked with a clean system-library environment. This was a cosmetic bug, not a failed VM handoff.

## 8. Windows Scarlett Solo crackling

The Scarlett Solo 3rd Gen. could be attached to Windows, but audio cracked until the user installed its **proper Windows driver**. Installing the driver fixed crackling but required a Windows reboot. This must not be confused with missing Radeon PCI HDMI audio; that PCI function was already passed to Windows.

## 9. Windows hotkey vanished after reboot

After the first driver reboot, there were no new COM1 hotkey events. Restarting Dell Display Manager did not help. The guest later shut down safely and host recovery passed. Fixes included no longer depending on Dell DDM for NumPad1 (host performs verified DDC), independent Windows per-user startup listeners, and explicit diagnostics.

## 10. Stale Windows PowerShell video listener

Replacing a script file while the old PowerShell process was alive left the old in-memory DDM calls running. New process exited because a named mutex was held. The targeted activation helper validates the exact video process executable/user/command/creation identity before stopping **only that listener**, starts a new one and verifies its fresh DDM-independent log. NumPad3 audio listener is left alone.

## 11. Destructive `HKCU Run` recreation

Both old Windows installers called `New-Item -Path $runKey -Force` on an existing *shared registry key*, which in the Registry PowerShell provider overwrites the key and clears old entries. Audio installation erased video autostart; earlier executions may also have erased unrelated startup entries. Fixed with narrow .NET `RegistryKey.SetValue`/`DeleteValue` and explicit comparison of other values plus current-key backup. **Do not invent or automatically restore unknown third-party startup entries**. The backup taken *after* the incident cannot undo already lost entries. User may need to review Windows Startup Apps.

## 12. Benign PTY error at Windows shutdown

When QEMU removed COM1 after graceful guest poweroff, termios cleanup raised EIO and caused an unnecessary watcher restart. This is now treated as expected **only after verified guest shutoff**; the same error while guest remains running still fails closed. Main GPU/audio recovery had already succeeded despite the benign error.

## 13. Fedora SSH replaced after normal guest shutdown

Fedora SSH was required for earlier dangerous GPU cutovers. The user later approved decommissioning that inbound server after both guests were off and Radeon was fully recovered. The strict initial preflight **and** last-moment Radeon release scanner now require an independently healthy root watchdog, exact helper/source identity and correct active-marker/timer state, instead of an authenticated Fedora session. Live SSH-independent readiness passed before and after purging the server packages. This removes external rescue ability, **not** the need for safe preflight. See [SSH retirement](10-ssh-retirement.md).

## 14. Libvirt transient normal shutdown misreported as failed daily run

While Windows was shutting down normally at 03:58:59, libvirt reported `in shutdown` rather than `running`/`shut off`. The old everyday root controller treated this as fatal and exited status 1; the independently armed root timer correctly waited for the real VM shutoff and then restored both Radeon PCI functions, ACLs and HDMI2. Its log is preserved. The revised wait loop tolerates that **transitional** state but still waits for *actual* `shut off`; it never forces guest shutdown. Recovery-completion log claims now also require marker retired, AMD Linux drivers restored and timer inactive. The fix initially passed offline transition tests; a **later real user-controlled Windows shutdown and full verified host recovery succeeded at 14:33-14:34** (see [acceptance evidence](09-acceptance-evidence.md)).

## 15. Ctrl+Alt+NumPad2 failed immediately after host reboot

Two early post-reboot shortcut requests passed hardware/overlay/watchdog preflight but stopped before GPU detach or Windows startup. The controller expected a Chromium main process even though the browser had not launched yet; its process lookup exited under shell `set -e` without a helpful blocker message. The revised controller accepts **no Chromium at a fresh login** while still requiring exact GNOME identity, rejecting ambiguous process lookups, and enforcing every independent Radeon DRM-client, storage, VM and watchdog check. The recovery helper understands the explicitly absent browser marker. The desktop launcher now distinguishes *startup requested* from *guest confirmed running*, with failure notification from the root service. These cold-login changes passed offline tests; the absent-Chromium case itself awaits another fresh-login hardware test.

## 16. Manual VM start bypassed live hotkey authority

After those failed requests, the same Windows VM was started manually through the virtualization GUI. That boot did not create the root controller's protected session marker or arm the required watchdog and COM1 focus watcher. The VM could display video, but bidirectional USB hotkeys correctly lacked verified authority. The fix is **not** to remove the authority checks: start a stopped guest through the existing guarded Ubuntu NumPad2/desktop launcher instead. A running guest without those safeguards now produces an explicit focus-blocked explanation.

## 17. Rebooted apps reopened Radeon render devices

Later in the Ubuntu session, Chat On Steroids, Chromium and inherited children held Radeon render-device descriptors, so strict detachment correctly failed closed. With user approval, a separate **SSH-free, one-time** application relaunch validated the local independent root watchdog, armed a timed root ACL rollback and user app-restore watchdog, saved Chromium session metadata, and relaunched both apps under clean NVIDIA-only graphics environments. The original GNOME process survived. A full process scan and strict preflight confirmed **zero Radeon clients**, even after the original ACL was restored. User-level launch preferences were installed for future Chat On Steroids/Chromium starts without changing GNOME, global GPU policy or the Snap package. These preferences are validated statically but **not yet tested across another host reboot**. The original Fedora-SSH-dependent historical relaunch scripts were preserved rather than reused unchanged.
