import os
import signal
import subprocess

is_tracking: bool = False
face_process: subprocess


def run_facetracker(width: int, height: int, fps: int, device_index: int, tracking_mode: int, server_ip: str,
                    server_port: int) -> bool:
    global is_tracking
    global face_process

    if not is_tracking:
        try:
            is_tracking = True
            script_to_run = "facetracker/OpenSeeFace/facetracker"
            face_process = subprocess.Popen(
                [script_to_run, "-W", str(width), "-H", str(height), "-c", str(device_index),
                 "--discard-after", "0", "--scan-every", "0", "--no-3d-adapt", "1", "--max-feature-updates", "900",
                 "-s", "1", "-p", str(server_port), "-i", server_ip, "--model", tracking_mode])
            return True
        except Exception as e:
            pass
    return False


def stop_facetracker() -> bool:
    global is_tracking

    if is_tracking:
        try:
            is_tracking = False
            os.kill(face_process.pid, signal.SIGKILL)
            return True
        except Exception as e:
            pass
    return False


def tracking_in_progress():
    global is_tracking
    return is_tracking
