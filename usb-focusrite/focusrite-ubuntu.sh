#!/bin/bash

vendorid="0x1235"
domain="win10"
devicedesc=/home/desktop/git/gpu-passthrough/usb-focusrite/usb-focusrite.xml

virsh detach-device $domain --file $devicedesc
# end pulseaudio
killall pulseaudio