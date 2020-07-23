#!/bin/sh
PREREQS=""
# find in /sys/bus/pci/devices or with virt-manager in your vw > add device > pci host device 
DEVS="0000:0a:00.0 0000:0a:00.1"
for DEV in $DEVS;
  do echo "vfio-pci" > /sys/bus/pci/devices/$DEV/driver_override
done

modprobe -i vfio-pci