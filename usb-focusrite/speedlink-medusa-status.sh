#!/bin/bash

vendorid="0x0d8c"
domain="win10"

status=$(virsh domstate $domain)
if [ "$status" = "shut off" ];then
    echo -e "shut off"
    exit 2
fi

virsh dumpxml $domain > "$domain".xml
if grep -q $vendorid "$domain".xml; then
    echo -e "vendorid: $vendorid found"
    exit 1
else
    echo -e "no vendorid found"
    exit 2
fi