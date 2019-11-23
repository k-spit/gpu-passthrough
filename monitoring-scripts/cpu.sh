#!/bin/bash

while :
do
  clear
  cat /proc/cpuinfo | grep "physical id\|core id\|processor\|cpu MHz"
  sleep 1
done
