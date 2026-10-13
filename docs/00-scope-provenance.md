# Scope, provenance and public-repository policy

This is an *after-the-fact* record of work performed on the specific owner's Ubuntu 24.04 desktop on 2026-10-12/13. It is intentionally **documentation only**, not an unattended deployment plan, installer or working sample configuration for other hardware. The original runtime scripts already exist locally and are recorded here as implementation evidence.

## Primary evidence

1. User observation: Windows 11 desktop and Logitech input usable, live NumPad1/2 focus, correct Scarlett driver fixing Windows crackling, NumPad1 returning to Ubuntu after a Windows-only reboot.
2. Root host evidence: PCI binding changes, exact libvirt domain identity, physical Windows SSD opened `O_RDONLY` by QEMU, COW overlay opened `O_RDWR`, DDC VCP reads, Logitech USB owner, Scarlett PipeWire default sink, GNOME/Chromium/COS PID continuity, and independent root recovery status.
3. Local source code, installed udev rules/systemd units, unredacted acceptance logs and test outputs located under the owner's `~/chat-on-steroids/single-gpu-vfio/dual-gpu/` directory.
4. Earlier GitHub 2020 repository and branch for historical context only; entirely different Ubuntu/Windows release and GPU topology.

## Status vocabulary

**PASS** means the specific claim was verified by hardware or logs. **Separately tested** is narrower than a complete Windows round trip. **Installed** means source on disk, not necessarily revalidated after every edit. **Historical incident** means an actual failure, not a recommended path. **Not authorized** means deliberately untouched.

No claim is made of portability to other PCI groups/host drivers/monitors, automated reproduction, direct-write Windows storage migration, Windows networking, a Mutter code patch, or universal Focusrite driver performance.

## Publication boundary

This repository is **public**. Do not publish QEMU/Windows disk images, BitLocker material, physical NVMe EUI serial, Focusrite/monitor serial, exact guest UUID, SSH private/host keys, authentication tokens, host LAN IPs or unreviewed raw system logs. Local evidence is intentionally not copied into public Git. Its file inventory and optional checksums support traceability.

The original GitHub `master` commit and complete history are preserved on `archive/legacy-gpu-passthrough-2020`. The existing `focus_feature` branch remains untouched. The new documentation branch is based on old `master` by an ordinary new commit, not by force-push.

## Local private evidence copy

A separate **local-only**, owner-readable (`0600`) compressed archive of the original dual-GPU source and logs was saved outside the Git repository on the workstation. It is not uploaded or linked as a public download. The archived raw files and on-disk source are to be handled as private evidence.
