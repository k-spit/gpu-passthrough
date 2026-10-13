# Read-only reference snapshots of selected installed configurations

The following reviewed non-secret source text corresponds to the udev, systemd and GNOME launcher configurations installed at acceptance. They are preserved as documentation, **not** an automated deployment directory; copying these verbatim to a different host may cause downtime. All other runtime scripts are indexed by file hashes only.

## `61-mutter-ignore-radeon-kms.rules`

```udev
# The AMD RX 6900 XT remains bound to amdgpu for Linux GPU offload/compute.
# Hide only its DRM *KMS card* from the GNOME Mutter compositor. The GTX1070
# remains Mutter's preferred render+display GPU on the Dell's HDMI2 input.
# Do not tag Radeon renderD* nodes, the HDMI audio function, or other AMD GPUs.
# This takes full effect at the next GNOME Wayland startup; never restart GDM
# to apply it while the user has unsaved graphical applications.
SUBSYSTEM=="drm", ENV{DEVTYPE}=="drm_minor", ENV{DEVNAME}=="/dev/dri/card[0-9]*", SUBSYSTEMS=="pci", ATTRS{vendor}=="0x1002", ATTRS{device}=="0x73bf", TAG+="mutter-device-ignore"
```

## `61-mutter-preferred-primary-gpu.rules`

```udev
# Proposed session anchor: GTX 1070 [10de:1b81], independent of PCI bus numbering.
# Do not activate until the HDMI input has been visually verified.
# Mutter's Wayland compositor should keep this GPU as its preferred render device;
# this alone does not prove the RX 6900 XT can be hot-detached without closing apps.
SUBSYSTEM=="drm", ENV{DEVTYPE}=="drm_minor", ENV{DEVNAME}=="/dev/dri/card[0-9]*", SUBSYSTEMS=="pci", ATTRS{vendor}=="0x10de", ATTRS{device}=="0x1b81", TAG+="mutter-device-preferred-primary"
```

## `dual-gpu-option-a-daily.service`

```ini
[Unit]
Description=Switch to Windows 11 safely (persistent qcow2, Radeon VFIO, NVIDIA GNOME retained)
Documentation=man:systemd.service(5)
After=local-fs.target systemd-udevd.service

[Service]
Type=oneshot
User=root
Group=root
ExecStart=/usr/local/sbin/dual-gpu-option-a-run --daily
TimeoutStartSec=infinity
TimeoutStopSec=20s
Restart=no
StandardOutput=journal
StandardError=journal
```

## `dual-gpu-option-a-recover.service`

```ini
[Unit]
Description=Option A conditional Radeon GPU/audio/ACL recovery without stopping GNOME
Documentation=man:systemd.service(5)
After=local-fs.target

[Service]
Type=oneshot
User=root
Group=root
ExecStart=/usr/local/sbin/dual-gpu-option-a-recover
TimeoutStartSec=110s
NoNewPrivileges=false
```

## `dual-gpu-option-a-recover.timer`

```ini
[Unit]
Description=Retry Option A host GPU recovery if the controlling process disappears

[Timer]
OnActiveSec=120s
OnUnitActiveSec=60s
AccuracySec=1s
Unit=dual-gpu-option-a-recover.service

[Install]
WantedBy=timers.target
```

## `dual-gpu-option-a-focus-watch.service`

```ini
[Unit]
Description=Follow Dell U4919DW video input with live Linux/Windows USB focus
Documentation=man:systemd.service(5)
After=libvirtd.service
StartLimitIntervalSec=0

[Service]
Type=simple
User=root
Group=root
ExecStart=/usr/local/sbin/dual-gpu-option-a-focus --watch
Restart=on-failure
RestartSec=3s
TimeoutStopSec=5s
StandardOutput=journal
StandardError=journal
```

## `dual-gpu-switch-to-windows.desktop`

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Switch to Windows 11
GenericName=GPU passthrough
Comment=Keep Ubuntu running on NVIDIA HDMI 2; open protected Windows 11 on Radeon DisplayPort
Exec=/home/desktop/.local/bin/switch-to-windows --start
Icon=computer
Terminal=false
StartupNotify=false
Categories=System;
Keywords=Windows;Ubuntu;Radeon;VFIO;switch;
```
