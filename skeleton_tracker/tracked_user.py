import numpy as np
from .linalg_helpers import *


class TrackedUser(object):
    def __init__(self, user_id,
                 head, neck, torso,
                 left_shoulder, left_elbow, left_hand,
                 right_shoulder, right_elbow, right_hand,
                 left_hip, left_knee, left_foot,
                 right_hip, right_knee, right_foot):
        self.user_id = user_id


        self.head = head
        self.neck = neck
        self.torso = torso

        self.left_shoulder = left_shoulder
        self.left_elbow = left_elbow
        self.left_hand = left_hand

        self.right_shoulder = right_shoulder
        self.right_elbow = right_elbow
        self.right_hand = right_hand

        self.left_hip = left_hip
        self.left_knee = left_knee
        self.left_foot = left_foot

        self.right_hip = right_hip
        self.right_knee = right_knee
        self.right_foot = right_foot


    @property
    def left_forearm(self):
        return self.left_hand - self.left_elbow

    @property
    def right_forearm(self):
        return self.right_hand - self.right_elbow

    @property
    def left_upper_arm(self):
        return self.left_elbow - self.left_shoulder

    @property
    def right_upper_arm(self):
        return self.right_elbow - self.right_shoulder

    @property
    def left_arm(self):
        return self.left_hand - self.left_shoulder

    @property
    def right_arm(self):
        return self.right_hand - self.right_shoulder

    def returnUser(self):
        return self.head, self.neck, self.torso, self.left_shoulder, self.left_elbow, self.left_hand, self.right_shoulder, self.right_elbow, self.right_hand, self.left_hip, self.left_knee, self.left_foot, self.right_hip, self.right_knee, self.right_foot


class WorldTrackedUser(TrackedUser):
    def __init__(self, user_id,
                 head, neck, torso,
                 left_shoulder, left_elbow, left_hand,
                 right_shoulder, right_elbow, right_hand,
                 left_hip, left_knee, left_foot,
                 right_hip, right_knee, right_foot):
        super(WorldTrackedUser, self).__init__(user_id,
                                               head, neck, torso,
                                               left_shoulder, left_elbow, left_hand,
                                               right_shoulder, right_elbow, right_hand,
                                               left_hip, left_knee, left_foot,
                                               right_hip, right_knee, right_foot)
        self._relative_user = None

    def get_forward_plane(self):
        # order of cross is important: ensure that resulting cross product points forward
        return normalize(np.cross(self.get_up_plane(),
                                  self.get_side_plane()))

    def get_up_plane(self):
        # create something that goes vaguely upwards
        vaguely_up = self.right_shoulder - self.torso
        return normalize(project_onto_plane(vaguely_up, self.get_side_plane()))

    def get_side_plane(self):
        return normalize(self.right_shoulder - self.left_shoulder)

    @property
    def relative_user(self):
        if self._relative_user is not None:
            return self._relative_user

        t_matrix = np.linalg.inv((self.get_side_plane(),
                                  self.get_up_plane(),
                                  self.get_forward_plane()))

        h = np.matmul(t_matrix, self.head - self.torso)
        n = np.matmul(t_matrix, self.neck - self.torso)
        torso = np.matmul(t_matrix, self.torso - self.torso)

        ls = np.matmul(t_matrix, self.left_shoulder - self.torso)
        le = np.matmul(t_matrix, self.left_elbow - self.torso)
        lh = np.matmul(t_matrix, self.left_hand - self.torso)

        rs = np.matmul(t_matrix, self.right_shoulder - self.torso)
        re = np.matmul(t_matrix, self.right_elbow - self.torso)
        rh = np.matmul(t_matrix, self.right_hand - self.torso)

        lhip = np.matmul(t_matrix, self.left_hip - self.torso)
        lk = np.matmul(t_matrix, self.left_knee - self.torso)
        lf = np.matmul(t_matrix, self.left_foot - self.torso)

        rhip = np.matmul(t_matrix, self.right_hip - self.torso)
        rk = np.matmul(t_matrix, self.right_knee - self.torso)
        rf = np.matmul(t_matrix, self.right_foot - self.torso)



        self._relative_user = RelativeTrackedUser(self.user_id,
                                                  h, n, torso,
                                                  ls, le, lh,
                                                  rs, re, rh,
                                                  lhip, lk, lf,
                                                  rhip, rk, rf,
                                                  self)
        return self._relative_user

class RelativeTrackedUser(TrackedUser):
    def __init__(self, user_id,
                 head, neck, torso,
                 left_shoulder, left_elbow, left_hand,
                 right_shoulder, right_elbow, right_hand,
                 left_hip, left_knee, left_foot,
                 right_hip, right_knee, right_foot,
                 world_user):
        super(RelativeTrackedUser, self).__init__(user_id,
                                                  head, neck, torso,
                                                  left_shoulder, left_elbow, left_hand,
                                                  right_shoulder, right_elbow, right_hand,
                                                  left_hip, left_knee, left_foot,
                                                  right_hip, right_knee, right_foot)
        self.world_user = world_user
