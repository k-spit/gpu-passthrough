USB Focusrite
===

# Usage:
Copy `.local` folder to your `HOME`-directory.  
`Focusrite-Win10.desktop` is your application that you can pin from your dock.  

```shell
[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Icon=/home/<your-user>/gpu-passthrough/usb-focusrite/scarlett.jpg
Exec=sh /home/<your-user>/gpu-passthrough/usb-focusrite/attach-detach.sh
Name=Focusrite Win10
```
`Focusrite-Win10.desktop`

Now make it executable (Right click in file manager).  

Now to attach/detach the device, simply click the `.desktop` icon.
The script, which does the work using virsh commands is `attach-detach.sh`.

```shell
#!/bin/bash

vendorid="0x1235"
domain="win10"
devicedesc=/home/desktop/gpu-passthrough/usb-focusrite/usb-focusrite.xml

virsh dumpxml $domain > tmp
if grep -q $vendorid tmp; then
  echo -e "vendorid: $vendorid found"
  virsh detach-device $domain --file $devicedesc
  exit
else
  echo -e "no vendorid found"
  virsh attach-device $domain --file $devicedesc
  exit
fi
```