# documentation at https://github.com/severin-lemaignan/openni-python
# can be installed through PyPi with pip3 install openni

# coordinates can be obtained from draw_limb function

import sys
import argparse
from openni import openni2, nite2, utils
import numpy as np
import cv2
from threading import Thread
import math

GRAY_COLOR = (64, 64, 64)
CAPTURE_SIZE_KINECT = (512, 424)
CAPTURE_SIZE_OTHERS = (640, 480)


############ BK junk ###############
# dictionary updated as the joints are drawn
coordinate_dict = {"HEAD": (None, None),
                    "NECK": (None, None),
                    "LEFT_SHOULDER": (None, None),
                    "TORSO": (None, None),
                    "RIGHT_SHOULDER": (None, None),
                    "LEFT_HAND": (None, None),
                    "LEFT_ELBOW": (None, None),
                    "RIGHT_HAND": (None, None),
                    "RIGHT_ELBOW": (None, None),
                    "LEFT_HIP": (None, None),
                    "RIGHT_HIP": (None, None),
                    "LEFT_FOOT": (None, None),
                    "LEFT_KNEE": (None, None),
                    "RIGHT_FOOT": (None, None),
                    "RIGHT_KNEE": (None, None)}

class Tracker:

    def __init__(self):
        pass

    def capture_coordinates(self, ut, j):
        (x, y) = ut.convert_joint_coordinates_to_depth(j.position.x, j.position.y, j.position.z)

        jointName = str(j.jointType)
        # EX: NiteJointType.NITE_JOINT_LEFT_HIP
        jointNameList = jointName.split("_")
        jointNameList.pop(0)
        jointNameList.pop(0)
        if len(jointNameList) == 2:
            key = jointNameList[0]+"_"+jointNameList[1]
        elif len(jointNameList) == 1:
            key = jointNameList[0]

        coordinate_dict[key] = (x, y)
    def calculate_angle(self, j1_name, j2_name):
        # takes string, keys to the coordinate_dict
        # returns degrees, angle relative to x axis
        j1_coordinates = coordinate_dict[str(j1_name)]
        j2_coordinates = coordinate_dict[str(j2_name)]

        if (j1_coordinates[0] == None) or (j1_coordinates[1] == None):
            #print("first joint has no coordinates")
            return
        elif (j2_coordinates[0] == None) or (j2_coordinates[1] == None):
            #print("first joint has no coordinates")
            return

        # top minus bottom, y axis in inverted (0,0) is top left i think
        o = abs(j1_coordinates[1]-j2_coordinates[1]) # difference in y coordinates
        a = abs(j1_coordinates[0]-j2_coordinates[0]) # difference in x coordinates
        theta = math.atan(o/a)

        return math.degrees(theta)


    def parse_arg(self):
        parser = argparse.ArgumentParser(description='Test OpenNI2 and NiTE2.')
        parser.add_argument('-w', '--window_width', type=int, default=1024,
                            help='Specify the window width.')
        return parser.parse_args()
    def draw_limb(self, img, ut, j1, j2, col):
        (x1, y1) = ut.convert_joint_coordinates_to_depth(j1.position.x, j1.position.y, j1.position.z)
        (x2, y2) = ut.convert_joint_coordinates_to_depth(j2.position.x, j2.position.y, j2.position.z)

        # example use of coordinates
        #if str(j1.jointType) == "NiteJointType.NITE_JOINT_LEFT_HAND":
        #    print("x1, y1:", x1, y1)

        if (0.4 < j1.positionConfidence and 0.4 < j2.positionConfidence):
            c = GRAY_COLOR if (j1.positionConfidence < 1.0 or j2.positionConfidence < 1.0) else col
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), c, 1)

            c = GRAY_COLOR if (j1.positionConfidence < 1.0) else col
            cv2.circle(img, (int(x1), int(y1)), 2, c, -1)

            c = GRAY_COLOR if (j2.positionConfidence < 1.0) else col
            cv2.circle(img, (int(x2), int(y2)), 2, c, -1)
    def draw_skeleton(self, img, ut, user, col):
        for idx1, idx2 in [(nite2.JointType.NITE_JOINT_HEAD, nite2.JointType.NITE_JOINT_NECK),
                           # upper body
                           (nite2.JointType.NITE_JOINT_NECK, nite2.JointType.NITE_JOINT_LEFT_SHOULDER),
                           (nite2.JointType.NITE_JOINT_LEFT_SHOULDER, nite2.JointType.NITE_JOINT_TORSO),
                           (nite2.JointType.NITE_JOINT_TORSO, nite2.JointType.NITE_JOINT_RIGHT_SHOULDER),
                           (nite2.JointType.NITE_JOINT_RIGHT_SHOULDER, nite2.JointType.NITE_JOINT_NECK),
                           # left hand
                           (nite2.JointType.NITE_JOINT_LEFT_HAND, nite2.JointType.NITE_JOINT_LEFT_ELBOW),
                           (nite2.JointType.NITE_JOINT_LEFT_ELBOW, nite2.JointType.NITE_JOINT_LEFT_SHOULDER),
                           # right hand
                           (nite2.JointType.NITE_JOINT_RIGHT_HAND, nite2.JointType.NITE_JOINT_RIGHT_ELBOW),
                           (nite2.JointType.NITE_JOINT_RIGHT_ELBOW, nite2.JointType.NITE_JOINT_RIGHT_SHOULDER),
                           # lower body
                           (nite2.JointType.NITE_JOINT_TORSO, nite2.JointType.NITE_JOINT_LEFT_HIP),
                           (nite2.JointType.NITE_JOINT_LEFT_HIP, nite2.JointType.NITE_JOINT_RIGHT_HIP),
                           (nite2.JointType.NITE_JOINT_RIGHT_HIP, nite2.JointType.NITE_JOINT_TORSO),
                           # left leg
                           (nite2.JointType.NITE_JOINT_LEFT_FOOT, nite2.JointType.NITE_JOINT_LEFT_KNEE),
                           (nite2.JointType.NITE_JOINT_LEFT_KNEE, nite2.JointType.NITE_JOINT_LEFT_HIP),
                           # right leg
                           (nite2.JointType.NITE_JOINT_RIGHT_FOOT, nite2.JointType.NITE_JOINT_RIGHT_KNEE),
                           (nite2.JointType.NITE_JOINT_RIGHT_KNEE, nite2.JointType.NITE_JOINT_RIGHT_HIP)]:
            self.draw_limb(img, ut, user.skeleton.joints[idx1], user.skeleton.joints[idx2], col)
            self.capture_coordinates(ut, user.skeleton.joints[idx1])
            self.capture_coordinates(ut, user.skeleton.joints[idx2])


    # -------------------------------------------------------------
    # main program from here
    # -------------------------------------------------------------

    def init_capture_device(self):

        openni2.initialize()
        nite2.initialize("/usr/lib/")
        # NiTE2 folder has to be in the same directory as this script!
        return openni2.Device.open_any()
    def close_capture_device(self):
        nite2.unload()
        openni2.unload()
    def capture_skeleton(self):
        args = self.parse_arg()
        dev = self.init_capture_device()

        dev_name = dev.get_device_info().name.decode('UTF-8')
        print("Device Name: {}".format(dev_name))
        use_kinect = False
        if dev_name == 'Kinect':
            use_kinect = True
            print('using Kinect.')

        try:
            user_tracker = nite2.UserTracker(dev)
        except utils.NiteError:
            print("Unable to start the NiTE human tracker. Check "
                  "the error messages in the console. Model data "
                  "(s.dat, h.dat...) might be inaccessible.")
            sys.exit(-1)

        (img_w, img_h) = CAPTURE_SIZE_KINECT if use_kinect else CAPTURE_SIZE_OTHERS
        win_w = args.window_width
        win_h = int(img_h * win_w / img_w)

        while True:
            ut_frame = user_tracker.read_frame()

            depth_frame = ut_frame.get_depth_frame()
            depth_frame_data = depth_frame.get_buffer_as_uint16()
            img = np.ndarray((depth_frame.height, depth_frame.width), dtype=np.uint16,
                             buffer=depth_frame_data).astype(np.float32)
            if use_kinect:
                img = img[0:img_h, 0:img_w]

            (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(img)
            if (min_val < max_val):
                img = (img - min_val) / (max_val - min_val)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

            if ut_frame.users:
                for user in ut_frame.users:
                    if user.is_new():
                        print("new human id:{} detected.".format(user.id))
                        user_tracker.start_skeleton_tracking(user.id)
                    elif (user.state == nite2.UserState.NITE_USER_STATE_VISIBLE and
                          user.skeleton.state == nite2.SkeletonState.NITE_SKELETON_TRACKED):
                        self.draw_skeleton(img, user_tracker, user, (255, 0, 0))

            cv2.imshow("Depth", cv2.resize(img, (win_w, win_h)))
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break

        self.close_capture_device()
        cv2.destroyAllWindows()  # close OpenCV window

    def stream(self):
        skeleton_tracker_thread = Thread(target=self.capture_skeleton, args=())
        skeleton_tracker_thread.start()

        while True:
            yield self.calculate_angle("LEFT_HAND", "RIGHT_HAND")

        #capture_skeleton()
# documentation at https://github.com/severin-lemaignan/openni-python
# can be installed through PyPi with pip3 install openni

# coordinates can be obtained from draw_limb function

import sys
import argparse
from openni import openni2, nite2, utils
import numpy as np
import cv2
from threading import Thread
import math

GRAY_COLOR = (64, 64, 64)
CAPTURE_SIZE_KINECT = (512, 424)
CAPTURE_SIZE_OTHERS = (640, 480)


############ BK junk ###############
# dictionary updated as the joints are drawn
coordinate_dict = {"HEAD": (None, None),
                    "NECK": (None, None),
                    "LEFT_SHOULDER": (None, None),
                    "TORSO": (None, None),
                    "RIGHT_SHOULDER": (None, None),
                    "LEFT_HAND": (None, None),
                    "LEFT_ELBOW": (None, None),
                    "RIGHT_HAND": (None, None),
                    "RIGHT_ELBOW": (None, None),
                    "LEFT_HIP": (None, None),
                    "RIGHT_HIP": (None, None),
                    "LEFT_FOOT": (None, None),
                    "LEFT_KNEE": (None, None),
                    "RIGHT_FOOT": (None, None),
                    "RIGHT_KNEE": (None, None)}

class Tracker:

    def __init__(self):
        pass

    def capture_coordinates(self, ut, j):
        (x, y) = ut.convert_joint_coordinates_to_depth(j.position.x, j.position.y, j.position.z)

        jointName = str(j.jointType)
        # EX: NiteJointType.NITE_JOINT_LEFT_HIP
        jointNameList = jointName.split("_")
        jointNameList.pop(0)
        jointNameList.pop(0)
        if len(jointNameList) == 2:
            key = jointNameList[0]+"_"+jointNameList[1]
        elif len(jointNameList) == 1:
            key = jointNameList[0]

        coordinate_dict[key] = (x, y)
    def calculate_angle(self, j1_name, j2_name):
        # takes string, keys to the coordinate_dict
        # returns degrees, angle relative to x axis
        j1_coordinates = coordinate_dict[str(j1_name)]
        j2_coordinates = coordinate_dict[str(j2_name)]

        if (j1_coordinates[0] == None) or (j1_coordinates[1] == None):
            #print("first joint has no coordinates")
            return
        elif (j2_coordinates[0] == None) or (j2_coordinates[1] == None):
            #print("first joint has no coordinates")
            return

        # top minus bottom, y axis in inverted (0,0) is top left i think
        o = abs(j1_coordinates[1]-j2_coordinates[1]) # difference in y coordinates
        a = abs(j1_coordinates[0]-j2_coordinates[0]) # difference in x coordinates
        theta = math.atan(o/a)

        return math.degrees(theta)


    def parse_arg(self):
        parser = argparse.ArgumentParser(description='Test OpenNI2 and NiTE2.')
        parser.add_argument('-w', '--window_width', type=int, default=1024,
                            help='Specify the window width.')
        return parser.parse_args()
    def draw_limb(self, img, ut, j1, j2, col):
        (x1, y1) = ut.convert_joint_coordinates_to_depth(j1.position.x, j1.position.y, j1.position.z)
        (x2, y2) = ut.convert_joint_coordinates_to_depth(j2.position.x, j2.position.y, j2.position.z)

        # example use of coordinates
        #if str(j1.jointType) == "NiteJointType.NITE_JOINT_LEFT_HAND":
        #    print("x1, y1:", x1, y1)

        if (0.4 < j1.positionConfidence and 0.4 < j2.positionConfidence):
            c = GRAY_COLOR if (j1.positionConfidence < 1.0 or j2.positionConfidence < 1.0) else col
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), c, 1)

            c = GRAY_COLOR if (j1.positionConfidence < 1.0) else col
            cv2.circle(img, (int(x1), int(y1)), 2, c, -1)

            c = GRAY_COLOR if (j2.positionConfidence < 1.0) else col
            cv2.circle(img, (int(x2), int(y2)), 2, c, -1)
    def draw_skeleton(self, img, ut, user, col):
        for idx1, idx2 in [(nite2.JointType.NITE_JOINT_HEAD, nite2.JointType.NITE_JOINT_NECK),
                           # upper body
                           (nite2.JointType.NITE_JOINT_NECK, nite2.JointType.NITE_JOINT_LEFT_SHOULDER),
                           (nite2.JointType.NITE_JOINT_LEFT_SHOULDER, nite2.JointType.NITE_JOINT_TORSO),
                           (nite2.JointType.NITE_JOINT_TORSO, nite2.JointType.NITE_JOINT_RIGHT_SHOULDER),
                           (nite2.JointType.NITE_JOINT_RIGHT_SHOULDER, nite2.JointType.NITE_JOINT_NECK),
                           # left hand
                           (nite2.JointType.NITE_JOINT_LEFT_HAND, nite2.JointType.NITE_JOINT_LEFT_ELBOW),
                           (nite2.JointType.NITE_JOINT_LEFT_ELBOW, nite2.JointType.NITE_JOINT_LEFT_SHOULDER),
                           # right hand
                           (nite2.JointType.NITE_JOINT_RIGHT_HAND, nite2.JointType.NITE_JOINT_RIGHT_ELBOW),
                           (nite2.JointType.NITE_JOINT_RIGHT_ELBOW, nite2.JointType.NITE_JOINT_RIGHT_SHOULDER),
                           # lower body
                           (nite2.JointType.NITE_JOINT_TORSO, nite2.JointType.NITE_JOINT_LEFT_HIP),
                           (nite2.JointType.NITE_JOINT_LEFT_HIP, nite2.JointType.NITE_JOINT_RIGHT_HIP),
                           (nite2.JointType.NITE_JOINT_RIGHT_HIP, nite2.JointType.NITE_JOINT_TORSO),
                           # left leg
                           (nite2.JointType.NITE_JOINT_LEFT_FOOT, nite2.JointType.NITE_JOINT_LEFT_KNEE),
                           (nite2.JointType.NITE_JOINT_LEFT_KNEE, nite2.JointType.NITE_JOINT_LEFT_HIP),
                           # right leg
                           (nite2.JointType.NITE_JOINT_RIGHT_FOOT, nite2.JointType.NITE_JOINT_RIGHT_KNEE),
                           (nite2.JointType.NITE_JOINT_RIGHT_KNEE, nite2.JointType.NITE_JOINT_RIGHT_HIP)]:
            self.draw_limb(img, ut, user.skeleton.joints[idx1], user.skeleton.joints[idx2], col)
            self.capture_coordinates(ut, user.skeleton.joints[idx1])
            self.capture_coordinates(ut, user.skeleton.joints[idx2])


    # -------------------------------------------------------------
    # main program from here
    # -------------------------------------------------------------

    def init_capture_device(self):

        openni2.initialize()
        nite2.initialize("/usr/lib/")
        # NiTE2 folder has to be in the same directory as this script!
        return openni2.Device.open_any()
    def close_capture_device(self):
        nite2.unload()
        openni2.unload()
    def capture_skeleton(self):
        args = self.parse_arg()
        dev = self.init_capture_device()

        dev_name = dev.get_device_info().name.decode('UTF-8')
        print("Device Name: {}".format(dev_name))
        use_kinect = False
        if dev_name == 'Kinect':
            use_kinect = True
            print('using Kinect.')

        try:
            user_tracker = nite2.UserTracker(dev)
        except utils.NiteError:
            print("Unable to start the NiTE human tracker. Check "
                  "the error messages in the console. Model data "
                  "(s.dat, h.dat...) might be inaccessible.")
            sys.exit(-1)

        (img_w, img_h) = CAPTURE_SIZE_KINECT if use_kinect else CAPTURE_SIZE_OTHERS
        win_w = args.window_width
        win_h = int(img_h * win_w / img_w)

        while True:
            ut_frame = user_tracker.read_frame()

            depth_frame = ut_frame.get_depth_frame()
            depth_frame_data = depth_frame.get_buffer_as_uint16()
            img = np.ndarray((depth_frame.height, depth_frame.width), dtype=np.uint16,
                             buffer=depth_frame_data).astype(np.float32)
            if use_kinect:
                img = img[0:img_h, 0:img_w]

            (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(img)
            if (min_val < max_val):
                img = (img - min_val) / (max_val - min_val)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

            if ut_frame.users:
                for user in ut_frame.users:
                    if user.is_new():
                        print("new human id:{} detected.".format(user.id))
                        user_tracker.start_skeleton_tracking(user.id)
                    elif (user.state == nite2.UserState.NITE_USER_STATE_VISIBLE and
                          user.skeleton.state == nite2.SkeletonState.NITE_SKELETON_TRACKED):
                        self.draw_skeleton(img, user_tracker, user, (255, 0, 0))

            cv2.imshow("Depth", cv2.resize(img, (win_w, win_h)))
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break

        self.close_capture_device()
        cv2.destroyAllWindows()  # close OpenCV window

    def stream(self):
        skeleton_tracker_thread = Thread(target=self.capture_skeleton, args=())
        skeleton_tracker_thread.start()

        while True:
            yield self.calculate_angle("LEFT_HAND", "RIGHT_HAND")

        #capture_skeleton()
