from direct.showbase.ShowBase import ShowBase
import SpaceJamClasses as spaceJamClasses
import DefensePaths as defensePaths
import Player as player
from panda3d.core import *
from panda3d.core import CollisionTraverser, CollisionHandlerPusher

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setScene()
        fullCycle = 60

        for j in range(fullCycle):
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.Station, nickName, j, fullCycle, 2)

        self.circleX = defensePaths.createCircleX(self)
        self.circleZ = defensePaths.createCircleZ(self)
        self.circleY = defensePaths.createCircleY(self)

        self.setCamera()

        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
    
        self.pusher.addCollider(self.Player.collisionNode, self.Player.modelNode)
        self.cTrav.addCollider(self.Player.collisionNode, self.pusher)
        self.cTrav.showCollisions(self.render)


    def setScene(self):
        self.Player = player.Player(self.loader, self.taskMgr, self.accept, "./Assets/Spaceships/ship.obj", self.render,
            "Player", "./Assets/Spaceships/Ship_ship_mat_BaseMap.tga", (0, 400, 0), (180, 0, 0), 5)

        self.Universe = spaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render,
            "Universe", "./Assets/Universe/Universe.jpg", (0, 0, 0), 15000)

        self.Planet1 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render,
            "Planet1", "./Assets/Planets/Planet1.jpg", (-1500, 5000, 350), 100)

        self.Planet2 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render,
            "Planet2", "./Assets/Planets/Planet2.png", (4000, 3000, 400), 100)

        self.Planet3 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render,
            "Planet3", "./Assets/Planets/Planet3.png", (-4000, -2000, -400), 100)

        self.Planet4 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render,
            "Planet4", "./Assets/Planets/Planet4.png", (-2000, 1000, 450), 100)

        self.Planet5 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render,
            "Planet5", "./Assets/Planets/Planet5.png", (0, 0, 5000), 100)

        self.Planet6 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render,
            "Planet6", "./Assets/Planets/Planet6.png", (2000, 6000, 0), 100)

        self.Station = spaceJamClasses.SpaceStation(self.loader, "./Assets/Space_Station/SpaceStation1B/spaceStation.egg",
            self.render, "SpaceStation", (5000, 4000, 70), 50)
        

    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/Spaceships/DroneDefender/DroneDefender.obj",
            self.render, droneName, "./Assets/Spaceships/DroneDefender/octotoad1_auv.png", position, 5)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/Spaceships/DroneDefender/DroneDefender.obj",
            self.render, droneName, "./Assets/Spaceships/DroneDefender/octotoad1_auv.png", position, 10)

    def setCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Player.modelNode)
        self.camera.setFluidPos(0, 4, -30)
        self.camera.setHpr(180, 90, 0)







app = MyApp()
app.run()