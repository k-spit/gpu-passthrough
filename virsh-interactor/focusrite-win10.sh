#!/bin/bash

vendorid="0x1235"
domain="win10"
devicedesc=usb-focusrite.xml

virsh attach-device $domain --file $devicedesc