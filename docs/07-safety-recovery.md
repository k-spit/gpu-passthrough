# Safety invariants and manual recovery boundaries

This is a record of checks and safe responses, **not** permission to bypass a failed preflight or force-reset hardware.

## Never cross these boundaries

- GNOME/Wayland, GDM, NVIDIA display and unaffected Ubuntu applications must not be stopped for routine Windows switching. The old single-GPU VFIO probe is unsafe here because it stops GDM.
- Radeon and HDMI-audio PCI must not be detached unless an exact, conservative `/proc/*/fd` scan proves zero AMD DRM clients under the same exclusive transition lock. Do not ignore ambiguous permission errors; only the proven read-only AppImage FUSE descriptor case is narrowly exempt.
- Do not rebind Radeon to Linux while either Windows VM owns it. The watchdog intentionally refuses unsafe rebind, retaining a marker for later exact recovery.
- Do not switch the Dell to DP without a safe return path. DDC must positively identify exact monitor and NVIDIA/Radeon I2C ancestry; monitor source observations alone do not authorize changing USB ownership.
- Never allow the guest to write to the native Windows SSD. The old NTFS/BitLocker backing must stay unchanged throughout the lifetime of its overlay. Never reset or commit the overlay without an explicit separate decision and backup.
- Never assume a random tab, hotkey text, prior PID, timed delay or stale VM state grants control authority. The live controllers use exact guest identities, markers, nonces and checked USB topology.
- No Windows networking was enabled. Secure Boot and host security restrictions remained in place. Do not bypass AppArmor to make a broken GPU handoff appear to work.

## Running Windows but showing Ubuntu

The Radeon remains bound to `vfio-pci`, root daily unit in progress, COM1 focus watcher and GPU recovery timer active. The Scarlett normally remains with Ubuntu unless explicitly toggled. **Do not** interpret an active recovery timer as a failed cleanup while Windows is deliberately running.

If the Windows hotkey fails, the guest has a desktop shortcut **Return to Ubuntu - keep Windows running** that sends a single COM1 request independent of the resident listener and Dell DDM. This still requires host root validation. Manually choosing HDMI2 on the Dell changes only display input, **not** ownership of Logitech keyboard/mouse; the monitor's physical menu alone is not complete recovery.

## After user shuts Windows down

The root controller detects guest off, restores both Radeon PCI functions and exact saved permissions, returns Scarlett if Windows borrowed it, selects Dell HDMI2, checks HDMI2 again after settling (12-second check), and retires its watchdog/marker only on a verified safe state. The historical acceptance covered full Windows->Ubuntu recovery without GNOME restart.

Read-only verification examples **on the originally configured Ubuntu host**:

```sh
virsh -c qemu:///system list --all
lspci -k -s 0b:00.0
lspci -k -s 0b:00.1
lspci -k -s 0c:00.0
sudo /usr/local/sbin/dual-gpu-option-a-focus --status
sudo /usr/local/sbin/dual-gpu-option-a-audio --status
systemctl show dual-gpu-option-a-recover.timer -p ActiveState -p SubState
sudo /usr/local/sbin/dual-gpu-option-a-ddc probe
```

Only when Windows is confirmed **shut off** is a manual HDMI-only return appropriate. A safe host-side input-only command exists as `sudo /usr/local/sbin/dual-gpu-option-a-ddc to-hdmi`, but it must not be mistaken for PCI or keyboard recovery. When a root handoff marker remains, investigate with logs and the idempotent guarded root recovery helper. Never force unloading VFIO or killing GDM.

## Fedora SSH retired after explicit recovery-policy decision

On 2026-10-13, after the **user** normally shut down Windows and both Radeon PCI functions/ACLs returned to Linux, the authenticated Fedora SSH prerequisite was replaced with a strictly verified **local independent root watchdog**. The shared read-only local recovery helper is called by *both* the first preflight and the last-moment Radeon zero-client gate. It checks exact root-installed helper/unit files, root ownership/permissions, systemd unit identity/status and correct watchdog timing/state. When no guest owns Radeon the timer must be inactive; during the handoff marker it must already be active. A broken, missing, unarmed or unexpectedly active recovery unit blocks GPU detach. The existing root watchdog still refuses to rebind hardware until both Windows guests are off.

The inbound OpenSSH server and its dedicated Fedora server drop-in were removed; the outgoing OpenSSH client remains. **Strict GPU preflight and the normal launcher's read-only check passed without the SSH socket, both before and after package purge.** No new guest was booted *during the retirement operation*. A separate later **2026-10-13 supervised Windows startup, bidirectional focus, graceful shutdown and full host recovery succeeded** under the local-watchdog model; see [acceptance evidence](09-acceptance-evidence.md).

The user explicitly accepted giving up independent **remote** Fedora rescue. A local root watchdog cannot fix a full host crash or inaccessible local console; do not imply it is an equivalent external access path. The physical Dell source menu and local Ubuntu console are still manual options, but selecting HDMI2 alone cannot reassign Logitech USB devices. See [SSH retirement](10-ssh-retirement.md).
