import os
import signal
import subprocess

import gi
from gi.repository import Gio

from facetracker import webcam_info
from facetracker.const import VERSION, APP_NAME

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facetracking = False
        self.face_process: int
        self.about_ui: Adw.AboutWindow
        self.bt_launch: Gtk.ToggleButton
        self.cam_combo_row: Adw.ComboRow

        self.set_title(APP_NAME + " (" + VERSION + ")")
        self.set_default_size(600, 300)
        self._build_title_bar()
        self._build_main_content()
        self._build_header_menu()

    def _build_title_bar(self):
        header = Gtk.HeaderBar()

        self.bt_launch = Gtk.ToggleButton(label="Start Tracking")
        self.bt_launch.set_tooltip_text("Start/Stop OpenSeeFace Facetracker")
        self.bt_launch.connect("clicked", self._start_stop_facetracker)
        self.bt_launch.add_css_class("suggested-action")
        header.pack_start(self.bt_launch)
        self.set_titlebar(header)

    def _build_header_menu(self):
        pass

    def _build_about(self):
        self.about_ui = Adw.AboutWindow()
        self.about_ui.set_transient_for(self)
        self.about_ui.set_application_name(APP_NAME)
        self.about_ui.set_version(VERSION)
        self.about_ui.set_developer_name("Imo 'Vortex Acherontic' Hester")
        self.about_ui.set_license_type(license_type=Gtk.License.MIT_X11)
        self.about_ui.set_comments("A graphical user interface to launch OpenSeeFace's Facetracker."
                                   "\nThis application is meant to be used in conjunction with the likes of "
                                   "VTube Studio VSeeFace and the likes as these do not offer a native Linux version"
                                   "and thus facetracking using a Webcam does not work in Wine or Proton.")
        self.about_ui.show()

    def _build_main_content(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_end(10)
        main_box.set_margin_start(10)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)

        boxed_list = Gtk.ListBox()
        boxed_list.set_selection_mode(Gtk.SelectionMode.NONE)
        boxed_list.add_css_class("boxed-list")
        main_box.append(boxed_list)

        self._build_webcam_cb(webcam_info.get_webcams())
        # cam_combo_row.add_suffix(self.cam_string_list)
        boxed_list.append(self.cam_combo_row)

        self.set_child(main_box)

    def _build_webcam_cb(self, webcams):
        self.cam_combo_row = Adw.ComboRow()
        self.cam_combo_row.set_title("Webcam")
        self.cam_combo_row.set_subtitle("Select which camera to use for tracking")
        self.cam_combo_row.set_activatable(True)
        cam_string_list = Gtk.StringList()

        for webcam in webcams:
            index = str(webcam.device_index)
            name = index + ": " + webcam.device_name
            cam_string_list.append(name)
        self.cam_combo_row.set_model(cam_string_list)
        self.cam_combo_row.set_enable_search(True)

    def _start_stop_facetracker(self, button):
        if not self.facetracking:
            self.facetracking = True
            self.bt_launch.set_label("Stop Tracking")
            self.bt_launch.remove_css_class("suggested-action")
            self.bt_launch.add_css_class("destructive-action")
            selected_item = self.cam_combo_row.get_selected_item()
            camera_index = selected_item.get_string().split(":")[0]
            video_width = 1280
            video_height = 720
            script_to_run = "facetracker/OpenSeeFace/facetracker.py"
            self.face_process = subprocess.Popen(
                ["python3", script_to_run, "-W", str(video_width), "-H", str(video_height), "-c", str(camera_index),
                 "--discard-after", "0", "--scan-every", "0", "--no-3d-adapt", "1", "--max-feature-updates", "900"])
        else:
            self.facetracking = False
            self.bt_launch.add_css_class("suggested-action")
            self.bt_launch.remove_css_class("destructive-action")
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
