# Copyright (c) 2020 Lee Clark
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

import mtt.view

# We need to specify the required version of some Gtk components.
gi.require_version("Gtk", "3.0")
gi.require_version("Handy", "0.0")

import gi.repository.GLib as GLib  # noqa: E402
import gi.repository.Gtk as Gtk  # noqa: E402


class MagnifierTweaks(Gtk.Application):
    def __init__(self):
        GLib.set_application_name("Magnifier Tweak Tool")
        Gtk.Application.__init__(self, application_id="com.magnifier.tweaks")
        self.win = None

    def do_activate(self):
        if not self.win:
            self.win = mtt.view.Window(self)
            self.win.show_all()
            self.win.back_button.props.visible = False
        self.win.present()

    def quit_cb(self, action, parameter):
        self.quit()
