'''
Kinetic Maze display:
controls everything that's displayed in the window.
'''

        #The plan is to draw each line between joints as the same length, but change the angle of display and a fixed point. first fixed point will be the torso, at 0,0 or something


import pygame
import math
import os
from pygame.locals import *
import time

#Make screen
SIZE = 800, 800
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Kinetic Maze V2")
FPSCLOCK = pygame.time.Clock()
done = False
screen.fill((0, 0, 0))


class Skeleton:
            #3 numbers in each joint.
            #1st is leftright
            #2nd is updown, higher is higher
            #3rd is depth, dist from camera

    def __init__(self):
        pass

    def updateSk(self, h, n, t, ls, le, lh, rs, re, rh, lhip, lk, lf, rhip, rk, rf):
        self.head = h
        self.neck = n
        self.torso = t

        self.left_shoulder = ls
        self.left_elbow = le
        self.left_hand = lh

        self.right_shoulder = rs
        self.right_elbow = re
        self.right_hand = rh

        self.left_hip = lhip
        self.left_knee = lk
        self.left_foot = lf

        self.right_hip = rhip
        self.right_knee = rk
        self.right_foot = rf

    def jointAngle(self,one,two):
        delta = two - one
        return math.atan2(delta[1], delta[0]) * 45 #Needs to be tuned a bit

    def angleLine(self,startx,starty, angle): #draw a line at an angle with fixed start point
        end = startx + 5*math.cos(angle),starty + 5*math.sin(angle) #location of the nonfixed end
        pygame.draw.line(screen, Color("green"), (startx,starty), end, 5)
        pygame.display.update()

    def returnLineEnd(self,tuple,angle, length):
        startx, starty = tuple
        return (startx - length*math.cos(math.radians(angle)),starty - length*math.sin(math.radians(angle)))
        #image flipped?


    def drawSkel(self):

        linCover = pygame.surface.Surface((720,600)).convert()
        linCover.fill((0, 0, 0))
        screen.blit(linCover, (0,100))

        torso = (400,400)

        lshoulderEP = self.returnLineEnd(torso, self.jointAngle(self.torso,self.left_shoulder), 75) #EP for end point, to reduce variable confusion
        rshoulderEP = self.returnLineEnd(torso, self.jointAngle(self.torso,self.right_shoulder), 75)
        lhipEP = self.returnLineEnd(torso, self.jointAngle(self.torso,self.left_hip), 75)
        rhipEP = self.returnLineEnd(torso, self.jointAngle(self.torso,self.right_hip), 75)

        #Torso/shoulders/hips, in blue
        pygame.draw.lines(screen, Color("blue"), True, [torso, lshoulderEP, rshoulderEP])
        pygame.draw.lines(screen, Color("blue"), True, [torso, lhipEP, rhipEP])

        #head + neck, in white. MAKE THIS DRAW A CIRCLE ON THE TORSO TRIANGLE
        #neckEP = self.returnLineEnd(torso, self.jointAngle(self.torso,self.neck))
        #headEP = self.returnLineEnd(torso, self.jointAngle(self.neck,self.head))
        #pygame.draw.lines(screen, Color("white"), False, [torso, neckEP, headEP])

        #arms, in green and red for left and right
        lelbowEP = self.returnLineEnd(lshoulderEP, self.jointAngle(self.left_shoulder,self.left_elbow), 75)
        lhandEP = self.returnLineEnd(lelbowEP, self.jointAngle(self.left_elbow,self.left_hand), 75)
        leftArmPoints = [lshoulderEP, lelbowEP, lhandEP]

        relbowEP = self.returnLineEnd(rshoulderEP, self.jointAngle(self.right_shoulder,self.right_elbow), 75)
        rhandEP = self.returnLineEnd(relbowEP, self.jointAngle(self.right_elbow,self.right_hand), 75)
        rightArmPoints = [rshoulderEP, relbowEP, rhandEP]

        #legs, in gold and pink for left and right
        lkneeEP = self.returnLineEnd(lhipEP, self.jointAngle(self.left_hip,self.left_knee), 75)
        lfootEP = self.returnLineEnd(lkneeEP, self.jointAngle(self.left_knee,self.left_foot), 75)
        leftLegPoints = [lhipEP, lkneeEP, lfootEP]

        rkneeEP = self.returnLineEnd(rhipEP, self.jointAngle(self.right_hip,self.right_knee), 75)
        rfootEP = self.returnLineEnd(rkneeEP, self.jointAngle(self.right_knee,self.right_foot), 75)
        rightLegPoints = [rhipEP, rkneeEP, rfootEP]



        pygame.draw.lines(screen, Color("green"), False, leftArmPoints)
        pygame.draw.lines(screen, Color("red"), False, rightArmPoints) #right arm is very glitchy and inaccurate
        pygame.draw.lines(screen, Color("gold"), False, leftLegPoints)
        pygame.draw.lines(screen, Color("deeppink"), False, rightLegPoints)

        pygame.display.update()
