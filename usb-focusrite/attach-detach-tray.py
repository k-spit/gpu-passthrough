#!/usr/bin/python
import gi
import os
import signal
import time

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
#from gi.repository import GObject
from threading import Thread

APPINDICATOR_ID = 'focusriteindicator'

CURRPATH = os.path.dirname(os.path.realpath(__file__))

class Indicator():
    def __init__(self):
        self.app = 'focusrite'
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, CURRPATH+"/attached.svg", appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        notify.init(APPINDICATOR_ID)

        # thread code
        self.update = Thread(target=self.update)
        # daemonize the thread to make the indicator stopable
        self.update.setDaemon(True)
        self.update.start()

    def build_menu(self):
        menu = gtk.Menu()

        item_color = gtk.MenuItem('focusrite win10')
        item_color.connect('activate', self.focusritewin10)

        item_color2 = gtk.MenuItem('focusrite ubuntu')
        item_color2.connect('activate', self.focusriteubuntu)

        item_color3 = gtk.MenuItem('speedlink medusa win10')
        item_color3.connect('activate', self.speedlinkmedusawin10)

        item_color4 = gtk.MenuItem('speedlink medusa ubuntu')
        item_color4.connect('activate', self.speedlinkmedusaubuntu)

        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)

        menu.append(item_color)
        menu.append(item_color2)
        menu.append(item_color3)
        menu.append(item_color4)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def update(self):
        t = 2
        while True:
            x = os.system(CURRPATH+"/checkStatus.sh")
            if x == 256:
                self.indicator.set_icon(CURRPATH+"/detached.svg")
                print("attached")
            else:
                self.indicator.set_icon(CURRPATH+"/attached.svg")
                print("not attached")
            time.sleep(1)
            t += 1

    def focusritewin10(self, source):
        os.system(CURRPATH+"/focusrite-win10.sh")
        self.indicator.set_icon(CURRPATH+"/detached.svg")

    def focusriteubuntu(self, source):
        os.system(CURRPATH+"/focusrite-ubuntu.sh")
        self.indicator.set_icon(CURRPATH+"/attached.svg")

    def speedlinkmedusawin10(self, source):
        os.system(CURRPATH+"/speedlink-medusa-win10.sh")

    def speedlinkmedusaubuntu(self, source):
        os.system(CURRPATH+"/speedlink-medusa-ubuntu.sh")

    def quit(self, source):
        gtk.main_quit()

Indicator()
#GObject.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)
gtk.main()