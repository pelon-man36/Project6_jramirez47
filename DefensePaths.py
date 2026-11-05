import math, random
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import SpaceJamClasses as spaceJamClasses

def Cloud(radius = 1):
    x = 2 * random.random() - 1
    y = 2 * random.random() - 1
    z = 2 * random.random() - 1
    unitVec = Vec3(x, y, z)
    unitVec.normalize()
    return unitVec * radius

def BaseballSeams(step, numSeams, B, F = 1):
    time = step / float(numSeams) * 2 * math.pi

    F4 = 0

    R = 1

    xxx = math.cos(time) - B * math.cos(3 * time)
    yyy = math.sin(time) + B * math.sin(3 * time)
    zzz = F * math.cos(2 * time) + F4 * math.cos(4 * time)

    rrr = math.sqrt(xxx ** 2 + yyy ** 2 + zzz ** 2)

    x = R * xxx / rrr
    y = R * yyy / rrr
    z = R * zzz / rrr

    return Vec3(x, y, z)

def createCircleX(self, objectModel="./Assets/Spaceships/DroneDefender/DroneDefender.obj"):
    x = 0
    for i in range(25):
        theta = x
        self.placeholder2 = spaceJamClasses.XYZDrone(self.loader, objectModel, self.render, "XDrone", Vec3(200.0 * math.cos(theta),
            200.0 * math.sin(theta), 0.0 * math.tan(theta)), (1, 0, 0, 1))
        x = x + 0.5

def createCircleZ(self, objectModel="./Assets/Spaceships/DroneDefender/DroneDefender.obj"):
    x = 0
    for i in range(25):
        theta = x
        self.placeholder2 = spaceJamClasses.XYZDrone(self.loader, objectModel, self.render, "ZDrone", Vec3(200.0 * math.sin(theta),
            0.0 * math.tan(theta), 200.0 * math.cos(theta)), (0, 1, 0, 1))
        x = x + 0.5

def createCircleY(self, objectModel="./Assets/Spaceships/DroneDefender/DroneDefender.obj"):
    x = 0
    for i in range(25):
        theta = x
        self.placeholder2 = spaceJamClasses.XYZDrone(self.loader, objectModel, self.render, "YDrone", Vec3(0.0 * math.cos(theta),
            200.0 * math.sin(theta), 200.0 * math.cos(theta)), (0, 0, 1, 1))
        x = x + 0.5