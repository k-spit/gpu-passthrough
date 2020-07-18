#!/bin/bash

vendorid="0x0d8c"
domain="win10"
devicedesc=speedlink-medusa.xml

virsh detach-device $domain --file $devicedesc