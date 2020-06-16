#!/bin/bash

vendorid="0x1235"
domain="win10"
devicedesc=/home/desktop/git/gpu-passthrough/usb-focusrite/usb-focusrite.xml

virsh attach-device $domain --file $devicedesc