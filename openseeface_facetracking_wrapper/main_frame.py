import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facetracking = False

        self.set_default_size(600, 300)
        self.set_title("OpenSeeFace Wrapper")
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.bt_launch = Gtk.ToggleButton(label="Start Tracking")
        self.bt_launch.set_tooltip_text("Start/Stop OpenSeeFace Facetracker")
        self.bt_launch.connect("clicked", self.start_stop_facetracker)
        self.header.pack_end(self.bt_launch)

    def start_stop_facetracker(self, button):
        if not self.facetracking:
            self.facetracking = True
            self.bt_launch.set_label("Stop Tracking")
        else:
            self.facetracking = False
            self.bt_launch.set_label("Start Tracking")


class OpenSeeFaceFacetrackingWrapper(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)
        self.connect("shutdown", self.on_close)
        self.win = None

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

    def on_close(self):
        self.win.stop_core()
