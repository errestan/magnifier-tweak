# Copyright (c) 2020 Lee Clark
# SPDX-License-Identifier: MITNFA

from gi.repository import Gtk

class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       show_menubar=False)
        self.set_size_request(700, 700)
        self.set_position(Gtk.WindowPosition.CENTER)

