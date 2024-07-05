#!/usr/bin/env python3
import sys

pkgdatadir = '@pkgdatadir@'
sys.path.insert(1, pkgdatadir)

from facetracker.const import APP_ID
from facetracker.main_frame import OpenSeeFaceFacetrackingWrapper


def run():
    OpenSeeFaceFacetrackingWrapper(application_id=APP_ID).run(sys.argv)
