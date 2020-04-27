# Copyright (c) 2020 Lee Clark
# SPDX-License-Identifier: MITNFA

from gi.repository import Gio
from gi.repository import GLib
from gi.repository import Gtk

from mtt.view import Window

class MagnifierTweaks(Gtk.Application):

    def __init__(self):
        GLib.set_application_name("Magnifier Tweak Tool")
        Gtk.Application.__init__(self, application_id="com.magnifier.tweaks")
        self.win = None

    def do_activate(self):
        if not self.win:
            self.win = Window(self)
            self.win.show_all()

        self.win.present()
