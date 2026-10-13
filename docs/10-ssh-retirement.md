# Retiring the Fedora-to-Ubuntu SSH recovery server

**Final status: completed on 2026-10-13 (~04:06 CEST).** The owner explicitly authorized using the **existing local independent root GPU recovery watchdog** in place of the external Fedora SSH requirement, and indicated they would reinstall SSH if later needed. Both libvirt Windows guests were confirmed off *before* any inbound SSH service was disabled. No host or Windows reboot was performed.

## Why SSH originally existed

Earlier passthrough experiments could temporarily leave the GNOME graphical display unusable. A Fedora laptop authenticated over a separately available SSH session to the Ubuntu desktop to inspect Radeon/NVIDIA drivers, recover safely from PCI handoff problems, and supervise the one-time Wayland/GDM transition. Old `option-a-preflight.py` and `radeon-release-readiness.py` **required** both an active `ssh.socket` and a live Fedora connection before GPU detach.

OpenSSH was socket-activated on the Ubuntu desktop with inbound port 22. The outgoing `openssh-client` is a **different package**, needed for Git and future manual SSH commands; it was intentionally retained.

## Evidence that it was safe to retire the external login

1. The user chose **Windows > Power > Shut down** normally, without a forced timeout. Both `win11-physical` and `win11-physical-vfio-check` reached `shut off`.
2. Radeon `0000:0b:00.0` was restored to `amdgpu` and audio `0000:0b:00.1` to `snd_hda_intel`, while NVIDIA `0000:0c:00.0` remained the GNOME `nvidia` device.
3. Dell U4919DW reported HDMI2 (`0x12`), both Logitech receivers were on Ubuntu, Scarlett Solo was Ubuntu-owned and the original GNOME/Chromium/Chat On Steroids processes survived.
4. The independent recovery timer was inactive, its state marker was absent, ACL backup markers were cleared, and the Windows backing SSD remained unmounted. The qcow2 overlay and original physical SSD were not reset, written, or converted.
5. There were no current inbound Fedora SSH connections; source `/etc/ssh/` and the effective systemd SSH definitions were backed up locally under a root-only restricted backup directory, **not published to GitHub**.

## Replace the SSH precondition with verified local recovery, not with no recovery

Added `local_recovery_readiness.py` to the existing, local dual-GPU project and called its `ensure_local_recovery_ready()` from **both** the initial `option-a-preflight.py` and the last-moment all-process `radeon-release-readiness.py`. It is **read-only** and **fail closed**. It verifies:

- The actual root-installed `/usr/local/sbin/dual-gpu-option-a-recover` is a non-symlink regular executable, owned by root and not group/world writable, byte-identical to its reviewed source.
- The installed root recovery systemd `.service` and `.timer` are similarly root-owned, non-writable and byte-identical to the reviewed local source files.
- The service is loaded from the exact root unit path, has type `oneshot`, effective root user/group, exact recovery-helper `ExecStart`, is not currently running and has not failed.
- The timer is loaded from the expected root unit file, triggers **only** the recovery service, has the documented `OnActiveSec=120s` and `OnUnitActiveSec=60s` schedule, and reports healthy systemd state.
- **Idle:** no GPU handoff marker exists and the timer must be inactive. **In a handoff:** the marker is present and the timer must be active. Mismatches prevent a new GPU release.

The existing controller continues to arm the timer *before* protecting Radeon render-node ACLs and detaching either AMD PCI function. The independent root recovery helper continues to refuse GPU rebind if either Windows VM has not shut off. All other hardware, VM XML, GPU FD, Dell and storage checks are preserved. No SSH fallback was silently swapped for an unconditional success.

## A separate false failure found during the final graceful Windows shutdown

At ~03:58:59, while Windows was powering down normally, libvirt briefly returned **`in shutdown`**. The old daily controller treated any state other than `running`/`shut off` as fatal, so its systemd unit reported exit 1, although the independent root timer subsequently restored Radeon/ACLs, Dell HDMI2 and GNU/Linux input safely by ~03:59:46.

The daily and bounded wait loops were corrected to **wait** through `in shutdown` (without classifying it as `shut off`, and without adding a guest auto-shutdown deadline). Unexpected other states still fail closed. The finish path now reports recovery success only if the root marker was retired, both AMD PCI drivers are back, and the watchdog timer is inactive; it no longer incorrectly calls a deferred guest-state recovery a PASS. Error messages referring to the retired Fedora path were updated to use local console/physical Dell fallback. After confirming the idle system was safe, the previous systemd failure flag was cleared; the original log was preserved. This change passed offline state-transition tests, **not** a second live Windows shutdown after the edit.

