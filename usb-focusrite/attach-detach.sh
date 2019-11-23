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