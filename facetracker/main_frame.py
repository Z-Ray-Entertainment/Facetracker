import os
import signal
import subprocess

import gi

from facetracker.const import VERSION, APP_NAME

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facetracking = False
        self.face_process = None

        self.set_default_size(600, 300)
        self.set_title(APP_NAME + " (" + VERSION + ")")
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
            camera_index = 2
            video_width = 1280
            video_height = 720
            script_to_run = "facetracker/OpenSeeFace/facetracker.py"
            self.face_process = subprocess.Popen(
                ["python3", script_to_run, "-W", str(video_width), "-H", str(video_height), "-c", str(camera_index),
                 "--discard-after", "0", "--scan-every", "0", "--no-3d-adapt", "1", "--max-feature-updates", "900"])
        else:
            self.facetracking = False
            self.bt_launch.set_label("Start Tracking")
            os.kill(self.face_process.pid, signal.SIGKILL)


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

