#!/bin/bash

domain="win10"

status=$(virsh domstate $domain)
if [ "$status" = "shut off" ];then
    #echo -e "$status"
    exit 1
fi
if [ "$status" = "running" ];then
    #echo -e "$status"
    exit 0
fi