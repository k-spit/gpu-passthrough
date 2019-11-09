Set Up GPU Passthrough
===

This tutorial is based on this [github repository](https://github.com/xiyizi/kvm-config).

# kvm-config
XML config and startup settings for GPU-passthrough of a second nVidia card in 2 slot of mainboard

  - Operating System: Ubuntu 18.04.3 LTS
  - Kernel Version: 5.0.0-32-generic
  - OS Type: 64-bit
  - Processors: 6 x AMD Ryzen 2600x Six-Core Processor
  - Memory: 32 GiB of RAM

  - Host GPU: Radeon R9 280x 3GB
  - Guest GPU: Nvidia 1080TI 8GB

  - Guest operating system: Windows 10 64bit 1903

  - Virtual Machine Manager version 1.5.1
  - qemu emulator version 4.1.90 (v4.2.0-rc0-2-g1cee80fa66-dirty)

# Key points: 
  - latest WORKING BIOS version is 4207!
  - svm must be enabled in BIOS
  - iommu group manipulation must be enabled in BIOS
  - GPU must be isolated and passed through to VFIO via script during boot process, *before* nvidia driver loads
  - the GPU you want to pass through should be in the *second* PCI-e slot

# How I did it:
[install/make](https://github.com/qemu/qemu) newest stable qemu version 

Lets get system up to date and install git, build tools for QEMU source building:  
```shell
sudo apt update && sudo apt upgrade -y; time sudo apt-get install build-essential zlib1g-dev pkg-config libglib2.0-dev binutils-dev libboost-all-dev autoconf libtool libssl-dev libpixman-1-dev libpython-dev python-pip python-capstone virtualenv ssvnc -y
```

GIT dependencies  
```shell
sudo apt update && sudo apt upgrade -y; sudo apt install make libssl-dev libghc-zlib-dev libcurl4-gnutls-dev libexpat1-dev gettext unzip -y
```

Do the installation process (can take some time (1hour), get a coffee, or some )
```shell
git clone https://git.qemu.org/git/qemu.git
cd qemu
git submodule init
git submodule update --recursive
./configure
make
sudo make install 
```

install the required packages:

`````shell
sudo apt-get install libvirt0 bridge-utils virt-manager ovmf
`````

make changes to _/etc/default/grub_:

  GRUB_CMDLINE_LINUX_DEFAULT="amd_iommu=on iommu=pt kvm_amd.npt=1 rd.modules-load=vfio-pci"
  
Update grub:

```shell
sudo update-grub
```

Reboot and check everything is all good:

```shell 
virt-host-validate
```

Identify PCI device:

```shell
lspci -nnv
```
  
Find the numbers of your nvidia GPU you want to pass through. A sound device will be part of your graphics card so pass that through too:

```shell
09:00.0 VGA compatible controller [0300]: NVIDIA Corporation GP102 [GeForce GTX 1080 Ti] [10de:1b06] (rev a1) (prog-if 00 [VGA controller])
	Subsystem: NVIDIA Corporation GP102 [GeForce GTX 1080 Ti] [10de:120f]

Audio device [0403]: NVIDIA Corporation GP102 HDMI Audio Controller [10de:10ef] (rev a1)
	Subsystem: NVIDIA Corporation GP102 HDMI Audio Controller [10de:120f]
```

The numbers I want to pass through to the VFIO driver are therefore __10de:1b06__ and **10de:10ef**. Do this by editing _/etc/modprobe.d/vfio.conf_:

```shell
softdep nvidia pre: vfio vfio_pci
softdep nvidiafb pre: vfio vfio_pci
softdep nvidia_drm pre: vfio vfio_pci
softdep nouveau pre: vfio vfio_pci
options vfio-pci ids=10de:1b06,10de:10ef disable_vga=1
```
  
And by editing _/etc/initramfs-tools/modules_:

```shell
softdep nvidia pre: vfio vfio_pci
softdep nvidiafb pre: vfio vfio_pci
softdep nvidia_drm pre: vfio vfio_pci
softdep nouveau pre: vfio vfio_pci

vfio
vfio_iommu_type1
vfio_virqfd
options vfio_pci ids=10de:1b06,10de:10ef
vfio_pci ids=10de:1b06,10de:10ef
vfio_pci
nvidiafb
nvidia
```
  
And by editing _/etc/modprobe.d/kvm.conf_:

```shell
options kvm ignore_msrs=1
```
  
Update init:
```shell
  sudo update-initramfs -u
  ```
  
Reboot and your second card should be completely isolated from your main operating system. nvidia control panel shouldn't even be able to see it even exists. You can check by running 

```shell
lspci -nnv
```
  
And checking the output:

```shell
  09:00.0 VGA compatible controller [0300]: NVIDIA Corporation GP102 [GeForce GTX 1080 Ti] [10de:1b06] (rev a1) (prog-if 00 [VGA controller])
	Subsystem: NVIDIA Corporation GP102 [GeForce GTX 1080 Ti] [10de:120f]
	Flags: bus master, fast devsel, latency 0, IRQ 100
	Memory at f6000000 (32-bit, non-prefetchable) [size=16M]
	Memory at c0000000 (64-bit, prefetchable) [size=256M]
	Memory at d0000000 (64-bit, prefetchable) [size=32M]
	I/O ports at c000 [size=128]
	Expansion ROM at f7000000 [disabled] [size=512K]
	Capabilities: <access denied>
	Kernel driver in use: vfio-pci
	Kernel modules: nvidiafb, nouveau
```

The nvidia card can now be pass through to a virtual-machine.

Now on to actually creating the virtual machine.

First, create a raw image to use as the hard disk for the virtual machine:

```shell
sudo fallocate -l 600G /var/libvirt/images/win10.img
```

Now fire up Virtual Manager and create a new machine:

![alt text](pics/1.png "Post a comment on this webzone if you want a pizza roll")

![part 2](pics/2.png "fuck movies")

I used the ISO you can download from [Microsoft's website](https://www.microsoft.com/en-gb/software-download/windows10ISO)

![part 3](pics/3.png "a gangsta ride blades if you ain't gon ride fly then you might as well hate")

I didn't want my virtual machine to gobble up *all* my RAM so I only gave it 12gb.

![part 4](pics/4.png "no way")

Using the image I created earlier.

![part 5](pics/5.png "my shit is custom")

Customise installation before continuing is a must so make sure it's checked.

![part 6](pics/6.png "Q is the best character in Star Trek")

I used Q35 as my machine type and selected UEFI code for my firmware.

![part 7](pics/7.png "hardware")

Click `add hardware` and select your nvidia card in the PCI selection. Click add hardware and also add your nvidia card's sound controller.

Begin the installation! I was brought t the UEFI bootloader screen so type `exit` to reach the boot selection screen and choose the ISO cd rom device. The monitor you have attached to your pass-through GPU may or may not work at this point. I had to take some extra steps after installation to get it to work.

Specifically, I had to run

```shell
sudo virsh edit win10
```

If you want to save your current virt-manager configuration, run:  
```shell
sudo virsh dumpxml win10 > win10-dump.xml
```

First of all find the very first line, which should read:  
```xml
<domain type='kvm'>
```

and replace it with:

```xml
<domain type='kvm' xmlns:qemu='http://libvirt.org/schemas/domain/qemu/1.0'>
```

Add the following xml in between the features brackets:

```xml
  <features>
    <acpi/>
    <apic/>
    <hyperv>
      <relaxed state="on"/>
      <vapic state="on"/>
      <spinlocks state="on" retries="8191"/>
      <vendor_id state="on" value="1234567890ab"/>
    </hyperv>
    <kvm>
      <hidden state="on"/>
    </kvm>
    <vmport state="off"/>
    <ioapic driver="kvm"/>
  </features>
```
That allowed my monitor to work on the next boot of the virtual machine. 

Now find the line which ends with `</vcpu>` and add the following block in the next line:

```xml
<vcpu placement='static'>8</vcpu>
<iothreads>1</iothreads>
<cputune>
  <vcpupin vcpu='0' cpuset='2'/>
  <vcpupin vcpu='1' cpuset='8'/>
  <vcpupin vcpu='2' cpuset='3'/>
  <vcpupin vcpu='3' cpuset='9'/>
  <vcpupin vcpu='4' cpuset='4'/>
  <vcpupin vcpu='5' cpuset='10'/>
  <vcpupin vcpu='6' cpuset='5'/>
  <vcpupin vcpu='7' cpuset='11'/>
  <emulatorpin cpuset='0,6'/>
  <iothreadpin iothread='1' cpuset='0,6'/>
</cputune>
```

Attention:Make sure `<vcpu>`, `<iothreads>` and `<cputune>` have the same indent.

Find the block `<features>`
and add the following block in parallel to the `<acpi>` block:

```xml
<hyperv> 
   <relaxed state='on'/>
   <vapic state='on'/>
   <spinlocks state='on' retries='8191'/>
</hyperv>
```

Attention:Make sure `<hyperv> `and `<acpi>` have the same indent.


Find the block `<CPU>` and adapt it to look like this:

```xml
<cpu mode='host-passthrough' check='none'>
  <topology sockets='1' cores='4' threads='2'/>
  <cache level='3' mode='emulate'/>
</cpu>
```

The whole xml file  
```xml
<domain type='kvm' id='1'>
  <name>win10</name>
  <uuid>915bbb74-196a-442d-b432-a137ae31b6f4</uuid>
  <memory unit='KiB'>16777216</memory>
  <currentMemory unit='KiB'>16777216</currentMemory>
  <memoryBacking>
    <hugepages/>
  </memoryBacking>
  <vcpu placement='static'>8</vcpu>
  <iothreads>1</iothreads>
  <cputune>
    <vcpupin vcpu='0' cpuset='2'/>
    <vcpupin vcpu='1' cpuset='8'/>
    <vcpupin vcpu='2' cpuset='3'/>
    <vcpupin vcpu='3' cpuset='9'/>
    <vcpupin vcpu='4' cpuset='4'/>
    <vcpupin vcpu='5' cpuset='10'/>
    <vcpupin vcpu='6' cpuset='5'/>
    <vcpupin vcpu='7' cpuset='11'/>
    <emulatorpin cpuset='0,6'/>
    <iothreadpin iothread='1' cpuset='0,6'/>
  </cputune>
  <resource>
    <partition>/machine</partition>
  </resource>
  <os>
    <type arch='x86_64' machine='pc-q35-2.11'>hvm</type>
    <loader readonly='yes' type='pflash'>/usr/share/OVMF/OVMF_CODE.fd</loader>
    <nvram>/var/lib/libvirt/qemu/nvram/win10_VARS.fd</nvram>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <hyperv>
      <relaxed state='on'/>
      <vapic state='on'/>
      <spinlocks state='on' retries='8191'/>
      <vendor_id state='on' value='1234567890ab'/>
    </hyperv>
    <kvm>
      <hidden state='on'/>
    </kvm>
    <vmport state='off'/>
    <ioapic driver='kvm'/>
  </features>
  <cpu mode='host-passthrough' check='none'>
    <topology sockets='1' cores='4' threads='2'/>
    <cache level='3' mode='emulate'/>
  </cpu>
  <clock offset='localtime'>
    <timer name='rtc' tickpolicy='catchup'/>
    <timer name='pit' tickpolicy='delay'/>
    <timer name='hpet' present='no'/>
    <timer name='hypervclock' present='yes'/>
  </clock>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <pm>
    <suspend-to-mem enabled='no'/>
    <suspend-to-disk enabled='no'/>
  </pm>
  <devices>
    <emulator>/usr/bin/kvm-spice</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='raw'/>
      <source file='/var/libvirt/images/win10.img'/>
      <backingStore/>
      <target dev='sda' bus='sata'/>
      <alias name='sata0-0-0'/>
      <address type='drive' controller='0' bus='0' target='0' unit='0'/>
    </disk>
    <disk type='file' device='cdrom'>
      <driver name='qemu' type='raw'/>
      <source file='/home/desktop/Downloads/Win10_1903_V2_German_x64.iso'/>
      <backingStore/>
      <target dev='sdb' bus='sata'/>
      <readonly/>
      <alias name='sata0-0-1'/>
      <address type='drive' controller='0' bus='0' target='0' unit='1'/>
    </disk>
    <disk type='block' device='disk'>
      <driver name='qemu' type='raw' cache='none' io='native'/>
      <source dev='/dev/disk/by-id/ata-OCZ-TRION100_95UB60EOKMGX'/>
      <backingStore/>
      <target dev='sdc' bus='sata'/>
      <alias name='sata0-0-2'/>
      <address type='drive' controller='0' bus='0' target='0' unit='2'/>
    </disk>
    <controller type='usb' index='0' model='ich9-ehci1'>
      <alias name='usb'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x1d' function='0x7'/>
    </controller>
    <controller type='usb' index='0' model='ich9-uhci1'>
      <alias name='usb'/>
      <master startport='0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x1d' function='0x0' multifunction='on'/>
    </controller>
    <controller type='usb' index='0' model='ich9-uhci2'>
      <alias name='usb'/>
      <master startport='2'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x1d' function='0x1'/>
    </controller>
    <controller type='usb' index='0' model='ich9-uhci3'>
      <alias name='usb'/>
      <master startport='4'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x1d' function='0x2'/>
    </controller>
    <controller type='sata' index='0'>
      <alias name='ide'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x1f' function='0x2'/>
    </controller>
    <controller type='pci' index='0' model='pcie-root'>
      <alias name='pcie.0'/>
    </controller>
    <controller type='pci' index='1' model='dmi-to-pci-bridge'>
      <model name='i82801b11-bridge'/>
      <alias name='pci.1'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x1e' function='0x0'/>
    </controller>
    <controller type='pci' index='2' model='pci-bridge'>
      <model name='pci-bridge'/>
      <target chassisNr='2'/>
      <alias name='pci.2'/>
      <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
    </controller>
    <controller type='pci' index='3' model='pcie-root-port'>
      <model name='pcie-root-port'/>
      <target chassis='3' port='0x10'/>
      <alias name='pci.3'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0' multifunction='on'/>
    </controller>
    <controller type='pci' index='4' model='pcie-root-port'>
      <model name='pcie-root-port'/>
      <target chassis='4' port='0x11'/>
      <alias name='pci.4'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x1'/>
    </controller>
    <controller type='pci' index='5' model='pcie-root-port'>
      <model name='pcie-root-port'/>
      <target chassis='5' port='0x12'/>
      <alias name='pci.5'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x2'/>
    </controller>
    <controller type='pci' index='6' model='pcie-root-port'>
      <model name='pcie-root-port'/>
      <target chassis='6' port='0x13'/>
      <alias name='pci.6'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x3'/>
    </controller>
    <controller type='pci' index='7' model='pcie-root-port'>
      <model name='pcie-root-port'/>
      <target chassis='7' port='0x14'/>
      <alias name='pci.7'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x4'/>
    </controller>
    <controller type='virtio-serial' index='0'>
      <alias name='virtio-serial0'/>
      <address type='pci' domain='0x0000' bus='0x03' slot='0x00' function='0x0'/>
    </controller>
    <interface type='network'>
      <mac address='52:54:00:1b:7c:42'/>
      <source network='default' bridge='virbr0'/>
      <target dev='vnet0'/>
      <model type='rtl8139'/>
      <alias name='net0'/>
      <address type='pci' domain='0x0000' bus='0x02' slot='0x01' function='0x0'/>
    </interface>
    <channel type='spicevmc'>
      <target type='virtio' name='com.redhat.spice.0' state='disconnected'/>
      <alias name='channel0'/>
      <address type='virtio-serial' controller='0' bus='0' port='1'/>
    </channel>
    <input type='mouse' bus='ps2'>
      <alias name='input0'/>
    </input>
    <input type='keyboard' bus='ps2'>
      <alias name='input1'/>
    </input>
    <graphics type='spice' port='5900' autoport='yes' listen='127.0.0.1'>
      <listen type='address' address='127.0.0.1'/>
      <gl enable='no' rendernode='/dev/dri/by-path/pci-0000:08:00.0-render'/>
    </graphics>
    <sound model='ich6'>
      <alias name='sound0'/>
      <address type='pci' domain='0x0000' bus='0x02' slot='0x02' function='0x0'/>
    </sound>
    <video>
      <model type='cirrus' vram='16384' heads='1' primary='yes'/>
      <alias name='video0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x0'/>
    </video>
    <hostdev mode='subsystem' type='pci' managed='yes'>
      <driver name='vfio'/>
      <source>
        <address domain='0x0000' bus='0x09' slot='0x00' function='0x0'/>
      </source>
      <alias name='hostdev0'/>
      <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
    </hostdev>
    <hostdev mode='subsystem' type='pci' managed='yes'>
      <driver name='vfio'/>
      <source>
        <address domain='0x0000' bus='0x09' slot='0x00' function='0x1'/>
      </source>
      <alias name='hostdev1'/>
      <address type='pci' domain='0x0000' bus='0x05' slot='0x00' function='0x0'/>
    </hostdev>
    <hostdev mode='subsystem' type='usb' managed='yes'>
      <source>
        <vendor id='0x0bc2'/>
        <product id='0x3300'/>
        <address bus='3' device='6'/>
      </source>
      <alias name='hostdev2'/>
      <address type='usb' bus='0' port='1'/>
    </hostdev>
    <hostdev mode='subsystem' type='usb' managed='yes'>
      <source>
        <vendor id='0x046d'/>
        <product id='0xc52e'/>
        <address bus='3' device='5'/>
      </source>
      <alias name='hostdev3'/>
      <address type='usb' bus='0' port='4'/>
    </hostdev>
    <hostdev mode='subsystem' type='usb' managed='yes'>
      <source>
        <vendor id='0x1235'/>
        <product id='0x8211'/>
        <address bus='3' device='3'/>
      </source>
      <alias name='hostdev4'/>
      <address type='usb' bus='0' port='5'/>
    </hostdev>
    <redirdev bus='usb' type='spicevmc'>
      <alias name='redir0'/>
      <address type='usb' bus='0' port='2'/>
    </redirdev>
    <redirdev bus='usb' type='spicevmc'>
      <alias name='redir1'/>
      <address type='usb' bus='0' port='3'/>
    </redirdev>
    <memballoon model='virtio'>
      <alias name='balloon0'/>
      <address type='pci' domain='0x0000' bus='0x06' slot='0x00' function='0x0'/>
    </memballoon>
  </devices>
  <seclabel type='dynamic' model='apparmor' relabel='yes'>
    <label>libvirt-915bbb74-196a-442d-b432-a137ae31b6f4</label>
    <imagelabel>libvirt-915bbb74-196a-442d-b432-a137ae31b6f4</imagelabel>
  </seclabel>
  <seclabel type='dynamic' model='dac' relabel='yes'>
    <label>+64055:+127</label>
    <imagelabel>+64055:+127</imagelabel>
  </seclabel>
</domain>
```

# Configuring Hugepages to use in a virtual machine

This is related to this [article](https://mathiashueber.com/configuring-hugepages-use-virtual-machine/)

Hugepages are an optional step during the VM configuration; it increases the RAM performance of the virtual machine. The downside is that the RAM allocated to the hugepages can not be used in the horst system, even if the guest isn’t running.

The minimum size should be not smaller then 4GB.

Check if hugepages are installed

```shell
hugeadm --explain
```

If you get the error message:  
```shell
hugeadm:ERROR: No hugetlbfs mount points found
```

install the missing package first before continuing:  
`sudo apt install hugepages`

Edit

sudo nano `/etc/default/qemu-kvm`

and add or uncomment  
```shell
`KVM_HUGEPAGES=1`
```

-> Reboot!

After the reboot, in a terminal window, enter again:
```shell
hugeadm --explain
```

Total System Memory: 32098 MB

Mount Point Options  
`/dev/hugepages rw,relatime,pagesize=2M`  
`/run/hugepages/kvm rw,relatime,gid=130,mode=775,pagesize=2M`

```text
Huge page pools: 
 Size Minimum Current Maximum Default 
 2097152 0 0 0 * 
 1073741824 0 0 0 …
```

As you can see, hugepages are now mounted to `/run/hugepages/kvm`, and the hugepage size is 2097152 Bytes/(1024*1024)=2MB.

Another way to determine the hugepage size is:
grep "Hugepagesize:" `/proc/meminfo`

Hugepagesize: 2048 kB

Some math:
We want to reserve 8GB for Windows:
8GB = 8x1024MB = 8192MB

Our hugepage size is 2MB, so we need to reserve:
8192MB/2MB = 4096 hugepages

We need to add some % extra space for overhead (some say 2%, some say 10%), to be on the safe side you can use 4500.

# Configure the hugepage pool

Again, run:

`sudo nano /etc/sysctl.conf`

and add the following lines into the file (a 16GB example):
```shell
# Set hugetables / hugepages for KVM single guest using 16GB RAM
vm.nr_hugepages = 8600
```

-> Reboot!

# Set shmmax value

test again:
```shell
hugeadm --explain
```

Total System Memory: 32098 MB

Mount Point Options  
`/dev/hugepages rw,relatime,pagesize=2M`  
`/run/hugepages/kvm rw,relatime,gid=130,mode=775,pagesize=2M`  

```text
Huge page pools: 
 Size Minimum Current Maximum Default 
 2097152 8600 8600 8600 * 
 1073741824 0 0 0 
Huge page sizes with configured pools:  
 …
``` 

find the part that reads:
The recommended shmmax for your currently allocated huge pages is 18035507200 bytes.
To make shmmax settings persistent, add the following line to `/etc/sysctl.conf`:
kernel.shmmax = 18035507200

->  Do it!

`sudo nano /etc/sysctl.conf`
add the recommended line
```shell
kernel.shmmax = 18035507200
```
-> yours may differ!

in order to use hugepages, add

```xml
<memoryBacking>
  <hugepages/>
</memoryBacking>
```

in your virsh edit.

# How to add a physical device or physical partition as virtual hard disk under virt-manager

```shell
$ ls -l /dev/disk/by-id/
insgesamt 0
lrwxrwxrwx 1 root root 9 23. Jul 21:05 ata-Crucial_CT256MX100SSD1_14360D295569 -> ../../sda
lrwxrwxrwx 1 root root 10 23. Jul 21:05 ata-Crucial_CT256MX100SSD1_14360D295569-part1 -> ../../sda1
lrwxrwxrwx 1 root root 10 23. Jul 21:05 ata-Crucial_CT256MX100SSD1_14360D295569-part2 -> ../../sda2
```

Add the device or partition to your existing virtual machine. In virt-manager, open the virtual machine window.

![alt text](pics/20.png "Add the device or partition to your existing virtual machine")

Click on the light bulb to bring up the virtual hardware details. Then select Add Hardware at the bottom.

![alt text](pics/21.png "Add the device or partition to your existing virtual machine")

We want to add a storage, and as device type choose Disk Device. Choose the radio button labelled “Select or create custom storage”. In the corresponding text input field, paste the name of the physical device or partition that you chose before. Set the Bus type to your liking, usually SATA or IDE are a good choice.  Click finish and the physical device is added.

Make sure the boot device is what you want it to be.

# Helpful links
https://github.com/xiyizi/kvm-config 

https://ckirbach.wordpress.com/2017/07/25/how-to-add-a-physical-device-or-physical-partition-as-virtual-hard-disk-under-virt-manager/

https://mathiashueber.com/cpu-pinning-on-amd-ryzen/#Virtual-machine-CPU-configuration

https://heiko-sieger.info/running-windows-10-on-linux-using-kvm-with-vga-passthrough/#Two_graphics_processors

https://wiki.archlinux.org/index.php/PCI_passthrough_via_OVMF#CPU_pinning

https://mathiashueber.com/configuring-hugepages-use-virtual-machine/