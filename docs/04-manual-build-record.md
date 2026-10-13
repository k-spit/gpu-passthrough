# Historical, manually supervised build and validation sequence

**This page documents what was done, not a runnable setup script.** Ordering, exact identity checks, and the distinction between historic experiments and final configuration are essential. Repeating these privileged steps on a different host without a separate design is unsafe.

## 1. Inspect and prepare the system

Confirmed both GPUs, exact IOMMU group membership, Linux DRM nodes, connected Dell HDMI/DP cabling, native Windows SSD and BitLocker/EFI signatures, libvirt guest XML, original Wayland/X11 session and original process identities. Backups and logs were captured first. Protected Ubuntu desktop apps and the still-running graphical session were treated as state that must survive.

The existing root filesystem was LUKS encrypted, Secure Boot stayed enabled, the NVIDIA proprietary 580 driver was installed/signed for Pascal GTX1070, and the host retained a working Ubuntu display on HDMI2. This process included a reboot for driver activation and later a **one-time**, user-authorized new GNOME Wayland login. Neither is required for routine VM launches.

## 2. Fix GNOME GPU ownership

A udev rule marked GTX1070 as Mutter's preferred KMS card and the exact Radeon RX6900 KMS card `mutter-device-ignore`. The rule excludes only AMD's KMS card, not Radeon render nodes or the AMD HDMI audio function. GNOME's Dell logical layout was pinned to NVIDIA HDMI only (5120x1440). Historical screenshots and an original monitor XML snapshot were saved locally before changing it.

A first driver detach/return under the old mirrored arrangement exposed Mutter's broken secondary-GPU hot re-registration. The preferred final **Option A** avoided relying on that hotplug path. No Mutter binary/source was patched; do not re-enable the old mirrored Radeon DP layout.

## 3. Prove Radeon unused before detaching

The initial `/proc/*/fd` check found GNOME and applications holding Radeon DRM nodes. A carefully saved ACL guard prevented new AMD render opens while relevant user apps were relaunched on NVIDIA. The exact previous ACL was restored. FUSE/AppImage read-only descriptor permission errors were distinguished by specific mount identity, filesystem, and FD flags; unexplained `EACCES` remained a hard block.

The strict preflight repeated this exact Radeon FD zero-client gate **under the handoff lock** so that process changes cannot race a PCI release. When any client holds Radeon DRM, the correct result is refuse startup, not kill applications blindly.

## 4. Validate PCI transition and independent recovery

Both AMD PCI functions (`0000:0b:00.0`, `.1`) were temporarily detached to `vfio-pci` without stopping GDM; NVIDIA/GNOME/Chrome stayed alive. After short hold, they returned to `amdgpu` and `snd_hda_intel`; GPU/render and disk ACLs were restored exactly. The independent root systemd timer and transaction marker were tested. It must never rebind AMD while a libvirt Windows VM still owns the GPU.

This was proven in a driver-only acceptance **before** any Windows display test. Old `single-gpu-vfio-probe.service` and other one-time GNOME cutover utilities remain **historical and unsafe for daily switching**.

## 5. Boot and test the correct Windows guest

The existing `win11-physical-vfio-check` libvirt domain was started under `qemu:///system`, using both Radeon PCI functions, the exact two Logitech USB devices, offline NIC, no virtual VGA and a read-only helpers CD-ROM. QEMU's live FDs were checked to prove the physical Samsung native Windows SSD was `O_RDONLY` and the persistent qcow2 overlay was `O_RDWR`.

The user saw the actual Windows desktop, logged in, and confirmed mouse and keyboard. A separate bounded acceptance session requested graceful ACPI shutdown, and independent recovery returned AMD functions, ACLs, GNOME process identity and HDMI2. This was **test mode**: daily mode later intentionally removed any automatic Windows shutdown timeout.

## 6. Monitor DDC/CI and daily launcher

Dell U4919DW was positively identified through both NVIDIA HDMI and Radeon DP. VCP `0x60` was tested with `0x12` HDMI2 and `0x0f` DP1. A root watchdog guarded a brief DP/HDMI smoke test. After success, the daily root service was installed, with Ubuntu desktop/application-menu launcher and duplicate submission lock. An integrated desktop-launcher-to-guest-to-host test passed. The Dell sometimes transiently returned to DP shortly after shutdown; a separate delayed 12-second HDMI2 verification/return step was installed and separately tested.

The launcher inherited incompatible AppImage GTK library variables in one test. `notify-send` was changed to use a clean host environment; that notification failure was cosmetic.

## 7. Live focus, COM1, audio and reboot resilience

User requirement evolved: NumPad1 must return HDMI+keyboard to Ubuntu **without Windows shutdown** and NumPad2 must show the **same running guest** again. An offline QEMU COM1 one-time message plus host-side Dell DDC verification and *live-only* Logitech USB hostdev changes implemented it. Dell Display Manager (originally tried inside Windows) became optional. The host independently selects HDMI2; it never transfers USB from mere observation of an input change.

NumPad3 separately borrows/returns physical Focusrite Scarlett Solo. Live USB attach/detach, exact serial/session marker, default PipeWire sink restore and independent Linux H570e microphone were tested. The user installed the native Windows Focusrite driver to eliminate audible crackling.

After a Windows reboot, the Windows hotkey listener did not resume reliably. Investigation found an old PowerShell instance retaining obsolete DDM behavior (new instance blocked on mutex) and a registry installer that erased prior `HKCU Run` values with `New-Item -Force`. A narrowly validated video-only process replacement and non-destructive per-value .NET RegistryKey updates corrected both. Local current-registry backup was added (it cannot reconstruct already lost startup entries). The user then verified both video and audio listeners started after Windows-only reboot, and NumPad1 still returned focus with Windows running.

## 8. Final evidence and limits

Source/installed equality, syntax and 38 offline regression checks were recorded. Hardware display+USB and Scarlett audio handoffs had independent real tests. The Windows-only reboot proof covered both listeners' startup and live NumPad1 return. It did **not** repeat the full Scarlett audible playback sequence after that last reboot.

See [architecture](01-architecture.md), [incidents](08-incidents.md), [acceptance](09-acceptance-evidence.md) and [SSH retirement](10-ssh-retirement.md). Future automation is intentionally deferred.
