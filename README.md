# Kinect-Skeleton-Tracker
Module for using Kinect for general purpose skeleton tracking

**Note: While the general format of this will be the same as the Kinetic Maze project and Kinect Library, the files are not interchangeable**

## Dependencies
[Libfreenect](https://github.com/OpenKinect/libfreenect),
[Openni2](https://github.com/occipital/openni2),
[NiTE2](http://jaist.dl.sourceforge.net/project/roboticslab/External/nite/NiTE-Linux-x64-2.2.tar.bz2)

### Installing Dependencies

1. Install Libfreenect (v.1, not v.2): `sudo apt install freenect`
2. Install OpenNI2: `sudo apt install libopenni2-0 libopenni2-dev`

#### Install NiTE:
Original instructions can be found in install_instructions.txt!

1. Get NiTE:
  ```
  wget http://jaist.dl.sourceforge.net/project/roboticslab/External/nite/NiTE-Linux-x64-2.2.tar.bz2
  ```
2. Unpack NiTe:
  ```
  tar -xvjf NiTE-Linux-x64-2.2.tar.bz2
  ```
3. Copy binaries to the right directory:
  ```
  sudo ln -s $PWD/NiTE-Linux-x64-2.2/Redist/libNiTE2.so /usr/local/lib/
  sudo ln -s $PWD/NiTE-Linux-x64-2.2/Include /usr/local/include/NiTE-Linux-x64-2.2
  sudo ldconfig
  mkdir /usr/include/nite
  cp $PWD/NiTE-Linux-x64-2.2/Include/* /usr/include/nite/
  cp $PWD/NiTE-Linux-x64-2.2/Redist/libNiTE2.so /usr/lib/
  cp -r $PWD/NiTE-Linux-x64-2.2/Redist/NiTE2 /usr/lib/
  ```
4. Fix headers
  - Change Niteheaders to use correct openni headers <openni2/package> instead of old <package> anything with OniXXXXXXX
  ```
  sudo vim /usr/include/nite/NiteCAPI.h
  sudo vim /usr/include/nite/NiteCTypes.h
  sudo vim /usr/include/nite/NiteVersion.h
  sudo vim /usr/include/nite/NiTE.h
  ```

5. Build OpenNNI2-FreenectDriver
  ```
  sudo apt install cmake make build-essential git
  sudo apt install libusb-dev

  git clone https://github.com/OpenKinect/libfreenect
  cd libfreenect
  mkdir build
  cd build
  cmake .. -DBUILD_OPENNI_DRIVER=ON
  cd .. # sometimes the makefile is in a different directory. use your eyes
  make
  ```
6. place libFreenectDriver.so.0 in /usr/lib/OpenNI2/Drivers
  ```
  cp libFreenectDriver.so /usr/lib/OpenNI2/Drivers/
  cp libFreenectDriver.so libFreenectDriver.so.0 			# need to be a .so.0 for some reason
  ```

## Organization

### File descriptions - short

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

### File descriptions - long (as needed)


## Todo
- [x] Modify tracking-module code to return full body data instead of just hands
- [x] (Re)write Python parser for new tracking module
- [x] Modify tracker.py
- [x] Modify tracked_user.py
- [ ] Write skeleton display - pygame

- [ ] Fix the JSON, delete the physics and dab code
- [ ] Rename trackhands to trackbody, modify trackers to use new name
- [ ] Update gitignore to ignore more files 

## Notes
When running the code, it displays all the data but claims an error and "invalid line," will disregard and move on to skeleton drawing
The plan is to draw each line between joints as the same length, but change the angle of display and a fixed point. first fixed point will be the torso, at 0,0 or something

ERROR   | 2019-12-04 12:04:09,139 | skeleton_tracker.tracker | invalid line: b'BODY DATA: 1|(-17.44, 350.42, 932.55)|(-49.54, 131.72, 943.17)|(-71.62, -96.91, 947.37)|(93.86, 119.25, 1017.80)|(137.14, -184.46, 1070.43)|(204.34, -501.58, 1043.09)|(-192.95, 144.20, 868.54)|(-276.34, -146.31, 831.78)|(-281.21, -468.98, 769.79)|( 0.08, -333.71, 1000.37)|( 0.08, -793.19, 1000.37)|( 0.08, -1235.00, 1000.25)|(-187.48, -317.39, 902.76)|(-187.48, -776.87, 902.76)|(-187.47, -1218.68, 902.73)'
