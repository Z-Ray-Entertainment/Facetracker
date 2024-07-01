import sys

from openseeface_facetracking_wrapper.main_frame import OpenSeeFaceFacetrackingWrapper

VERSION = "24.7.1"


# Press the green button in the gutter to run the script.
def run():
    OpenSeeFaceFacetrackingWrapper(application_id="de.zray.openseeface_facetracking_wrapper").run(sys.argv)
