# Kinect-Skeleton-Tracker
Module for using Kinect for general purpose skeleton tracking

**Note: While the general format of this will be the same as the Kinetic Maze project and Kinect Library, the files are not interchangeable**

## Dependencies
[Libfreenect](https://github.com/OpenKinect/libfreenect),
[Openni2](https://github.com/occipital/openni2),
[NiTE2](http://jaist.dl.sourceforge.net/project/roboticslab/External/nite/NiTE-Linux-x64-2.2.tar.bz2)

**Installation instructions coming soon!**

## Organization

#File descriptions - short

* /skeleton_tracker - Python Folder
  * /skeleton_tracker/\_\_init\_\_.py
  * /skeleton_tracker/\_\_main\_\_.py  - The file that is run by run_tracker.sh
  * /skeleton_tracker/composition.py - File containing class with main loops
  * /skeleton_tracker/config.json - A config file, if modified breaks the Json decoder.
  * /skeleton_tracker/config.py - Reads config? Unsure of exactly what it does outside of being a config
  * /skeleton_tracker/tracked_user.py - Classes for assigning data to the active user
  * /skeleton_tracker/tracker.py - Converts tracking module (C) data to be used by python
  * /skeleton_tracker/draw.py - Pygame code to draw the skeleton tracked
* /tracking-module - C Tracker Folder
  * /tracking-module/main.cpp - C source code
  * /tracking-module/Makefile
  * /tracking-module/trackbody - Compiled code, if it does not exist, run `make` in this directory.
* /README.md - Readme
* /run_tracker.sh - Used to run the tracker (the entire project)

#File descriptions - long (as needed)


## Todo
- [x] Modify tracking-module code to return full body data instead of just hands
- [x] (Re)write Python parser for new tracking module
- [x] Modify tracker.py
- [x] Modify tracked_user.py
- [ ] Write skeleton display - pygame

- [ ] Fix the JSON, delete the physics and dab code
- [ ] Rename trackhands to trackbody, modify trackers to use new name

## Notes
When running the code, it displays all the data but claims an error and "invalid line," will disregard and move on to skeleton drawing
The plan is to draw each line between joints as the same length, but change the angle of display and a fixed point. first fixed point will be the torso, at 0,0 or something
