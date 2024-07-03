import os
import subprocess


class VideoMode:
    def __init__(self, width: int, height: int, fps: int):
        self.width = width
        self.height = height
        self.fps = fps


class WebcamInfo:

    def __init__(self, index: int, device_name: str):
        self.device_index = index
        self.device_name = device_name
        self.video_modes = []

    def add_video_mode(self, video_mode: VideoMode):
        self.video_modes.append(video_mode)

    def get_video_modes(self) -> [VideoMode]:
        return self.video_modes


def get_webcams() -> [WebcamInfo]:
    """
    TODO: Some idiot patched the Linux Kernel to list every webcam twice in /sys/class/video4linux/video* (and /dev/)
    Because of some random metadata.
    However the file "index" is unusable this way as it is not the real index. Because it looks like this on a multi
    webcam system:

    Cam found | Index: 1 Name: C922 Pro Stream Webcam
    Cam found | Index: 1 Name: USB3. 0 capture: USB3. 0 captur
    Cam found | Index: 0 Name: C922 Pro Stream Webcam
    Cam found | Index: 0 Name: USB3. 0 capture: USB3. 0 captur

    This is garbage as not both devices can be index 0 and 1 at teh same time while cam with index 1 is actually index 2
    ... ... ... ... Well we'll just use the number of the directory /sys/class/video4linux/video* here.

    So we need to merge these devices somehow to not list every device twice.
    This was supposed to be a simple application until now ...
    """
    device_path = "/sys/class/video4linux/"
    webcams = []

    for subdir, dirs, files in os.walk(device_path):
        for video_dir in dirs:
            device_index_result = video_dir.split("video")[1]
            device_name_result = subprocess.run(["cat", device_path + video_dir + "/name"], stdout=subprocess.PIPE)

            device_index = int(device_index_result)
            device_name = device_name_result.stdout.decode("utf-8").rstrip()
            print("Cam found | Index: " + str(device_index) + " Name: " + device_name)
            webcam = WebcamInfo(device_index, device_name)
            webcams.append(webcam)

    return webcams
