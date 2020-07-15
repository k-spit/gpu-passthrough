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

item_domain_status = gtk.MenuItem('Status win10 domain')
item_medusa_status = gtk.MenuItem('Status Speedlink Medusa')


def check_domain_status():
    ds = os.system(CURRPATH+"/domain-status.sh")
    if ds == 256:
        item_domain_status.set_label("win10 domain - shut off")
    else:
        item_domain_status.set_label("win10 domain - running")


def check_medusa_status():
    sms = os.system(CURRPATH+"/speedlink-medusa-status.sh")
    if sms == 256:
        item_medusa_status.set_label("Speedlink Medusa - attached")
    else:
        item_medusa_status.set_label("Speedlink Medusa - not attached")


class Indicator():
    def __init__(self):
        self.app = 'focusrite'
        self.indicator = appindicator.Indicator.new(
            APPINDICATOR_ID, CURRPATH+"/windows-logo.svg", appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        print(self.indicator.get_status())
        notify.init(APPINDICATOR_ID)

        # thread code
        self.update = Thread(target=self.update)
        # daemonize the thread to make the indicator stopable
        self.update.setDaemon(True)
        self.update.start()

    def build_menu(self):
        menu = gtk.Menu()

        item_domain_status.connect('activate', self.statuswin10)

        item_medusa_status.connect('activate', self.statusspeedlinkmedusa)

        item_start_win10_domain = gtk.MenuItem('Start win10 domain')
        item_start_win10_domain.connect('activate', self.startwin10)

        item_stop_win10_domain = gtk.MenuItem('Stop win10 (force)')
        item_stop_win10_domain.connect('activate', self.forcestopwin10)

        item_focusrite_attach = gtk.MenuItem('Focusrite win10')
        item_focusrite_attach.connect('activate', self.focusritewin10)

        item_focusrite_detach = gtk.MenuItem('Focusrite ubuntu')
        item_focusrite_detach.connect('activate', self.focusriteubuntu)

        item_medusa_attach = gtk.MenuItem('Speedlink medusa win10')
        item_medusa_attach.connect('activate', self.speedlinkmedusawin10)

        item_medusa_detach = gtk.MenuItem('Speedlink medusa ubuntu')
        item_medusa_detach.connect('activate', self.speedlinkmedusaubuntu)

        item_quit = gtk.MenuItem('quit')
        item_quit.connect('activate', self.quit)

        menu.append(item_domain_status)
        menu.append(item_start_win10_domain)
        menu.append(item_stop_win10_domain)
        menu.append(item_focusrite_attach)
        menu.append(item_focusrite_detach)
        menu.append(item_medusa_status)
        menu.append(item_medusa_attach)
        menu.append(item_medusa_detach)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def update(self):
        t = 2
        while True:
            x = os.system(CURRPATH+"/focusrite-status.sh")
            if x == 256:
                self.indicator.set_icon(CURRPATH+"/windows-logo.svg")
                print("attached")
            else:
                self.indicator.set_icon(CURRPATH+"/ubuntu-logo.svg")
                print("not attached")

            check_domain_status()

            check_medusa_status()

            time.sleep(1)
            t += 1

    def statusspeedlinkmedusa(self, source):
        item_medusa_status.set_label("Status Speedlink Medusa")

    def statuswin10(self, source):
        item_domain_status.set_label("Status win10")

    def focusritewin10(self, source):
        os.system(CURRPATH+"/focusrite-win10.sh")
        self.indicator.set_icon(CURRPATH+"/windows-logo.svg")

    def focusriteubuntu(self, source):
        os.system(CURRPATH+"/focusrite-ubuntu.sh")
        self.indicator.set_icon(CURRPATH+"/ubuntu-logo.svg")

    def speedlinkmedusawin10(self, source):
        os.system(CURRPATH+"/speedlink-medusa-win10.sh")

    def speedlinkmedusaubuntu(self, source):
        os.system(CURRPATH+"/speedlink-medusa-ubuntu.sh")

    def startwin10(self, source):
        os.system(CURRPATH+"/start-win10.sh")

    def forcestopwin10(self, source):
        os.system(CURRPATH+"/forcestop-win10.sh")

    def quit(self, source):
        gtk.main_quit()


Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
gtk.main()