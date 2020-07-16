#!/usr/bin/python
from threading import Thread
from gi.repository import Notify as notify
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk as gtk
import gi
import os
import signal
import time

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')


APPINDICATOR_ID = 'focusriteindicator'

CURRPATH = os.path.dirname(os.path.realpath(__file__))

item_domain_toggle = gtk.MenuItem('Toggle domain (win10)')
item_medusa_toggle = gtk.MenuItem('Toggle Medusa')
item_focusrite_toggle = gtk.MenuItem('Toggle Focusrite')

def check_domain_status():
    ds = os.system(CURRPATH+"/domain-status.sh")
    if ds == 256:
        item_domain_toggle.set_label("Toggle domain (win10) - shut off")
    else:
        item_domain_toggle.set_label("Toggle domain (win10) - running")

def check_focusrite_status(self):
    x = os.system(CURRPATH+"/focusrite-status.sh")
    if x == 256:
        self.indicator.set_icon(CURRPATH+"/windows-logo.svg")
        item_focusrite_toggle.set_label("Toggle Focusrite - attached")
        #print("attached")
    else:
        self.indicator.set_icon(CURRPATH+"/ubuntu-logo.svg")
        item_focusrite_toggle.set_label("Toggle Focusrite - detached")
        #print("not attached")

def check_medusa_status():
    sms = os.system(CURRPATH+"/speedlink-medusa-status.sh")
    if sms == 256:
        item_medusa_toggle.set_label("Toggle Medusa - attached")
    else:
        item_medusa_toggle.set_label("Toggle Medusa - detached")


class Indicator():
    def __init__(self):
        self.app = 'focusrite'
        self.indicator = appindicator.Indicator.new(
            APPINDICATOR_ID, CURRPATH+"/windows-logo.svg", appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        #print(self.indicator.get_status())
        notify.init(APPINDICATOR_ID)

        # thread code
        self.update = Thread(target=self.update)
        # daemonize the thread to make the indicator stopable
        self.update.setDaemon(True)
        self.update.start()

    def build_menu(self):
        menu = gtk.Menu()

        item_domain_toggle.connect('activate', self.startwin10)

        item_focusrite_toggle.connect('activate', self.focusritewin10)

        item_medusa_toggle.connect('activate', self.speedlinkmedusawin10)

        item_quit = gtk.MenuItem('quit')
        item_quit.connect('activate', self.quit)

        menu.append(item_domain_toggle)
        menu.append(item_focusrite_toggle)
        menu.append(item_medusa_toggle)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def update(self):
        t = 2
        while True:
            check_domain_status()
            check_focusrite_status(self)
            check_medusa_status()

            time.sleep(1)
            t += 1

    def startwin10(self, source):    
        x=os.system(CURRPATH+"/start-win10.sh")
        if x == 256:
            os.system(CURRPATH+"/forcestop-win10.sh")     
    
    def focusritewin10(self, source):
        if self.indicator.get_icon() == "/home/desktop/git/gpu-passthrough/usb-focusrite/windows-logo.svg":
            focusrite_activated = True
        else:
            focusrite_activated = False
        if focusrite_activated:
            os.system(CURRPATH+"/focusrite-ubuntu.sh")
            self.indicator.set_icon(CURRPATH+"/ubuntu-logo.svg")
            return
        if not focusrite_activated:
            os.system(CURRPATH+"/focusrite-win10.sh")
            self.indicator.set_icon(CURRPATH+"/windows-logo.svg")

    def speedlinkmedusawin10(self, source):
        x = os.system(CURRPATH+"/speedlink-medusa-win10.sh")
        if x == 256:
            os.system(CURRPATH+"/speedlink-medusa-ubuntu.sh")

    def quit(self, source):
        gtk.main_quit()

Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
gtk.main()