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
        return math.atan2(delta[1], delta[0])

    def angleLine(self,startx,starty, angle): #draw a line at an angle with fixed start point
        end = startx + 5*math.cos(angle),starty + 5*math.sin(angle) #location of the nonfixed end
        pygame.draw.line(screen, Color("green"), (startx,starty), end, 5)
        pygame.display.update()

    def returnLineEnd(self,tuple,angle):
        startx, starty = tuple
        return (startx - 75*math.cos(math.radians(angle)),starty - 75*math.sin(math.radians(angle)))
        #image flipped?


    def drawSkel(self): #untested as of 12/2/2019

        linCover = pygame.surface.Surface((720,600)).convert()
        linCover.fill((0, 0, 0))
        screen.blit(linCover, (0,100))

        #pygame.draw.line(screen, Color("yellow"), (400,300), (400,500), 1)


        torso = (400,400)
        shoulder = self.returnLeftEnd(torso, self.jointAngle(self.t,self.ls)  * 45)
        elbow = self.returnLeftEnd(shoulder, self.jointAngle(self.ls,self.le)  * 45)
        hand = self.returnLeftEnd(elbow, self.jointAngle(self.le,self.lh)  * 45)
        leftPoints = [shoulder, elbow, hand]

        pygame.draw.lines(screen, Color("green"), False, leftPoints)
        # left arm works-ish, shoulder line goes straight down but else tracks well.


        rshoulder = self.returnRightEnd(torso, self.jointAngle(self.t,self.rs) * 45)
        relbow = self.returnRightEnd(rshoulder, self.jointAngle(self.rs,self.re)  * 45)
        rhand = self.returnRightEnd(relbow, self.jointAngle(self.re,self.rh)  * 45)
        rightPoints = [rshoulder, relbow, rhand]

        pygame.draw.lines(screen, Color("red"), False, rightPoints)

        pygame.draw.lines(screen, Color("blue"), True, [torso, shoulder, rshoulder])


        pygame.display.update()
