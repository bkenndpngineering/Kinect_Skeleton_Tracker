/*******************************************************************************
*                                                                              *
*   PrimeSense NiTE 2.0 - Simple Skeleton Sample                               *
*   Copyright (C) 2012 PrimeSense Ltd.                                         *
*                                                                              *
*******************************************************************************/

#include <stdio.h>
#include <nite/NiTE.h>

#define PREFIX "HT! "
#define BODY_DATA "BODY DATA: "
#define SEP_CHAR "|"
#define FRAME_END "FRAME END"
#define COORD_FORMAT "(%5.2f, %5.2f, %5.2f)"

#define REQUIRED_CONFIDENCE 0.25

#define MAX_USERS 10
bool g_visibleUsers[MAX_USERS] = {false};
nite::SkeletonState g_skeletonStates[MAX_USERS] = {nite::SKELETON_NONE};

#define USER_MESSAGE(msg) \
  {printf("# [%08llu] User #%d:\t%s\n",ts, user.getId(),msg);}

void updateUserState(const nite::UserData& user, unsigned long long ts) {
  if (user.isNew())
    USER_MESSAGE("New")
  else if (user.isVisible() && !g_visibleUsers[user.getId()])
    USER_MESSAGE("Visible")
  else if (!user.isVisible() && g_visibleUsers[user.getId()])
    USER_MESSAGE("Out of Scene")
  else if (user.isLost())
    USER_MESSAGE("Lost")

  g_visibleUsers[user.getId()] = user.isVisible();


  if(g_skeletonStates[user.getId()] != user.getSkeleton().getState()) {
    switch(g_skeletonStates[user.getId()] = user.getSkeleton().getState()) {
    case nite::SKELETON_NONE:
      USER_MESSAGE("Stopped tracking.")
      break;
    case nite::SKELETON_CALIBRATING:
      USER_MESSAGE("Calibrating...")
      break;
    case nite::SKELETON_TRACKED:
      USER_MESSAGE("Tracking!")
      break;
    case nite::SKELETON_CALIBRATION_ERROR_NOT_IN_POSE:
    case nite::SKELETON_CALIBRATION_ERROR_HANDS:
    case nite::SKELETON_CALIBRATION_ERROR_LEGS:
    case nite::SKELETON_CALIBRATION_ERROR_HEAD:
    case nite::SKELETON_CALIBRATION_ERROR_TORSO:
      USER_MESSAGE("Calibration Failed... :-|")
      break;
    }
  }
}

