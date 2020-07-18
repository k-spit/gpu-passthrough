#!/bin/bash

vendorid="0x1235"
domain="win10"
devicedesc=usb-focusrite.xml

virsh detach-device $domain --file $devicedesc
# end pulseaudio
killall pulseaudio