## Recovery verification without SSH

- The root timer was **actually started and observed active** while both Windows domains and all GPU handoff markers were absent. The local idle readiness check intentionally rejected that unexpected active-timer state. The timer was stopped, and idle readiness passed again. This established that the independent root timer could be armed and retired without touching the GPU.
- **50 offline tests passed:** 38 prior focus/audio/Windows listener contracts and 12 new local-recovery, fail-closed and shutdown-state tests.
- Both the **full strict preflight** (`option-a-preflight.py --strict`) and the ordinary user's **read-only launcher check** (`switch-to-windows --check`) passed with `ssh.socket` stopped and no Fedora session. They both passed again **after package purging**.
- The guest was **not** started again to test a complete fresh post-SSH VFIO cycle. Previous live round trips and watcher recoveries remain the hardware evidence; this retirement adds strict no-SSH readiness proof, not a new Windows boot claim.

## Exact server retirement

Prior to removal, `apt-get -s purge openssh-server openssh-sftp-server` was checked to remove **only** those two server packages. No unrelated `apt autoremove` was executed.

1. Stopped and disabled `ssh.socket` and `ssh.service` with systemd while both Windows domains were off.
2. Rechecked full strict GPU preflight and desktop launch preflight with port 22 closed; both passed.
3. Purged **only** `openssh-server` and `openssh-sftp-server`; left `openssh-client` installed.
4. Verified `ssh.socket`/`ssh.service` were `not-found` and inactive, there was no `sshd` process, and TCP port 22 had **no listening socket**.
5. Found one non-package-owned server-only drop-in, `/etc/ssh/sshd_config.d/01-single-gpu-recovery.conf`, from the old Fedora access. Preserved a private root-only copy and removed that drop-in and its now-empty directory. No user SSH client configuration was removed.
6. Checked the same GNOME, Chromium, Chat On Steroids, NVIDIA display, Linux AMD drivers, Logitech input, Scarlett default playback and stopped Windows domains; all remained intact.

Private originals and the pre-change root helper/source scripts were retained under `/var/backups/dual-gpu-ssh-retirement-20261013/` (root-only permissions), **not** in this public repository. The earlier user-private compressed original dual-GPU source backup also remains outside Git.

## Security/recovery tradeoff and manual reinstall

With inbound SSH removed, there is **no Fedora remote recovery connection**. The verified local watchdog can restore AMD and ACLs after shutdown while independent systemd/root remains alive, but it **cannot guarantee remote access** if the entire host crashes or its graphical input becomes unusable. This reduced external recovery capability was explicitly accepted. The Dell physical input selector and local console remain the manual display options; choosing HDMI2 alone does not transfer Logitech USB ownership.

If inbound SSH is later needed, the user can manually reinstall OpenSSH server through Ubuntu's package manager (e.g. `sudo apt install openssh-server`) and review whether `ssh.socket` should be enabled. The prior private configuration backup exists for *inspection*, not blind unattended restoration. No recurrent server-install or deployment automation has been introduced.

## Offline Windows helper ISO label cleanup

While **both Windows guests remained shut off**, the existing read-only `UBUNTU_RETURN` tools ISO was preserved, unpacked, and rebuilt with **only** the manual fallback PowerShell script's now-obsolete Fedora SSH help text changed to reference the physical Dell input menu and **local Ubuntu console**. Its other 18 files were byte-for-byte unchanged. The guest XML still points to the exact canonical ISO path and the image remains read-only, `libvirt-qemu:kvm` owned. The original ISO checksum was `1bc3095810f72bea99c5bdf1265c65793bb14056f820842cb13f61c0ebafa8f9`; its preserved backup remains local. The new canonical ISO checksum was `7cc519aaa408993cea3397ecc7706b75b51036fb7e127ad8c5ec2f930cb45e63`.

This was **not** a Windows guest session, Windows-profile installer run, or VM disk edit. The copy of the fallback script already installed in the Windows user's profile may still display the historical Fedora SSH wording until a later **manual** reinstall; its COM1 operation is unchanged. No new guest boot is necessary for this cosmetic message update.
