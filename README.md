# OpenSeeFace Facetracking Wrapper

<div style="text-align: center;">

![logo](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/icons/hicolor/scalable/apps/de.z_ray.Facetracker.svg)

</div>

Simple wrapper UI for OpenSeeFace's facetracker.  

- Start / Stop the tracker
- Select Webcam
- Select video mode (width, height, frames per second)
- Select tracking model used by the facetracker
- Set IP and Port for the tracker to listen
<div style="text-align: center;">

![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/screenshots/facetracker.png)
![screenshot](https://raw.githubusercontent.com/Z-Ray-Entertainment/Facetracker/main/facetracker/data/screenshots/facetracker_2.png)

</div>

### Download
<div style="text-align: center;">
<a href="https://flathub.org/apps/de.z_ray.Facetracker">
  <img width='240' alt='Download on Flathub' src='https://dl.flathub.org/assets/badges/flathub-badge-en.png'/>
</a>
</div>

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
