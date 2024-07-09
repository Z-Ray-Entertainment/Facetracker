from os import environ

if environ.get("FLATPAK_ID") is not None:
    VERSION = "@VERSION@"
    LOCALE_DIR = "@localedir@"
else:
    VERSION = "dev"
    LOCALE_DIR = "facetracker/data/po"
APP_NAME = "Facetracker"
APP_ID = "de.z_ray.Facetracker"

