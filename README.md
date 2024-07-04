# OpenSeeFace Facetracking Wrapper

This is just a little utility to provide a graphical interface for OpenSeeFace Facetracking.

- It allows to select a webcam from al ist of available devices
- Specify a port for teh facetracker to listen
- video width and height
- choose supported frames per second of a selected device

![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/facetracker.png)
![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/facetracker_2.png)
![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/facetracker_3.png)
![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/facetracker_4.png)

## Development Requirements

- gcc
- python3-devel
- python3-pip
- gobject-introspection-devel

### OpenSeeFace prebuild binary

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