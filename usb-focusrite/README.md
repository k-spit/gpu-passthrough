USB Focusrite
===

# Usage:
Add the following command to Startup Applications (Ubuntu):  
`python /path/to/script/attach-detach-tray-service.py`

Now with a right-click on the icon choose between:  
* Attach Focusrite (attaches the interface to the vm)
* Detach Focusrite (detaches the interface from the vm)
* Quit (shutdown the application)

# How it works
## [attach-detach-tray.py](attach-detach-tray.py):
### init method:
Define `appindicator` with svg icon.  

```python
self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, CURRPATH+"/detached.svg", appindicator.IndicatorCategory.SYSTEM_SERVICES)
```
Define Thread and daemonize it to make the indicator stopable.

```python
self.update = Thread(target=self.show_seconds)
self.update.setDaemon(True)
```

Define thread-update function, check virsh domain status and if necessary change icon.  
```python
def update(self):
  t = 2
  while True:
      x = os.system(CURRPATH+"/checkStatus.sh")
      if x == 256:
          print("attached")
          self.indicator.set_icon(CURRPATH+"/attached.svg")
      else:
          print("not attached")
          self.indicator.set_icon(CURRPATH+"/detached.svg")
      time.sleep(1)
      t += 1
```

Define functions for attaching/detaching the interface.  Each of these function is used to execute a underlying shell script with the help of `os.system`.

```shell
vendorid="0x1235" # device vendorid
domain="win10" # virsh domain
devicedesc=/home/desktop/gpu-passthrough/usb-focusrite/usb-focusrite.xml

# to attach a device to a domain
virsh attach-device $domain --file $devicedesc

# to detach a device from a domain
virsh detach-device $domain --file $devicedesc
```

For updating the status (icon) `update` function is call every second by thread. To get the current status (is the device attached, or not ?), `checkStatus.sh` is called by `os.system`.

```shell
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
```

If the domain is not running `checkStatus.sh` exits with `exit 2` (x == 512 in `attach-detach-tray.py`). 
If the device is already attached, `checkStatus.sh` exits with `exit 1` (x == 256 in `attach-detach-tray.py`). 