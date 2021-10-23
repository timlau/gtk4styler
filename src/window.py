# window.py
#
# Copyright 2021 Tim Lauridsen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os.path
from gi.repository import Gtk, GLib, Gio

RESOURCE_PATH = '/dk/rasmil/Gtk4Styler/'

@Gtk.Template(resource_path=RESOURCE_PATH + 'ui/window.ui')
class Gtk4stylerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'Gtk4stylerWindow'

    main = Gtk.Template.Child()
    overlay = Gtk.Template.Child()
    headerbox = Gtk.Template.Child()
    hdr_menu = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.css_provider = self.load_css()
        self.set_title("Gtk4 - Colormania")
        btn = Gtk.Button()
        btn.props.label = "Toggle Overlay"
        btn.props.valign = Gtk.Align.START
        btn.props.halign = Gtk.Align.CENTER
        btn.props.vexpand = True
        btn.props.hexpand = True
        btn.connect('clicked', self.on_button_clicked)
        self.main.append(btn)
        # setup overlay box
        btn = Gtk.Button()
        btn.props.label = "Touch Me Softly"
        btn.props.valign = Gtk.Align.CENTER
        btn.props.halign = Gtk.Align.CENTER
        btn.props.vexpand = True
        btn.props.hexpand = True
        btn.connect('clicked', self.on_button_clicked)
        self.overlay.append(btn)
        self.add_custom_styling(self)
        # Get the shortcuts window and add styling
        shortcut_win = self.get_help_overlay()
        self.add_custom_styling(shortcut_win)
        self.create_action('new', self.menu_handler)
        self.create_action('about', self.menu_handler)
        self.create_action('quit', self.menu_handler)

    def on_button_clicked(self, widget):
        label = widget.get_label()
        print(f'Button {label} Pressed')
        if label == 'Toggle Overlay':
            visible = self.overlay.get_visible()
            self.overlay.set_visible(not visible)

    def menu_handler(self, action, state):
        """ Callback for  menu actions"""
        name = action.get_name()
        print(f'active : {name}')
        if name == 'quit':
            self.close()

    def load_css(self):
        """create a provider for custom styling"""
        css_provider = None
        css_provider = Gtk.CssProvider()
        css_path = RESOURCE_PATH + 'css/main.css'
        try:
            css_provider.load_from_resource(resource_path=css_path)
        except GLib.Error as e:
            print(f"Error loading CSS : {e} ")
            return None
        print(f'loading custom styling from resource: {css_path}')
        return css_provider

    def _add_widget_styling(self, widget):
        if self.css_provider:
            context = widget.get_style_context()
            context.add_provider(
                self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def add_custom_styling(self, widget):
        self._add_widget_styling(widget)
        # iterate children recursive
        for child in widget:
            self.add_custom_styling(child)

    def create_action(self, name, callback):
        """ Add an Action and connect to a callback """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)

