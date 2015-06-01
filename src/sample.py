#TEST ENVIRONMENT
import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math


class World(DirectObject):
      
      
    def initEnvironment(self):
        
        self.woody = loader.loadModel("zevmodels/Woody02")
        self.woody.setScale(0.1)
        self.woody.reparentTo(render)
        
        grass = loader.loadModel("zevmodels/Grass01")
        grass.reparentTo(render)
        grass.setScale(1)
        grass.setY(100)
        grass.setH(-90)
        grass.setX(11)
        grass.setY(11)
        
        """
        for i in range(1,10) :
            for j in range(1,10):
                #Load the first environment model
                grass = loader.loadModel("zevmodels/Grass")
                grass.reparentTo(render)
                grass.setScale(1)
                grass.setY(100)
                grass.setH(-90)
                grass.setX(j*11)
                grass.setY(i*11)
        
        grass = loader.loadModel("zevmodels/Hill_Big")
        grass.reparentTo(render)
        grass.setScale(1)
        grass.setY(100)
        grass.setH(-90)
        grass.setX(5*11)
        grass.setY(6*11)
        
        grass = loader.loadModel("zevmodels/Hill_Big")
        grass.reparentTo(render)
        grass.setScale(1)
        grass.setY(100)
        grass.setH(-90)
        grass.setX(8*11)
        grass.setY(8*11)
        
        grass = loader.loadModel("zevmodels/Hill_Big")
        grass.reparentTo(render)
        grass.setScale(1)
        grass.setY(100)
        grass.setH(-90)
        grass.setX(7*11)
        grass.setY(9*11)
        """
     
    def initCamera(self):
          #la telecamera e gestita in un task separato dal gameloop
          base.disableMouse()
          taskMgr.add(self.controlCamera, "camera-task")
          camera.reparentTo(render)
          camera.lookAt(self.woody)
          """
          camera.setZ(80)
          camera.setP(-40)
          camera.setY(-15)
          """
          
    def controlCamera(self, task):
          if(self.keys['camerafar']==1):
              camera.setY(camera.getY()-1)
          if(self.keys['cameradeep']==1):
              camera.setY(camera.getY()+1)
          if(self.keys['cameraHleft']==1):
              camera.setH(camera.getH()+1)
          if(self.keys['cameraHright']==1):
              camera.setH(camera.getH()-1) 
          if(self.keys['cameraleft']==1):
              camera.setX(camera.getX()-1)
          if(self.keys['cameraright']==1):
              camera.setX(camera.getX()+1) 
          if(self.keys['cameraup']==1):
              camera.setZ(camera.getZ()+1) 
          if(self.keys['cameradown']==1):
              camera.setZ(camera.getZ()-1) 
          if(self.keys['camerapitchup']==1):
              camera.setP(camera.getP()+1) 
          if(self.keys['camerapitchdown']==1):
              camera.setP(camera.getP()-1) 
          
                     
          return Task.cont
    
    
    def initKeys(self):          
          #Tengo traccia in questa variabile di quali tasti sono premuti
          self.keys = {"cameradeep" : 0, "camerafar": 0, "cameraHleft":0, 
                       "cameraHright":0, "cameraleft":0, "cameraright":0,
                       "cameraup":0, "cameradown":0,"camerapitchup":0,
                       "camerapitchdown":0}
    
          #Mediante la funzione setKey mi salvo il fatto che e stato premuto un certo tasto
          self.accept("mouse1", self.setKey, ["cameradeep", 1])
          self.accept("mouse1-up", self.setKey, ["cameradeep", 0])
          self.accept("mouse3", self.setKey, ["camerafar", 1])
          self.accept("mouse3-up", self.setKey, ["camerafar", 0])
          self.accept("q", self.setKey, ["cameraleft", 1])
          self.accept("q-up", self.setKey, ["cameraleft", 0])
          self.accept("w", self.setKey, ["cameraright", 1])
          self.accept("w-up", self.setKey, ["cameraright", 0])
          self.accept("a", self.setKey, ["cameraHleft", 1])
          self.accept("a-up", self.setKey, ["cameraHleft", 0])
          self.accept("s", self.setKey, ["cameraHright", 1])
          self.accept("s-up", self.setKey, ["cameraHright", 0])
          self.accept("z", self.setKey, ["cameraup", 1])
          self.accept("z-up", self.setKey, ["cameraup", 0])
          self.accept("x", self.setKey, ["cameradown", 1])
          self.accept("x-up", self.setKey, ["cameradown", 0])
          self.accept("p", self.setKey, ["camerapitchup", 1])
          self.accept("p-up", self.setKey, ["camerapitchup", 0])
          self.accept("o", self.setKey, ["camerapitchdown", 1])
          self.accept("o-up", self.setKey, ["camerapitchdown", 0])
          
          #self.accept("escape", myfsm.request, ["GameOver"])     
    
    
    def setKey(self, key, val): self.keys[key] = val
        
    
    def enter(self):

      self.initEnvironment() 
      #accepted keys
      self.initKeys()
      #setto la telecamera
      self.initCamera()  
      self.gameTask =taskMgr.add(self.gameLoop, "gameLoop")
      self.gameTask.last = 0 
    
    
    def gameLoop(self, task):
          #Calculate how much time has elapsed
          self.dt = task.time - task.last
          task.last = task.time
                
          #Attualmente nulla
          
          return Task.cont


w = World()  
w.enter()        
run()  

