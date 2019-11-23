#!/bin/bash

SomeString="1235"

virsh dumpxml win10 > tmp
if grep -q $SomeString tmp; then
  echo -e "found"
  virsh detach-device win10 --file /home/desktop/gpu-passthrough/usb-focusrite/usb-focusrite.xml
  exit
else
  echo -e "not found"
  virsh attach-device win10 --file /home/desktop/gpu-passthrough/usb-focusrite/usb-focusrite.xml
  exit
fi
