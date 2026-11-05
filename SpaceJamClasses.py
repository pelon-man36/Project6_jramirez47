from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from CollideObjectBase import *

class Planet(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,
        texPath: str, posVec: Vec3, scaleVec: float):
        super(Planet, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1.5)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Universe(InverseSphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,
        texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)


class SpaceStation(CapsuleCollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,
        posVec: Vec3, scaleVec: float):
        super(SpaceStation, self).__init__(loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

class Drone(SphereCollideObject):
    droneCount = 0
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,
        texPath: str, posVec: Vec3, scaleVec: float):
        super(Drone, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class XYZDrone(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,
        posVec: Vec3, RGB: tuple):
        super(XYZDrone, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3)
        self.modelNode.setPos(posVec)
        tex = self.modelNode.setColor(RGB)
        self.modelNode.setName(nodeName)

class Missile(SphereCollideObject):
    missileCount = 0
    fireModels = {}
    cNodes = {}
    collisionSolids = {}
    intervals = {}
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, 
        posVec: Vec3, scaleVec: float = 1.0):
        super(Missile, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.0)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setPos(posVec)

        Missile.missileCount += 1
        Missile.fireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName] = self.collisionNode

        # We retrieve the solid for our collisionNode
        Missile.collisionSolids[nodeName] = self.collisionNode.node().getSolid(0)
        Missile.cNodes[nodeName].show()

        print("Fire missle #" + str(Missile.missileCount))
