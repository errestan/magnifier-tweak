# Copyright (c) 2020 Lee Clark
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio
from gi.repository import Gtk
from gi.repository import Handy

class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       show_menubar=False)
        self.set_size_request(-1, 700)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_name("com.magnifier.tweaks")

        self.hsize_group = Gtk.SizeGroup(mode=Gtk.SizeGroupMode.HORIZONTAL)

        self.main_box = Handy.Leaflet()
        self.main_box.set_mode_transition_type(Handy.LeafletModeTransitionType.SLIDE)
        self.main_box.set_child_transition_type(Handy.LeafletChildTransitionType.SLIDE)

        titlebar = self.create_titlebar()

        self.set_titlebar(titlebar)

        sidebar = self.create_sidebar()
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        content = self.create_content()

        self.main_box.add(sidebar)
        self.main_box.add(separator)
        self.main_box.add(content)
        self.main_box.child_set(sidebar, name="sidebar")
        self.main_box.child_set(content, name="content")

        self.add(self.main_box)

    def create_titlebar(self):
        header = Handy.Leaflet()
        header.set_mode_transition_type(Handy.LeafletModeTransitionType.SLIDE)
        header.set_child_transition_type(Handy.LeafletChildTransitionType.SLIDE)

        self.builder = Gtk.Builder()

        lbl = Gtk.Label(label="Options")
        lbl.get_style_context().add_class("title")
        icon1 = Gtk.Image()
        icon1.set_from_icon_name("edit-find-symbolic", Gtk.IconSize.MENU)
        icon2 = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="open-menu-symbolic"),
                                         Gtk.IconSize.BUTTON)
        appmenu = self.builder.get_object('appmenu')

        self.button = Gtk.ToggleButton()
        self.button.add(icon1)
        self.button.props.valign = Gtk.Align.CENTER

        self.menu_btn = Gtk.MenuButton()
        self.menu_btn.set_image(icon2)
        self.menu_btn.set_menu_model(appmenu)

        left_header = Gtk.HeaderBar()
        left_header.props.show_close_button = True
        left_header.set_custom_title(lbl)
        left_header.pack_start(self.button)
        left_header.pack_end(self.menu_btn)

        self.title = Gtk.Label(label="")
        self.back_button = Gtk.Button.new_from_icon_name("go-previous-symbolic", 1)

        right_header = Gtk.HeaderBar()
        right_header.props.show_close_button = True
        right_header.props.hexpand = True
        right_header.set_custom_title(self.title)
        right_header.pack_start(self.back_button)

        header.add(left_header)
        header.add(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
        header.add(right_header)
        header.child_set(left_header, name="sidebar")
        header.child_set(right_header, name="content")

        header.bind_property("folded", self.back_button, "visible")

        self.header_group = Handy.HeaderGroup()
        self.header_group.add_header_bar(left_header)
        self.header_group.add_header_bar(right_header)

        self.hsize_group.add_widget(left_header)

        return header

    def create_sidebar(self):
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.entry = Gtk.SearchEntry(placeholder_text="Search Tweaks…")
        if (Gtk.check_version(3, 22, 20) is None):
            self.entry.set_input_hints(Gtk.InputHints.NO_EMOJI)

        self.searchbar = Gtk.SearchBar()
        self.searchbar.add(self.entry)
        self.searchbar.props.hexpand = False

        self.listbox = Gtk.ListBox()
        self.listbox.set_size_request(200, -1)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER,
                          Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.listbox)

        sidebar_box.pack_start(self.searchbar, False, False, 0)
        sidebar_box.pack_start(scroll, True, True, 0)

        self.hsize_group.add_widget(sidebar_box)

        return sidebar_box

    def create_content(self):
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        content_box.set_size_request(750, -1)

        self.stack = Gtk.Stack()

        content_box.pack_start(self.stack, True, True, 0)

        return content_box
