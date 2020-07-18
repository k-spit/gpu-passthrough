#!/bin/bash

device="/dev/input/event2"

evemu-event ${device} --type EV_KEY --code 29 --value 1 --sync
evemu-event ${device} --type EV_KEY --code 97 --value 1 --sync
evemu-event ${device} --type EV_KEY --code 97 --value 0 --sync
evemu-event ${device} --type EV_KEY --code 29 --value 0 --sync