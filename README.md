# Kinect-Skeleton-Tracker
Module for using Kinect for general purpose skeleton tracking


## Dependencies
[Libfreenect](https://github.com/OpenKinect/libfreenect),
[Openni2](https://github.com/occipital/openni2),
[NiTE2](http://jaist.dl.sourceforge.net/project/roboticslab/External/nite/NiTE-Linux-x64-2.2.tar.bz2)

## Organization
### Plans
Using libfreenect, the kinect camera, send the image the kinect sees to a Neural Net for skeleton tracking.



## Todo
- [x] Modify tracking-module code to return full body data instead of just hands
- [ ] (Re)write Python parser for new tracking module
- [ ] Write skeleton display - pygame
