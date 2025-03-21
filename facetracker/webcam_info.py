import math
import os
import re
import subprocess


class VideoMode:
    def __init__(self, width: int, height: int, fps: int):
        self.width = width
        self.height = height
        self.fps = fps

    def to_string(self) -> str:
        return str(self.width) + "x" + str(self.height) + "@" + str(self.fps)


class WebcamInfo:

    def __init__(self, index: int, device_name: str, device_path: str):
        self.device_index = index
        self.device_name = device_name
        self.device_path = device_path
        self.video_modes = {}

    def add_video_mode(self, mode: VideoMode, codec: str):
        if codec not in self.video_modes:
            self.video_modes[codec] = []
        self.video_modes[codec].append(mode)

    def get_osf_video_modes(self) -> [VideoMode]:
        supported_formats = self.video_modes["default"]
        for codec in ["YUYV", "NV12", "YU12"]:
            if codec in self.video_modes:
                # Will return right away if the first known working format was found.
                return supported_formats + self.video_modes[codec]
        return supported_formats

    def get_all_video_modes(self) -> {}:
        return self.video_modes

    def debug_info(self):
        debug_info = str(self.device_index) + " " + self.device_name + " " + self.device_path + "\n"
        for codec in self.video_modes:
            debug_info += codec + ":\n"
            for mode in self.video_modes[codec]:
                debug_info += mode.to_string() + "\n"
        return debug_info

    def print_info(self):
        print(self.debug_info())


def get_webcams() -> [WebcamInfo]:
    """
    Some idiot patched the Linux Kernel to list every webcam twice in /sys/class/video4linux/video* (and /dev/) because
    of some random metadata. However, the file "index" is unusable this way as it is not the real index anymore:

    Cam found | Index: 1 Name: C922 Pro Stream Webcam
    Cam found | Index: 1 Name: USB3. 0 capture: USB3. 0 captur
    Cam found | Index: 0 Name: C922 Pro Stream Webcam
    Cam found | Index: 0 Name: USB3. 0 capture: USB3. 0 captur

    Both device can't be index 0 and 1 simultaneously.

    To get the "real" device index of each webcam we first gather all devices found.
    Then look for devices sharing a similar realpath and then take the device with the lowest index of each path as
    the actual device. THis is based on the assumption that a metadate device node can't be created before the actual
    device was created to gather the metadata from.

    Example:
    /sys/devices/pci0000:00/0000:00:02.1/0000:03:00.0/0000:04:0c.0/0000:0e:00.0/usb1/1-3/1-3:1.0/video4linux/video3 <-- fake device
    /sys/devices/pci0000:00/0000:00:02.1/0000:03:00.0/0000:04:0c.0/0000:0e:00.0/usb1/1-3/1-3:1.0/video4linux/video2 <-- real device
    /sys/devices/pci0000:00/0000:00:08.1/0000:10:00.3/usb4/4-1/4-1:1.0/video4linux/video1 <-- fake device
    /sys/devices/pci0000:00/0000:00:08.1/0000:10:00.3/usb4/4-1/4-1:1.0/video4linux/video0 <-- real device

    To get the real path of the device we use realpath on the /sys/class/video4linux/video* symbolic link and split on
    the keyword video4linux (see above).
    """
    video_devices_path = "/sys/class/video4linux/"
    webcams = []

    for subdir, dirs, files in os.walk(video_devices_path):
        found_devices = {}
        for video_dir in dirs:
            device_index = int(video_dir.split("video")[1])

            device_name_result = subprocess.run(["cat", video_devices_path + video_dir + "/name"],
                                                stdout=subprocess.PIPE)
            device_name = device_name_result.stdout.decode("utf-8").rstrip()
            device_path_result = subprocess.run(["realpath", video_devices_path + video_dir], stdout=subprocess.PIPE)
            device_path = device_path_result.stdout.decode("utf-8").rstrip().split("video4linux")[0]

            webcaminfo = WebcamInfo(device_index, device_name, device_path)

            already_found_device = found_devices.get(device_path)
            if already_found_device is None:
                found_devices[device_path] = webcaminfo
            else:
                """
                The video* device with the lowest number is initialized first in Linux.
                Medatadata are getting created after wards. This means if two video* devices share a similar device path
                then the one with the lowest number is the real hardware which an be read. The other one is just a dummy
                """
                if already_found_device.device_index > webcaminfo.device_index:
                    found_devices[device_path] = webcaminfo

        webcams = []
        for webcam_info in found_devices:
            webcam = found_devices[webcam_info]
            all_video_modes = _get_video_modes(webcam.device_index)
            for codec in all_video_modes:
                for mode in all_video_modes[codec]:
                    webcam.add_video_mode(mode, codec)
            webcams.append(webcam)
    return webcams


def _get_video_modes(device_index: int) -> [VideoMode]:
    """"
    Until I found a sophisticated way of getting the actually supported resolutions and frame rates for each
    webcam these default must suffice.
    Also it is important that you can not tell opencv (what OSF uses for it's webcam access) which video format
    to use and it will always default to RAW while MJPEG would allow for a wider range of resolutions and
    frame rates.

    - linuxpy does not offer a complete list of supported device capabilities
    - v4l2.py is disconnected and have actually emerged into linuxpy
    - Parsing the output of "v4l2-ctl -d /dev/video* --list-formats-ext" seems a bit too daunting atm, but it is the
    best option I know of as of now.
    - Using "ffmpeg -hide_banner -f v4l2 -list_formats all -i /dev/video*" lacks the frame rate info but has the
    best format
    """

    command = ["v4l2-ctl", "-d", "/dev/video" + str(device_index), "--list-formats-ext"]
    v4l2_result = subprocess.run(command, stdout=subprocess.PIPE)
    v4l2_formats = v4l2_result.stdout.decode("utf-8").rstrip().split("\n")

    collect_new_video_mode = False
    current_resolution = "0x0"
    current_format = "default"
    videomode_default = VideoMode(width=640, height=360, fps=24)  # OSF default always added as fallback
    video_modes = {current_format: [videomode_default]}

    for field in v4l2_formats:
        line = field.replace("\t", "").replace(":", "").replace("(", "").replace(")", "")
        cells = line.split(" ")

        res = re.match(r"\[[0123456789]\]", cells[0])
        if res is not None:
            current_format = cells[1].replace("'", "")
            video_modes[current_format] = []
            collect_new_video_mode = True

        match cells[0]:
            case "Size":
                if collect_new_video_mode:
                    current_resolution = cells[2]
            case "Interval":
                if collect_new_video_mode:
                    current_frame_rate = cells[3]
                    res = current_resolution.split("x")
                    fps = int(math.ceil(float(current_frame_rate)))
                    new_video_mode = VideoMode(int(res[0]), int(res[1]), fps)
                    video_modes[current_format].append(new_video_mode)
    return video_modes
