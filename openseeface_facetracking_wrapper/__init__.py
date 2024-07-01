import sys

from openseeface_facetracking_wrapper.main_frame import OpenSeeFaceFacetrackingWrapper

if __name__ == "__main__":
    OpenSeeFaceFacetrackingWrapper(application_id="de.zray.openseeface_facetracking_wrapper").run(sys.argv)
