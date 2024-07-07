# OpenSeeFace Facetracking Wrapper

Simple wrapper UI for OpenSeeFace's facetracker.  

- Start / Stop the tracker
- Select Webcam
- Select video mode (width, height, frames per second)
- Select tracking model used by the facetracker
- Set IP and Port for the tracker to listen

![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/screenshots/facetracker.png)
![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/screenshots/facetracker_2.png)
![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/screenshots/facetracker_3.png)
![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/screenshots/facetracker_4.png)

## Development Requirements

- gcc
- python3-devel
- python3-pip
- gobject-introspection-devel

### Setup
- Clone repository
- pip install -e .

#### OpenSeeFace prebuild binary

To ease up flatpak distribution Facetracker uses OpenSeeFace's facetracker as a pre-build binary.  
Get is as follows:

- `cd ../`
- `git clone git@github.com:emilianavt/OpenSeeFace.git`
- `cd OpenSeeFace`
- `pip install onnxruntime opencv-python pillow numpy`
- `pip install -U pyinstaller`
- `pyinstaller ./facetracker.py`
- `cp models ./dist/facetracker/`
- `cd ../Facetracker/facetracker`
- `ln -s ../../OpenSeeFace/dist/facetracker ./OpenSeeFace`
