# Fedora-to-Ubuntu SSH recovery: original role and retirement

**This page is a record of the actual status and the safety blocker, not an instruction to disable live recovery carelessly.** The user requested removing the Ubuntu SSH *server* installed for the Fedora laptop. The client-side SSH program is useful for Git/GitHub and must remain installed.

## Why the server was installed

During early Radeon passthrough tests, Ubuntu GNOME or its display output could disappear. The Fedora laptop authenticated over SSH to the Ubuntu desktop to verify PCI drivers, libvirt, GDM, exact ACLs and independent root recovery without requiring a functional display. This path was a safety prerequisite for the one-time GNOME relogin and first VFIO detach.

The host originally had OpenSSH `sshd` started through socket-activated systemd (`ssh.socket`, listening on TCP 22). Ubuntu's `openssh-client` is a separate **outgoing** program; removing `openssh-server` does not require removing the client.

## Actual inspection before removal (2026-10-13 ~03:44 CEST)

- `openssh-server` and `openssh-sftp-server` installed (Ubuntu 24.04); `openssh-client` also installed.
- `ssh.socket` **enabled and active**, `ssh.service` **active**, IPv4/IPv6 TCP port 22 listening.
- **No active Fedora SSH client session** at the point of inspection. Local GNOME session remained Wayland seat0.
- `ufw` reported **inactive**; no active UFW SSH rule removal was needed.
- The **exact Windows VFIO guest was still running** in the background. Radeon PCI GPU/audio remained `vfio-pci`; Logitech receivers and Scarlett were on Ubuntu, Dell HDMI2.

## Critical dependency discovered

`option-a-preflight.py` currently requires BOTH an active `ssh.socket` and an authenticated live Fedora SSH login before approving a new Radeon handoff. `radeon-release-readiness.py` also includes this gate. Removing the OpenSSH server therefore intentionally causes the next Windows *start from an idle host* to **fail closed** until the recovery prerequisite is separately redesigned. This is not a reason to quietly bypass the gate or claim a new Windows session would work without independent recovery.

The already-running guest can still use COM1 NumPad1/Ubuntu NumPad2 hotkeys and independent root recovery watchdog while the host remains healthy. But deleting the external SSH path during active VFIO removes the fallback used in original safety tests. It should be retired only when the Windows guest has been gracefully shut down, Radeon drivers/ACLs are back on Ubuntu and the root recovery timer is inactive.

## Safe retirement conditions

1. User shuts down Windows **normally**, without an imposed deadline. Both libvirt Windows domains report shut off.
2. Radeon `.0` binds to `amdgpu` and `.1` to `snd_hda_intel`; NVIDIA keeps GNOME HDMI2. Exact root transaction markers are cleared and independent GPU recovery timer is inactive.
3. Backup the existing `/etc/ssh/` and the service's effective state into a local, access-restricted (not GitHub) file. Check `apt-get -s purge openssh-server openssh-sftp-server` for unrelated packages before doing any removal; **keep openssh-client**.
4. Stop/disable the **server** and socket activation; purge only the server packages if the dependency simulation is clean. Do not run broad `apt autoremove` or delete unrelated keys/accounts.
5. Verify no process listens on TCP 22, both OpenSSH server packages are absent, Ubuntu SSH *client* remains, and GNOME/other desktop applications are still running.
6. Record actual results (or an explicit blocker) here. Do not pretend the pre-existing strict VM-start preflight will still pass after SSH retirement; decide separately whether to provide another independent recovery channel before future GPU handoffs.

**No recurring cleanup automation, firewall broadening, or silent guest shutdown is authorized.** The absence of inbound SSH changes the security/recovery tradeoff; it does not improve the correctness of GPU transitions.

## Removal readiness check at ~03:55 CEST (no service was changed)

A read-only `apt-get -s purge openssh-server openssh-sftp-server` simulation showed **only those two packages** would be purged. `openssh-client` would remain installed and functional for outbound SSH/Git. The simulation also printed unrelated old autoremove candidates, but **none** should be autore-moved as part of this task. `ss` still showed `sshd`/systemd on port 22, and no active Fedora SSH clients.

**Actual removal status: BLOCKED / NOT EXECUTED.** The exact Windows VM was still running under Radeon VFIO and the independent root GPU recovery timer was armed. Removing the external recovery server now would discard the historical rescue path in mid-handoff. The existing strict preflight also explicitly requires a live Fedora SSH session for *future* Windows starts, so removing the server without a separately approved replacement makes the daily launch fail closed. Do not silently modify that authorization/safety gate. Shutdown of the guest must remain user-controlled.