int main(int argc, char** argv) {
  nite::UserTracker userTracker;
  nite::Status niteRc;

  setvbuf(stdout, NULL, _IONBF, 0);

  nite::NiTE::initialize();

  niteRc = userTracker.create();
  if (niteRc != nite::STATUS_OK) {
    fprintf(stderr, "Couldn't create user tracker\n");
    return 3;
  }

  nite::UserTrackerFrameRef userTrackerFrame;
  while (1) {
    niteRc = userTracker.readFrame(&userTrackerFrame);
    if (niteRc != nite::STATUS_OK) {
      fprintf(stderr, "Get next frame failed\n");
      continue;
    }

    const nite::Array<nite::UserData>& users = userTrackerFrame.getUsers();
    for (int i = 0; i < users.getSize() && i < MAX_USERS; ++i) {
      const nite::UserData& user = users[i];
      updateUserState(user,userTrackerFrame.getTimestamp());

      if (user.isNew()) {
        userTracker.startSkeletonTracking(user.getId());
      }
      else if (user.getSkeleton().getState() == nite::SKELETON_TRACKED) {
        // These are flipped intentionally. NiTE defines "left hand" as the hand on the left
        // _from the camera's perspective_, which is the opposite of what we want.

        const nite::SkeletonJoint& head      = user.getSkeleton().getJoint(nite::JOINT_HEAD);
        const nite::SkeletonJoint& neck      = user.getSkeleton().getJoint(nite::JOINT_NECK);
        const nite::SkeletonJoint& torso     = user.getSkeleton().getJoint(nite::JOINT_TORSO);

        const nite::SkeletonJoint& rshoulder = user.getSkeleton().getJoint(nite::JOINT_LEFT_SHOULDER);
        const nite::SkeletonJoint& relbow    = user.getSkeleton().getJoint(nite::JOINT_LEFT_ELBOW);
        const nite::SkeletonJoint& rhand     = user.getSkeleton().getJoint(nite::JOINT_LEFT_HAND);

        const nite::SkeletonJoint& lshoulder = user.getSkeleton().getJoint(nite::JOINT_RIGHT_SHOULDER);
        const nite::SkeletonJoint& lelbow    = user.getSkeleton().getJoint(nite::JOINT_RIGHT_ELBOW);
        const nite::SkeletonJoint& lhand     = user.getSkeleton().getJoint(nite::JOINT_RIGHT_HAND);

        const nite::SkeletonJoint& rhip      = user.getSkeleton().getJoint(nite::JOINT_LEFT_HIP);
        const nite::SkeletonJoint& rknee     = user.getSkeleton().getJoint(nite::JOINT_LEFT_KNEE);
        const nite::SkeletonJoint& rfoot     = user.getSkeleton().getJoint(nite::JOINT_LEFT_FOOT);

        const nite::SkeletonJoint& lhip      = user.getSkeleton().getJoint(nite::JOINT_RIGHT_HIP);
        const nite::SkeletonJoint& lknee     = user.getSkeleton().getJoint(nite::JOINT_RIGHT_KNEE);
        const nite::SkeletonJoint& lfoot     = user.getSkeleton().getJoint(nite::JOINT_RIGHT_FOOT);


        if (head.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            neck.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            torso.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            rshoulder.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            relbow.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            rhand.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            lshoulder.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            lelbow.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            lhand.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            rhip.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            rknee.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            rfoot.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            lhip.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            lknee.getPositionConfidence() > REQUIRED_CONFIDENCE &&
            lfoot.getPositionConfidence() > REQUIRED_CONFIDENCE) {
          printf(PREFIX BODY_DATA "%d"
                 SEP_CHAR COORD_FORMAT // head
                 SEP_CHAR COORD_FORMAT // neck
                 SEP_CHAR COORD_FORMAT // torso
                 SEP_CHAR COORD_FORMAT // lshoulder
                 SEP_CHAR COORD_FORMAT // lelbow
                 SEP_CHAR COORD_FORMAT // lhand
                 SEP_CHAR COORD_FORMAT // rshoulder
                 SEP_CHAR COORD_FORMAT // relbow
                 SEP_CHAR COORD_FORMAT // rhand
                 SEP_CHAR COORD_FORMAT // lhip
                 SEP_CHAR COORD_FORMAT // lknee
                 SEP_CHAR COORD_FORMAT // lfoot
                 SEP_CHAR COORD_FORMAT // rhip
                 SEP_CHAR COORD_FORMAT // rknee
                 SEP_CHAR COORD_FORMAT // rfoot

                 "\n",
                 user.getId(),
                 head.getPosition().x,     head.getPosition().y,     head.getPosition().z,
                 neck.getPosition().x,     neck.getPosition().y,     neck.getPosition().z,
                 torso.getPosition().x,    torso.getPosition().y,    torso.getPosition().z,
                 lshoulder.getPosition().x,lshoulder.getPosition().y,lshoulder.getPosition().z,
                 lelbow.getPosition().x,   lelbow.getPosition().y,   lelbow.getPosition().z,
                 lhand.getPosition().x,    lhand.getPosition().y,    lhand.getPosition().z,
                 rshoulder.getPosition().x,rshoulder.getPosition().y,rshoulder.getPosition().z,
                 relbow.getPosition().x,   relbow.getPosition().y,   relbow.getPosition().z,
                 rhand.getPosition().x,    rhand.getPosition().y,    rhand.getPosition().z,
                 lhip.getPosition().x,     lhip.getPosition().y,     lhip.getPosition().z,
                 lknee.getPosition().x,    lknee.getPosition().y,    lknee.getPosition().z,
                 lfoot.getPosition().x,    lfoot.getPosition().y,    lfoot.getPosition().z,
                 rhip.getPosition().x,     rhip.getPosition().y,     rhip.getPosition().z,
                 rknee.getPosition().x,    rknee.getPosition().y,    rknee.getPosition().z,
                 rfoot.getPosition().x,    rfoot.getPosition().y,    rfoot.getPosition().z);
        }
      }
    }
    printf("HT! FRAME END\n");
  }

  nite::NiTE::shutdown();

}
