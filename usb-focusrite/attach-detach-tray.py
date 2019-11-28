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
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, CURRPATH+"/detached.svg", appindicator.IndicatorCategory.SYSTEM_SERVICES)
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

        item_color = gtk.MenuItem('Attach Focusrite')
        item_color.connect('activate', self.attach)

        item_color2 = gtk.MenuItem('Detach Focusrite')
        item_color2.connect('activate', self.detach)

        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)

        menu.append(item_color)
        menu.append(item_color2)
        menu.append(item_quit)
        menu.show_all()
        return menu

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
            #mention = str(t)+" Monkeys"
            # apply the interface update using  GObject.idle_add()
            #GObject.idle_add(
            #    self.indicator.set_label,
            #    mention, self.app,
            #    priority=GObject.PRIORITY_DEFAULT
            #    )
            t += 1

    def attach(self, source):
        self.indicator.set_icon(CURRPATH+"/attached.svg")
        os.system(CURRPATH+"/attach.sh")

    def detach(self, source):
        self.indicator.set_icon(CURRPATH+"/detached.svg")
        os.system(CURRPATH+"/detach.sh")

    def quit(self, source):
        gtk.main_quit()

Indicator()
#GObject.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)
gtk.main()