from .tracker import Tracker
from .config import global_config as c
from . import logger
import os

from . import Skeleton
sk = Skeleton()


l = logger.getChild("composition")

class Kinect:
    def __init__(self, tracker_path, tracker_wd):
        self.tracker_path = tracker_path
        self.tracker_wd = tracker_wd
        self.kmm = None
        self.tracker = None

    def run(self):
        self.tracker = Tracker(self.tracker_path, self.tracker_wd)
        l.info("Starting main loop")
        for user in self.tracker.stream():
            if (user is not None):
                head, neck, torso, lshoulder, lelbow, lhand, rshoulder, relbow, rhand, lhip, lknee, lfoot, rhip, rknee, rfoot = user

                sk.updateSk(head, neck, torso, lshoulder, lelbow, lhand, rshoulder, relbow, rhand, lhip, lknee, lfoot, rhip, rknee, rfoot)
                sk.drawSkel()
