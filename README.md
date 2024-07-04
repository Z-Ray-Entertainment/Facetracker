# OpenSeeFace Facetracking Wrapper

Simple wrapper UI for OpenSeeFace's facetracker.  

- Start / Stop the tracker
- Select Webcam
- Select video mode (width, height, frames per second)
- Select tracking model used by the facetracker
- Set IP and Port for the tracker to listen

![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/facetracker.png)
![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/facetracker_2.png)
![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/facetracker_3.png)
![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/facetracker_4.png)

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

- Clone git@github.com:emilianavt/OpenSeeFace.git
- cd OpenSeeFace/
- pip install onnxruntime opencv-python pillow numpy
- pip install -U pyinstaller
- This will build facetracker to a subdirectory called dist
- Additionally copy the folder models from the source path to dist/facetracker/
- Then provide a symlink to the dist directory inside Facetracker
- Inside th Facetracker root directory
- cd facetracker
- ln -s ../../OpenSeeFace/dist/facetracker ./OpenSeeFace