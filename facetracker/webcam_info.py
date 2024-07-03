import os
import subprocess


class VideoMode:
    def __init__(self, width: int, height: int, fps: int):
        self.width = width
        self.height = height
        self.fps = fps


class WebcamInfo:

    def __init__(self, index: int, device_name: str, device_path: str):
        self.device_index = index
        self.device_name = device_name
        self.device_path = device_path
        self.video_modes = []

    def add_video_mode(self, video_mode: VideoMode):
        self.video_modes.append(video_mode)

    def get_video_modes(self) -> [VideoMode]:
        return self.video_modes

    def print_info(self):
        print(str(self.device_index) + " " + self.device_name + " " + self.device_path)


def get_webcams() -> [WebcamInfo]:
    """
    Some idiot patched the Linux Kernel to list every webcam twice in /sys/class/video4linux/video* (and /dev/) because
    of some random metadata. However the file "index" is unusable this way as it is not the real index. Because it
    looks like this on a multi webcam system:

    Cam found | Index: 1 Name: C922 Pro Stream Webcam
    Cam found | Index: 1 Name: USB3. 0 capture: USB3. 0 captur
    Cam found | Index: 0 Name: C922 Pro Stream Webcam
    Cam found | Index: 0 Name: USB3. 0 capture: USB3. 0 captur

    This is garbage as not both devices can be index 0 and 1 at the same time while cam with index 1 is actually index 2
    ... ... ... ... Well we'll just use the number of the directory /sys/class/video4linux/video* here.

    So we need to merge these devices somehow to not list every device twice.
    This was supposed to be a simple application until now ...

    Possible solution: readlink /sys/class/video4linux/video* and then compare which do point to the same device.
    Edit: readlink returns non zero status which causes readlink to "fail" while outputting the correct thing.
    Realpath so instead it is ...
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

            """"
            Example:
            /sys/devices/pci0000:00/0000:00:02.1/0000:03:00.0/0000:04:0c.0/0000:0e:00.0/usb1/1-3/1-3:1.0/video4linux/video3 <-- fake device
            /sys/devices/pci0000:00/0000:00:08.1/0000:10:00.3/usb4/4-1/4-1:1.0/video4linux/video1  <-- fake device
            /sys/devices/pci0000:00/0000:00:02.1/0000:03:00.0/0000:04:0c.0/0000:0e:00.0/usb1/1-3/1-3:1.0/video4linux/video2 <-- real device
            /sys/devices/pci0000:00/0000:00:08.1/0000:10:00.3/usb4/4-1/4-1:1.0/video4linux/video0 <-- real device
            """
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
            # TODO: Get video modes
            webcams.append(webcam)
    return webcams
