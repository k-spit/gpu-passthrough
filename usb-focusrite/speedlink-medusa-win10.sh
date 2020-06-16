#!/bin/bash

vendorid="0x0d8c"
domain="win10"
devicedesc=/home/desktop/git/gpu-passthrough/usb-focusrite/speedlink-medusa.xml

virsh attach-device $domain --file $devicedesc