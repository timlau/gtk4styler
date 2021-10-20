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
from gi.repository import Gtk, GLib


@Gtk.Template(resource_path='/dk/rasmil/Gtk4Styler/ui/window.ui')
class Gtk4stylerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'Gtk4stylerWindow'

    main = Gtk.Template.Child()
    overlay = Gtk.Template.Child()
    headerbox = Gtk.Template.Child()
    hdr_menu = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.css_provider = self.load_css()
        self.set_title("Gtk4 Styler")
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
        # label = Gtk.Label()
        # label.set_text("Hallo")
        # self.headerbox.append(label)
        builder = Gtk.Builder()
        builder.add_from_resource(resource_path='/dk/rasmil/Gtk4Styler/ui/mainmenu.ui')
        menu = builder.get_object('app_menu')
        print(type(menu))
        self.hdr_menu.set_menu_model(menu)        
        self.add_custom_styling(self)

    def on_button_clicked(self, widget):
        label = widget.get_label()
        print(f'Button {label} Pressed')
        if label == 'Toggle Overlay':
            visible = self.overlay.get_visible()
            self.overlay.set_visible(not visible)


    def load_css(self):
        """create a provider for custom styling"""
        css_provider = None
        css_provider = Gtk.CssProvider()
        css_path = '/dk/rasmil/Gtk4Styler/css/main.css'
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
