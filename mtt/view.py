# Copyright (c) 2020 Lee Clark
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk
from gi.repository import Handy

class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       show_menubar=False)
        self.set_size_request(700, 700)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.main_box = Handy.Leaflet()
        self.main_box.set_mode_transition_type(Handy.LeafletModeTransitionType.SLIDE)
        self.main_box.set_child_transition_type(Handy.LeafletChildTransitionType.SLIDE)

        titlebar = self.create_titlebar()

        self.set_titlebar(titlebar)

    def create_titlebar(self):
        header = Handy.Leaflet()
        header.set_mode_transition_type(Handy.LeafletModeTransitionType.SLIDE)
        header.set_child_transition_type(Handy.LeafletChildTransitionType.SLIDE)

        right_side = Gtk.HeaderBar()
        right_side.props.show_close_button = True
        right_side.props.hexpand = True

        self.title = Gtk.Label(label="")
        right_side.set_custom_title(self.title)

        header.add(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
        header.add(right_side)
        header.child_set(right_side, name="content")

        return header
