# Verified hardware and ownership architecture

## One physical screen, two operating systems

| Function | Hardware | Exact PCI/USB identity, Linux driver | Monitor |
| --- | --- | --- | --- |
| GNOME Wayland host | NVIDIA GeForce GTX 1070 | PCI `0000:0c:00.0`, `10de:1b81`, proprietary `nvidia` 580.178.04 | Dell U4919DW HDMI **2**, logical GNOME `HDMI-1` at 5120x1440 |
| VM GPU | AMD RX 6900 XT | PCI `0000:0b:00.0`, `1002:73bf`, `amdgpu` when guest off and `vfio-pci` while Windows owns it | Same Dell DisplayPort **1** |
| VM GPU HDMI audio | AMD audio function | PCI `0000:0b:00.1`, `1002:ab28`, `snd_hda_intel` or `vfio-pci` | Accompanies RX6900 |
| Video input selection | Dell U4919DW | DDC/CI VCP `0x60`: `0x12` HDMI2, `0x0f` DP1 | Host HDMI DDC over NVIDIA I2C bus |
| Guest keyboard and mouse | Two Logitech USB receivers | `046d:c534` and `046d:c53f` | USB hot-attach/detach while guest stays running |
| Explicitly selected playback | Focusrite Scarlett Solo (3rd Gen.) | USB `1235:8211`, additionally checked by exact private serial | Separate guest USB port 4, live-only |
| Ubuntu voice input | Logitech H570e | Separate USB default microphone | Stays in Linux even if Scarlett goes to guest |

GNOME 46 Wayland is permanently anchored to NVIDIA. The Radeon DRM **KMS card** is tagged `mutter-device-ignore`; NVIDIA is tagged `mutter-device-preferred-primary`. Only the Radeon KMS card is hidden from Mutter, *not* its render node. This avoids the failed Mutter secondary-GPU re-registration while retaining `amdgpu` capability when Windows stops.

## Guest and immutable source data

The accepted daily libvirt VM is `win11-physical-vfio-check` at `qemu:///system`. Another, `win11-physical`, exists and is intentionally not used. The accepted domain has RX6900+audio PCI, two Logitech receivers, ISA COM1 for authenticated offline hotkey intents, a read-only `UBUNTU_RETURN` optical helper, no virtual VGA, and a network interface with link explicitly **down**.

Windows changes are written only to `/var/lib/libvirt/images/win11-physical-safety-overlay.qcow2`. Its raw backing block device is the **physical native Windows Samsung SSD 970 EVO Plus 1TB**, mounted nowhere on Ubuntu and made read-only to QEMU. During a real Windows guest run the *live QEMU file descriptors* were independently verified: backing physical Windows SSD `O_RDONLY`, overlay `O_RDWR`. The device by-id serial and VM UUID are deliberately omitted from this public record. **Never modify the backing SSD by booting native Windows while this overlay is reused.**

## Three distinct operations

**Starting/stopping Windows:** Ubuntu desktop launcher starts an independent fixed root systemd unit. Preflight verifies exact hardware, isolated storage, active GNOME+NVIDIA display, Radeon no-client gate and a recovery channel. Only Radeon GPU/audio are handed to VFIO. The Windows session has *no fixed automatic shutdown deadline*. Normal Windows shutdown triggers root recovery to `amdgpu`/`snd_hda_intel`, saved ACLs and HDMI2.

**Live video and Logitech focus:** With Windows running, its NumPad1 listener emits a one-time exact guest/session-bound COM1 intent. The root host watcher *sets and verifies* HDMI2 using Dell DDC on NVIDIA, then returns only two USB receivers to Ubuntu. Windows keeps running, still owns Radeon. Ubuntu NumPad2 reverses the USB focus and selects DP1. Spontaneous Dell input changes cannot authorize USB transfer.

**Independent USB playback:** NumPad3 moves the entire Scarlett USB device to/from the running Windows VM; video focus is unaffected. A saved session marker identifies Scarlett hardware and previous PipeWire default sink. Returning to Ubuntu restores exact default playback. The independent H570e microphone stays with Ubuntu. Scarlett's own recording inputs necessarily travel with the device.

## Safety infrastructure

A guarded root GPU recovery timer is armed during guest ownership; it must not rebind Radeon while Windows remains running. A root focus watcher handles COM1/USB/DDC. Other scripts validate state under locks and compare original GNOME process identity. Production installation leaves NVIDIA, GNOME, Chrome and Chat On Steroids running throughout normal focus changes.

This setup originally relied on independently authenticated Fedora SSH. The user later authorized retiring that server after Windows was off and replacing its preflight condition with a strictly checked **local root recovery service/timer** (not an external equivalent). Strict no-SSH readiness passed. See [SSH retirement](10-ssh-retirement.md).
