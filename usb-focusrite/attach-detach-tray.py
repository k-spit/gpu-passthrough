#!/usr/bin/python
import gi
import os
import signal
import time
import subprocess

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

        item_color5 = gtk.MenuItem('Start win10 domain')
        item_color5.connect('activate', self.startwin10)

        item_color6 = gtk.MenuItem('Stop win10 (force)')
        item_color6.connect('activate', self.forcestopwin10)

        item_color = gtk.MenuItem('Focusrite win10')
        item_color.connect('activate', self.focusritewin10)

        item_color2 = gtk.MenuItem('Focusrite ubuntu')
        item_color2.connect('activate', self.focusriteubuntu)

        item_color3 = gtk.MenuItem('Speedlink medusa win10')
        item_color3.connect('activate', self.speedlinkmedusawin10)

        item_color4 = gtk.MenuItem('Speedlink medusa ubuntu')
        item_color4.connect('activate', self.speedlinkmedusaubuntu)

        item_quit = gtk.MenuItem('quit')
        item_quit.connect('activate', self.quit)

        menu.append(item_color5)
        menu.append(item_color6)
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

    def startwin10(self, source):
        os.system(CURRPATH+"/start-win10.sh")
        password=open(CURRPATH+"/password.txt").readline().rstrip()
        print(os.getcwd())
        print(password)
        subprocess.call('echo {} | sudo -S ' + CURRPATH+'/evemu-focus.sh --args'.format(password), shell=True)
        #subprocess.call('echo {} | sudo -S /home/desktop/git/gpu-passthrough/usb-focusrite/evemu-focus.sh --args'.format(password), shell=True)

    def forcestopwin10(self, source):
        os.system(CURRPATH+"/forcestop-win10.sh")

    def quit(self, source):
        gtk.main_quit()

Indicator()
#GObject.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)
gtk.main()