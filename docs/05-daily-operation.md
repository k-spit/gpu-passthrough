# Documented daily operation (existing installation)

**This is a record of the already-installed shortcuts, not an installation procedure.** The machine-specific binaries, protected guest and storage must already exist. NumLock must be **on** and keys refer to the physical **numeric keypad**, not the top row.

**Current acceptance (2026-10-13 afternoon):** An actual guarded NumPad2 startup and bidirectional NumPad1/NumPad2 focus sequence worked after a reboot-related repair; the guest then shut down normally and root restoration completed successfully. If a launcher only reports that startup was **requested**, this is not proof Windows is running; the independent systemd controller reports failures separately. Starting this VM directly in a virtualization GUI bypasses the supervised root transaction and will **not** authorize safe live USB/input hotkeys. See [incident analysis](08-incidents.md) and [new acceptance](09-acceptance-evidence.md).

| Key | Intended result |
| --- | --- |
| `Ctrl+Alt+NumPad1` | Ubuntu HDMI2 + Logitech keyboard/mouse. Windows keeps running. |
| `Ctrl+Alt+NumPad2` | Windows DisplayPort + Logitech keyboard/mouse. If Windows is stopped, initiate guarded daily boot. |
| `Ctrl+Alt+NumPad3` | *Audio only*: Scarlett Solo USB from Ubuntu to running Windows; next press returns Scarlett to Ubuntu and restores default PipeWire sink. Does not boot Windows. |

### Beginning a Windows session

The Ubuntu application menu or trusted Schreibtisch icon **Switch to Windows 11** runs `~/.local/bin/switch-to-windows --start`, which starts the fixed root `dual-gpu-option-a-daily.service` asynchronously. The root controller verifies exact VM configuration, recovery availability, GNOME/NVIDIA ownership, Radeon zero-client gate and read-only source/overlay chain before VFIO transfer. The Dell selects DP through VCP `0x60`. If a guard fails, no forced PCI detach or new Windows guest should occur.

**Daily Windows sessions have no time limit.** The root service `TimeoutStartSec=infinity` waits for *the user's normal Windows shutdown* instead of issuing timed ACPI shutdown. Do not mistake the earlier bounded test mode for normal daily behavior.

### Working between desktops

When both systems run, NumPad1 (inside Windows) sends a COM1 intent and the Ubuntu host selects Dell HDMI2, waits for verified input and returns both Logitech receivers. Same guest remains alive on RX6900. NumPad2 (on Ubuntu) focuses back to the existing running guest, transferring both receivers and selecting DP. Merely moving the Dell input manually does **not** reassign mouse/keyboard. Automatic focus **does not** reassign Scarlett audio.

### Audio choice

Ubuntu is initial owner of Scarlett and its music/Discord may continue while Windows is displayed. Press NumPad3 to transfer Scarlett USB to Windows only when Windows sound is desired; press again to return. The whole Scarlett device moves, including its built-in recording inputs. Ubuntu H570e headset microphone remains on Ubuntu. The correct Windows Focusrite Scarlett 3rd Gen. driver was necessary to stop crackling; installing that driver required a guest reboot in the tested session.

### Normal shutdown

In Windows choose **Start > Power > Shut down**. After Windows shuts off normally, the root controller restores Radeon GPU/audio drivers and saved ACLs, returns Scarlett if Windows borrowed it, selects HDMI2 and rechecks input after the delayed settling period; the watchdog is retired after verified recovery. The same Ubuntu GNOME instance is preserved. Do not forcibly `virsh destroy` or restart GDM for everyday switching.

### Safe read-only checks from existing Ubuntu installation

```sh
~/.local/bin/switch-to-windows --status
virsh -c qemu:///system list --all
sudo /usr/local/sbin/dual-gpu-option-a-focus --status
sudo /usr/local/sbin/dual-gpu-option-a-audio --status
sudo /usr/local/sbin/dual-gpu-option-a-ddc probe
systemctl show dual-gpu-option-a-recover.timer -p ActiveState -p SubState
```

Read-only `~/.local/bin/switch-to-windows --check` is a stricter **idle preflight**, not a valid check while the VM is already running. The former Fedora SSH requirement was explicitly replaced with a **fail-closed local root recovery watchdog check** after the user approved removing the inbound SSH server. Its actual systemd service/timer, installed source identity and armed/idle state are verified by both initial and last-moment Radeon-readiness gates. At SSH retirement no additional Windows session was started; **later on 2026-10-13 the guarded SSH-free VM round trip did pass**, including normal shutdown and recovery. If another action already holds the controller's lock, a simultaneous `--check` can fail without indicating bad hardware; use the exact service/VM state rather than forcing a duplicate check.

### Windows-side checks

The read-only `UBUNTU_RETURN` CD contains `Check-Live-Hotkeys.cmd` for process/HKCU Run/Startup-folder verification. The installed Windows helper stores logs under `%LOCALAPPDATA%\DualGpuLiveFocus\`. The user-tested `Return to Ubuntu - keep Windows running` desktop shortcut is the manual **no-shutdown** COM1 fallback if an in-guest hotkey registration fails. It does not replace root-side validation or make a failed host DDC path safe.

### No longer-active older procedures

Do not use the old `single-gpu-vfio-probe.service`, scripts intended to force GDM relogin, the discarded mirrored Radeon DP layout, or any helper that resets the persistent overlay. They were historical experiments. Do not boot bare-metal Windows against the live backing SSD. See [safety](07-safety-recovery.md).
