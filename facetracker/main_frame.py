import gi

from facetracker import webcam_info, face_wrapper
from facetracker.const import VERSION, APP_NAME
from facetracker.webcam_info import VideoMode

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.about_ui: Adw.AboutWindow
        self.bt_launch: Gtk.ToggleButton
        self.cam_combo_row: Adw.ComboRow
        self.video_modes_row: Adw.ComboRow
        self.tracking_mode_row: Adw.ComboRow
        self.advanced_row: Adw.ExpanderRow
        self.ip_text: Adw.EntryRow
        self.port_text: Adw.EntryRow
        self.webcam_infos = webcam_info.get_webcams()

        self.set_title(APP_NAME)
        self._build_title_bar()
        self._build_main_content()
        self._build_header_menu()

    def _build_title_bar(self):
        header = Gtk.HeaderBar()

        self.bt_launch = Gtk.ToggleButton(label=_("Start face tracking"))
        self.bt_launch.set_tooltip_text(_("Start or Stop the OpenSeeFace face tracker"))
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

        if len(self.webcam_infos) > 0:
            boxed_list = Gtk.ListBox()
            boxed_list.set_selection_mode(Gtk.SelectionMode.NONE)
            boxed_list.add_css_class("boxed-list")
            main_box.append(boxed_list)

            self._build_webcam_cb()
            boxed_list.append(self.cam_combo_row)

            self.tracking_settings_row = Adw.ExpanderRow()
            self.tracking_settings_row.set_title(_("Face tracking Settings"))
            self._build_video_modes()
            self.tracking_settings_row.add_row(self.video_modes_row)
            self._build_tracking_mode_selection()
            self.tracking_settings_row.add_row(self.tracking_mode_row)
            boxed_list.append(self.tracking_settings_row)

            self.server_settings_row = Adw.ExpanderRow()
            self.server_settings_row.set_title(_("Server Settings"))
            self._build_server_settings(self.server_settings_row)
            boxed_list.append(self.server_settings_row)
        else:
            no_cams_label = Gtk.Label()
            no_cams_label.set_label(_("No webcams found!"))
            main_box.append(no_cams_label)

        self.set_child(main_box)

    def _build_tracking_mode_selection(self):
        """
        --model {-3,-2,-1,0,1,2,3,4}
                        This can be used to select the tracking model. Higher numbers are models with better tracking
                        quality, but slower speed, except for
                        model 4, which is wink optimized.
                        Models 1 and 0 tend to be too rigid for expression and blink detection.
                        Model -2 is roughly equivalent to model 1, but faster.
                        Model -3 is between models 0 and -1. (default: 3)
        """
        self.tracking_mode_row = Adw.ComboRow()
        self.tracking_mode_row.set_title(_("Model:"))
        self.tracking_mode_row.set_subtitle(_("Set the tracking model used by the face tracker"))
        model_string_list = Gtk.StringList()
        model_string_list.append("-1: " + _("Superfast"))
        model_string_list.append("0: " + _("Fastest"))
        model_string_list.append("1: " + _("Faster"))
        model_string_list.append("2: " + _("Normal"))
        model_string_list.append("3: " + _("Default"))
        model_string_list.append("4: " + _("Wink optimized"))
        self.tracking_mode_row.set_model(model_string_list)
        self.tracking_mode_row.set_selected(4)

    def _build_server_settings(self, boxed_list: Adw.ExpanderRow):
        ip_and_port_row = Adw.ActionRow()

        self.ip_text = Adw.EntryRow()
        self.ip_text.set_title(_("IP Address:"))
        self.ip_text.set_text("0.0.0.0")
        self.port_text = Adw.EntryRow()
        self.port_text.set_title(_("Port:"))
        self.port_text.set_text("11573")
        ip_and_port_row.add_prefix(self.ip_text)
        ip_and_port_row.add_suffix(self.port_text)
        boxed_list.add_row(ip_and_port_row)

    def _build_webcam_cb(self):
        self.cam_combo_row = Adw.ComboRow()
        self.cam_combo_row.set_title(_("Webcam"))
        self.cam_combo_row.set_subtitle(_("Select which camera to use for face tracking"))
        self.cam_combo_row.set_activatable(True)
        cam_string_list = Gtk.StringList()

        for webcam in self.webcam_infos:
            index = str(webcam.device_index)
            name = index + ": " + webcam.device_name
            cam_string_list.append(name)
        self.cam_combo_row.set_model(cam_string_list)

    def _build_video_modes(self):
        self.video_modes_row = Adw.ComboRow()
        self.video_modes_row.set_title(_("Video Mode:"))
        self.video_modes_row.set_subtitle(_("Select the video mode to be used for face tracking"))
        mode_string_list = Gtk.StringList()
        selected_cam = self._get_webcam_by_index(self._get_selected_camera_index())
        for mode in selected_cam.video_modes:
            mode_string_list.append(mode.to_string())
        self.video_modes_row.set_model(mode_string_list)

    def _get_selected_camera_index(self) -> int:
        selected_item = self.cam_combo_row.get_selected_item()
        return int(selected_item.get_string().split(":")[0])

    def _get_selected_video_mode(self) -> VideoMode:
        selected_video_mode = self.video_modes_row.get_selected_item()
        fps_split = selected_video_mode.get_string().split("@")
        fps: int = int(fps_split[1])
        resolution = fps_split[0].split("x")
        width: int = int(resolution[0])
        height: int = int(resolution[1])
        return VideoMode(width, height, fps)

    def _start_stop_facetracker(self, button):
        if len(self.webcam_infos) > 0:
            if not face_wrapper.tracking_in_progress():
                selected_video_mode = self._get_selected_video_mode()
                video_width = selected_video_mode.width
                video_height = selected_video_mode.height
                frame_rate = selected_video_mode.fps
                camera_index = self._get_selected_camera_index()
                tracking_mode = str(self.tracking_mode_row.get_selected_item().get_string().split(":")[0])
                server_ip = self.ip_text.get_text()
                server_port = self.port_text.get_text()

                if face_wrapper.run_facetracker(video_width, video_height, frame_rate, camera_index, tracking_mode,
                                                server_ip, server_port):
                    self.bt_launch.set_label(_("Stop face tracking"))
                    self.bt_launch.remove_css_class("suggested-action")
                    self.bt_launch.add_css_class("destructive-action")
            else:
                if face_wrapper.tracking_in_progress():
                    if face_wrapper.stop_facetracker():
                        self.bt_launch.add_css_class("suggested-action")
                        self.bt_launch.remove_css_class("destructive-action")
                        self.bt_launch.set_label(_("Start face tracking"))

    def _get_webcam_by_index(self, index: int):
        for cam in self.webcam_infos:
            if cam.device_index == index:
                return cam


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
        if face_wrapper.tracking_in_progress():
            face_wrapper.stop_facetracker()
