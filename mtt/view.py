# Copyright (c) 2020 Lee Clark
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
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
        self._update_decorations()

        sidebar = self.create_sidebar()
        content = self.create_content()
        content.props.hexpand = True

        self.main_box.add(sidebar)
        self.main_box.add(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
        self.main_box.add(content)
        self.main_box.child_set(sidebar, name="sidebar")
        self.main_box.child_set(content, name="content")
        self.main_box.set_visible_child_name("sidebar")
        self.main_box.bind_property("visible-child-name", titlebar,
                                    "visible-child-name", GObject.BindingFlags.SYNC_CREATE)

        start_pane_size_group = Gtk.SizeGroup(Gtk.SizeGroupMode.HORIZONTAL)
        start_pane_size_group.add_widget(sidebar)
        start_pane_size_group.add_widget(self._left_header)

        end_pane_size_group = Gtk.SizeGroup(Gtk.SizeGroupMode.HORIZONTAL)
        end_pane_size_group.add_widget(content)
        end_pane_size_group.add_widget(self._right_header)

        widget = self.listbox.get_row_at_index(0)
        self.listbox.select_row(widget)

        Gtk.Settings.get_default().connect("notify::gtk-decoration-layout",
                                           self._update_decorations)
        self.connect("key-press-event", self._on_key_press)

        self.add(self.main_box)

    def create_titlebar(self):
        self._group_titlebar_widget = None

        header = Handy.Leaflet()
        header.set_mode_transition_type(Handy.LeafletModeTransitionType.SLIDE)
        header.set_child_transition_type(Handy.LeafletChildTransitionType.SLIDE)
        header.connect("notify::visible-child", self._update_decorations)
        header.connect("notify::fold", self._update_decorations)

        lbl = Gtk.Label(label="Options")
        lbl.get_style_context().add_class("title")
        icon1 = Gtk.Image()
        icon1.set_from_icon_name("edit-find-symbolic", Gtk.IconSize.MENU)
        icon2 = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="open-menu-symbolic"),
                                         Gtk.IconSize.BUTTON)

        self.button = Gtk.ToggleButton()
        self.button.add(icon1)
        self.button.connect("toggled", self._on_find_toggled)
        self.button.props.valign = Gtk.Align.CENTER

        appmenu = Gio.Menu()
        appmenu.append("About Magnifier Tweaks", "win.about")

        self.menu_btn = Gtk.MenuButton()
        self.menu_btn.set_image(icon2)
        self.menu_btn.set_menu_model(appmenu)

        left_header = Gtk.HeaderBar()
        left_header.props.show_close_button = True
        left_header.set_custom_title(lbl)
        left_header.pack_start(self.button)
        left_header.pack_end(self.menu_btn)
        self._left_header = left_header

        self.title = Gtk.Label(label="")

        self.back_button = Gtk.Button.new_from_icon_name("go-previous-symbolic", 1)
        self.back_button.connect("clicked", self._on_back_clicked)

        right_header = Gtk.HeaderBar()
        right_header.props.show_close_button = True
        right_header.props.hexpand = True
        right_header.set_custom_title(self.title)
        right_header.pack_start(self.back_button)
        self._right_header = right_header

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

        action_about = Gio.SimpleAction.new("about", None)
        action_about.connect("activate", self._on_activate_about)
        self.add_action(action_about)

        return header

    def create_sidebar(self):
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.entry = Gtk.SearchEntry(placeholder_text="Search Tweaks…")
        if (Gtk.check_version(3, 22, 20) is None):
            self.entry.set_input_hints(Gtk.InputHints.NO_EMOJI)
        self.entry.connect("search-changed", self._on_search)

        self.searchbar = Gtk.SearchBar()
        self.searchbar.add(self.entry)
        self.searchbar.props.hexpand = False

        self.listbox = Gtk.ListBox()
        self.listbox.set_size_request(200, -1)
        self.listbox.connect("row-selected", self._on_select_row)
        self.listbox.set_header_func(self._list_header_func, None)
        self.listbox.add(self.make_list_row("Magnification"))
        self.listbox.add(self.make_list_row("Tracking"))
        self.listbox.add(self.make_list_row("Colour Enhancement"))
        self.listbox.add(self.make_list_row("Cross hairs"))

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

    def make_list_row(self, text):
        lbl = Gtk.Label(label=text, xalign=0.0)
        row = Gtk.ListBoxRow()
        row.add(lbl)

        return row

    def _update_decorations(self, *_):
        header = self.get_titlebar()
        if header.props.folded:
            self.header_group.set_focus(header.get_visible_child())
        else:
            self.header_group.set_focus(None)

    def _on_key_press(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)

        if keyname == 'Escape' and self.button.get_active():
            if self.entry.is_focus():
                self.button.set_active(False)
            else:
                self.entry.grab_focus()
            return True

        if event.state & Gdk.ModifierType.CONTROL_MASK:
            if keyname == 'f':
                self.button.set_active(True)
                return True

        if keyname == 'F10':
            self.menu_btn.activate()
            return True

        return False

    def _on_list_changed(self, group):
        self.listbox.set_filter_func(self._list_filter_func, group)
        selected = self.listbox.get_selected_row().get_child().get_text()
        if group and selected not in group:
            index = 0
            row = self.listbox.get_row_at_index(index)
            self.listbox.select_row(row)

    def _list_filter_func(self, row, user_data):
        lbl = row.get_child()
        if lbl.get_text() in user_data:
            return row

    def _list_header_func(self, row, before, user_data):
        if before and not row.get_header():
            row.set_header(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

    def _on_select_row(self, listbox, row):
        if row:
            group = row.get_child().get_text()
            self.title.set_text(group)
            self.main_box.set_visible_child_name("content")

    def _on_find_toggled(self, btn):
        if self.searchbar.get_search_mode():
            self.searchbar.set_search_mode(False)
            self.entry.set_text("")
        else:
            self.searchbar.set_search_mode(True)
            self.entry.grab_focus()

    def _on_search(self, entry):
        txt = entry.get_text()
        self._on_list_changed(txt)

    def _on_back_clicked(self, *_):
        self.main_box.set_visible_child_name("sidebar")

    def _on_activate_about(self, action, parameter):
        aboutdialog = Gtk.AboutDialog(modal=True, transient_for=self)
        aboutdialog.set_program_name(aboutdialog.get_program_name())

        aboutdialog.set_comments("")
        aboutdialog.set_copyright("Copyright © 2020 Lee Clark.")
        aboutdialog.set_license_type(Gtk.License.GPL_3_0)
        aboutdialog.set_authors(["Lee Clark <lclark125@users.github.com>"])

        aboutdialog.show()
