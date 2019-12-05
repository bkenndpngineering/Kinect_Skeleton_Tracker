# Kinect-Skeleton-Tracker
Module for using Kinect for general purpose skeleton tracking

**Note: While the general format of the NiTE implementation will be the same as the Kinetic Maze project and Kinect Library, the files are not interchangeable**

## Dependencies
[Libfreenect](https://github.com/OpenKinect/libfreenect),
[Openni2](https://github.com/occipital/openni2),
[NiTE2](http://jaist.dl.sourceforge.net/project/roboticslab/External/nite/NiTE-Linux-x64-2.2.tar.bz2)

### Installing Dependencies

1. Install Libfreenect (v.1, not v.2): `sudo apt install freenect`
2. Install OpenNI2: `sudo apt install libopenni2-0 libopenni2-dev`

#### Install NiTE:
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

* /NiTE_skeleton_tracker - Python Folder, NiTE skeleton tracking
  * /NiTE_skeleton_tracker/\_\_init\_\_.py
  * /NiTE_skeleton_tracker/\_\_main\_\_.py  - The file that is run by run_tracker.sh
  * /NiTE_skeleton_tracker/composition.py - File containing class with main loops
  * /NiTE_skeleton_tracker/config.json - A config file, if modified breaks the Json decoder.
  * /NiTE_skeleton_tracker/config.py - Reads config? Unsure of exactly what it does outside of being a config
  * /NiTE_skeleton_tracker/tracked_user.py - Classes for assigning data to the active user
  * /NiTE_skeleton_tracker/tracker.py - Converts tracking module (C) data to be used by python
  * /NiTE_skeleton_tracker/draw.py - Pygame code to draw the skeleton tracked
  * /NiTE_skeleton_tracker/openni_nite2_test.py
  * /NiTE_skeleton_tracker/openni_python_binding.py
* /OpenNI2_skeleton_tracker - Python Folder, OpenNI2 skeleton tracking
  * /OpenNI2_skeleton_tracker/Old - Old OpenNI2 files that were left in the NiTE folder
    * /OpenNI2_skeleton_tracker/Old/openni_nite2_test.py
    * /OpenNI2_skeleton_tracker/Old/openni_python_binding.py
  * /OpenNI2_skeleton_tracker/openni_nite2_test.py
* /tracking-module - C Tracker Folder - for NiTE
  * /tracking-module/main.cpp - C source code
  * /tracking-module/Makefile
  * /tracking-module/trackbody - Compiled NiTE code, if it does not exist, run `make` in this directory.
* /README.md - Readme
* /run_tracker.sh - Used to run the NiTE tracker

### File descriptions - long (as needed)


## Todo

### NiTE
- [x] Modify tracking-module code to return full body data instead of just hands
- [x] (Re)write Python parser for new tracking module
- [x] Modify tracker.py
- [x] Modify tracked_user.py
- [x] Write skeleton display - pygame
- [ ] Make skeleton display better
- [ ] Add limb length setting in the endpoint calc
- [ ] Make head drawing a neck and circle, not to limbs
- [ ] Fix the slouch
- [ ] Rewrite Angle code


- [ ] Fix the JSON, delete the physics and dab code
- [ ] Rename trackhands to trackbody, modify trackers to use new name
- [x] Update gitignore to ignore more files

### OpenNI2

- [ ] Kinetic Maze implementation: Add a bar drawn between user hands and display angle
- [ ] Test with maze to see if it will track users after game is done/reset once game is over.
