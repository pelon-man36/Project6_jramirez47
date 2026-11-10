from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
import sys
from SpaceJamClasses import Missile
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import CollisionHandlerEvent, CollisionTraverser
from direct.interval.LerpInterval import LerpFunc
from direct.particles.ParticleEffect import ParticleEffect
import re

class Player(SphereCollideObject):
    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], cTrav: CollisionTraverser, modelPath: str, parentNode: NodePath, nodeName: str,
            texPath: str, posVec: Vec3, posHpr: Vec3, scaleVec: float):
        super(Player, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 8)
        self.taskMgr = taskMgr
        self.accept = accept
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setHpr(posHpr)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.render = parentNode
        self.loader = loader

        self.reloadTimeSniper = 1
        self.reloadTimeGatling = 0.5
        self.missileDistanceSniper = 7000 #Until missile explodes
        self.missileBaySniper = 1 #Ammo
        self.missileDistanceGatling = 3000 #Until missile explodes
        self.missileBayGatling = 10
        self.flight_speed = 5
        self.turn_speed = .5
        self.weapon_options = 0

        self.cntExplode = 0
        self.explodeIntervals = {}
        self.traverser = cTrav
        self.traverser.traverse(self.render)
        self.handler = CollisionHandlerEvent()

        self.SetParticles()

        self.handler.addInPattern("into")
        self.accept("into", self.HandleInto)


        self.taskMgr.add(self.CheckIntervals, "checkMissiles", 34)
        self.EnableHUD()

        self.setKeyBindings()

    def quit(self):
        sys.exit()

    def Upwards(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.MoveUpwards, "upward-thrust")
        else:
            self.taskMgr.remove("upward-thrust")

    def Downwards(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.MoveDownwards, "downward-thrust")
        else:
            self.taskMgr.remove("downward-thrust")

    def Forward(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.MoveForward, "forward-thrust")
        else:
            self.taskMgr.remove("forward-thrust")

    def Backward(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.MoveBackward, "backward-thrust")
        else:
            self.taskMgr.remove("backward-thrust")

    def Leftward(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.MoveLeftward, "leftward-thrust")
        else:
            self.taskMgr.remove("leftward-thrust")

    def Rightward(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.MoveRightward, "rightward-thrust")
        else:
            self.taskMgr.remove("rightward-thrust")
    
    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeftTurn, "left-turn")
        else:
            self.taskMgr.remove("left-turn")

    def RightTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightTurn, "right-turn")
        else:
            self.taskMgr.remove("right-turn")
    
    def MoveUpwards(self, task):
        rate = self.turn_speed
        self.modelNode.setP(self.modelNode.getP() - rate)
        return task.cont

    def MoveDownwards(self, task):
        rate = self.turn_speed
        self.modelNode.setP(self.modelNode.getP() + rate)
        return task.cont

    def MoveForward(self, task):
        speed = self.flight_speed
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.up())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * speed)
        return task.cont

    def MoveBackward(self, task):
        speed = self.flight_speed
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.up())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() - trajectory * speed)
        return task.cont

    def MoveLeftward(self, task):
        rate = self.turn_speed
        self.modelNode.setR(self.modelNode.getR() + rate)
        return task.cont

    def MoveRightward(self, task):
        rate = self.turn_speed
        self.modelNode.setR(self.modelNode.getR() - rate)
        return task.cont
    
    def ApplyLeftTurn(self, task):
        # half a degree every frame
        rate = self.turn_speed
        self.modelNode.setH(self.modelNode.getH() - rate)
        return task.cont

    def ApplyRightTurn(self, task):
        # half a degree every frame
        rate = self.turn_speed
        self.modelNode.setH(self.modelNode.getH() + rate)
        return task.cont

    def Sniper(self):
        if self.missileBaySniper:
            travRate = self.missileDistanceSniper
            aim = self.render.getRelativeVector(self.modelNode, Vec3.up()) # Direction spaceship is facing.
            aim.normalize() # Normalizing a vector makes it consistent all the time.
            fireSolution = aim * travRate
            inFront = aim * 150
            travVec = fireSolution + self.modelNode.getPos()
            self.missileBaySniper -= 1
            tag = "Missile" + str(Missile.missileCount)

            posVec = self.modelNode.getPos() + inFront # Spawn missle infront of the nose of the ship
            currentMissile = Missile(self.loader, "./Assets/Spaceships/Phaser/Phaser/phaser.egg", self.render, tag, posVec, 4.0)

            # fluid = 1 makes collisions be checked between the last interval and this interval to make 
            # sure there's nothing in-between both checks that wasn't hit
            self.traverser.addCollider(currentMissile.collisionNode, self.handler)
            Missile.intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
            Missile.intervals[tag].start()
        else:
            # If not reloading, reload.
            if not self.taskMgr.hasTaskNamed("reload_sniper"):
                print("Initializing reload...")
                # Call reload method, no delay
                self.taskMgr.doMethodLater(0, self.Reload_Sniper, "reload_sniper")
                return Task.cont

    def Gatling(self):
        if self.missileBayGatling:
            travRate = self.missileDistanceGatling
            aim = self.render.getRelativeVector(self.modelNode, Vec3.up())
            aim.normalize()
            fireSolution = aim * travRate
            inFront = aim * 150
            travVec = fireSolution + self.modelNode.getPos()
            self.missileBayGatling -= 1
            tag = "Missile" + str(Missile.missileCount)

            posVec = self.modelNode.getPos() + inFront
            currentMissile = Missile(self.loader, "./Assets/Spaceships/Phaser/Phaser/phaser.egg", self.render, tag, posVec, 4.0)

            self.traverser.addCollider(currentMissile.collisionNode, self.handler)
            Missile.intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
            Missile.intervals[tag].start()
        else:
            if not self.taskMgr.hasTaskNamed("reload_gatling"):
                print("Preparing reload...")
                self.taskMgr.doMethodLater(0, self.Reload_Gatling, "reload_gatling")
                return Task.cont


    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        print("fromNode" + fromNode)
        intoNode = entry.getIntoNodePath().getName()
        print("intoNode" + intoNode)
        intoPosition = Vec3(entry.getSurfacePoint(self.render))

        tempVar = fromNode.split("_")
        print("temVar:" + str(tempVar))
        shooter = tempVar[0]
        print("Shooter:" + str(shooter))
        tempVar = intoNode.split("-")
        print("TempVar1:" + str(tempVar))
        tempVar = intoNode.split("_")
        print("TempVar2:" + str(tempVar))
        victim = tempVar[0]
        print("Victim:" + str(victim))

        pattern = r"[0-9]"
        strippedString = re.sub(pattern, "", victim)

        if (strippedString == "Drone" or strippedString == "Planet" or strippedString == "Space Station"):
            print(victim, " hit at ", intoPosition)
            self.DestroyObject(victim, intoPosition)

        print(shooter + "is DONE")
        Missile.intervals[shooter].finish()

    def DestroyObject(self, hitID, hitPosition):
        nodeID = self.render.find(hitID)
        nodeID.detachNode()

        self.explodeNode.setPos(hitPosition)
        self.Explode()

    def Explode(self):
        self.cntExplode += 1
        tag = "particles-" + str(self.cntExplode)

        self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, duration = 4.0)
        self.explodeIntervals[tag].start()

    def ExplodeLight(self, t):
        if t == 1.0 and self.explodeEffect:
            self.explodeEffect.disable()
        elif t == 0:
            self.explodeEffect.start(self.explodeNode)

    def SetParticles(self):
        self.explodeEffect = ParticleEffect()
        self.explodeEffect.loadConfig("./Assets/Part-Efx/default_efx.ptf")
        self.explodeEffect.setScale(70)
        self.explodeNode = self.render.attachNewNode("ExplosionEffects")

    def Reload_Sniper(self, task):
        if task.time > self.reloadTimeSniper:
            self.missileBaySniper += 1
            print("Reload complete.")
            if self.missileBaySniper > 1:
                self.missileBaySniper = 1
            return Task.done
        elif task.time <= self.reloadTimeSniper:
            print("Reload processing...")
            return Task.cont

    def Reload_Gatling(self, task):
        if task.time > self.reloadTimeGatling:
            self.missileBayGatling += 10
            print("Reload complete.")
            if self.missileBayGatling > 10:
                self.missileBayGatling = 10
            return Task.done
        elif task.time <= self.reloadTimeGatling:
            print("Reload processing...")
            return Task.cont

    def Speed(self):
        print("Speed boost activated.")
        self.taskMgr.add(self.SpeedBoost, "speed-boost")

    def SpeedBoost(self, task):
        if task.time > 5:
            print("Speed boost deactivated.")
            self.flight_speed = 5
            self.turn_speed = .5
            return Task.done
        elif task.time <= 5:
            print("Speed boost processing...")
            self.flight_speed = 20
            self.turn_speed = 1
            return Task.cont

    def Swap(self, keyDown):
        if keyDown:
            self.weapon_options += 1
            if self.weapon_options > 1:
                self.weapon_options = 0
            print("Arsenal " + str(self.weapon_options) + " enabled.")

    def Fire(self):
        if self.weapon_options == 0:
            self.Sniper()
        elif self.weapon_options == 1:
            self.Gatling()

    def CheckIntervals(self, task):
        for i in Missile.intervals:
            if not Missile.intervals[i].isPlaying():
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()
                del Missile.intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]
                print(i + " has reached the end of its fire solution.")
                break
        return Task.cont

    def EnableHUD(self):
        self.Hud = OnscreenImage(image = "./Assets/Spaceships/target.png", pos = Vec3(0, 0, 0), scale = 0.1)
        self.Hud.setTransparency(1)
    
    def setKeyBindings(self):
        # key bindings for ship movement
        self.accept("escape", self.quit)
        self.accept("f", self.Fire)
        self.accept("rshift", self.Speed)
        self.accept("arrow_up", self.Upwards, [1])
        self.accept("arrow_up-up", self.Upwards, [0])
        self.accept("arrow_down", self.Downwards, [1])
        self.accept("arrow_down-up", self.Downwards, [0])
        self.accept("w", self.Forward, [1])
        self.accept("w-up", self.Forward, [0])
        self.accept("s", self.Backward, [1])
        self.accept("s-up", self.Backward, [0])
        self.accept("a", self.Leftward, [1])
        self.accept("a-up", self.Leftward, [0])
        self.accept("d", self.Rightward, [1])
        self.accept("d-up", self.Rightward, [0])
        self.accept("m", self.Swap, [1])
        self.accept("m-up", self.Swap, [0])
        self.accept("arrow_left", self.LeftTurn, [1])
        self.accept("arrow_left-up", self.LeftTurn, [0])
        self.accept("arrow_right", self.RightTurn, [1])
        self.accept("arrow_right-up", self.RightTurn, [0])