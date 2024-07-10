#!/usr/bin/env python3
import sys

from os import environ

pkgdatadir = '@pkgdatadir@'
if environ.get("FLATPAK_ID") is not None:
    sys.path.insert(1, pkgdatadir)

from facetracker.const import APP_ID, LOCALE_DIR
from facetracker.main_frame import OpenSeeFaceFacetrackingWrapper

import gettext

gettext.install('facetracker', LOCALE_DIR)


def run():
    OpenSeeFaceFacetrackingWrapper(application_id=APP_ID).run(sys.argv)


if __name__ == '__main__':
    OpenSeeFaceFacetrackingWrapper(application_id=APP_ID).run(sys.argv)
