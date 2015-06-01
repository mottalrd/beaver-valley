import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject
from direct.fsm import FSM
import random, sys, os, math
from direct.showbase import Audio3DManager
from threading import Timer
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from pandac.PandaModules import FontPool
from pandac.PandaModules import OdeUtil
import codecs ,random, math
from direct.gui.OnscreenImage import OnscreenImage


class World(DirectObject):
  
    ENVDIST=7
    ENVSCALE=5
    SKYSCALE=5.7
    SKYDIST=-15
    
    #Hardcode length parameters of the environment
    XLENGTH=22.1
    YLENGTH=22.1
    
    #The matrix of positions
    MX=50
    MY=50
    M=[]
    
    #village y position
    VILLAGE=4
    
              
    def initM(self):
        #############################################
        # Init the matrix for the puzzle
        # The matrix may contain 
        # 'N' : nothing
        # 'H' : hill
        # 'T' : tree
        # 'House' : house
        #############################################
        self.M=[]
        for i in range(0,self.MY):
            self.M.append([])
            for j in range(0,self.MX):
                self.M[i].append('N')


    def getLastY(self):
        return self.YLENGTH/2 
       
        
    def getLastX(self): 
        return self.XLENGTH/2

    
    def loadLevel1(self):
          self.score_to_win=400
          self.odeworld.setGravity(0, -0.01, -0.01)
          #Number of dams in the level
          #!!!BE COHERENT
          self.dam_n=3
          ##############################################
          # Populate the world with 
          # finite state machines
          ##############################################
          dam1=self.damFSM(15,49,10,3,self)
          dam2=self.damFSM(25,49,8,4,self, last=True)
          dam3=self.damFSM(35,49,10,3,self)
          self.FSMList.append(dam1)
          self.FSMList.append(dam2) 
          self.FSMList.append(dam3)
                 
          ##tree to be used for bars       
          self.FSMList.append(self.treeFSM(4,31,self,little=True))
          self.FSMList.append(self.treeFSM(5,29,self,little=True))
          self.FSMList.append(self.treeFSM(5,17,self,little=True))
          self.FSMList.append(self.treeFSM(6,20,self))
          self.FSMList.append(self.treeFSM(8,20,self,little=True))
          self.FSMList.append(self.treeFSM(45,17,self))
          self.FSMList.append(self.treeFSM(44,15,self))
          self.FSMList.append(self.treeFSM(44,19,self,little=True))
          self.FSMList.append(self.treeFSM(46,20,self,little=True))
          
          ##tree to be used for deflecting
          self.FSMList.append(self.treeFSM(24,35,self,little=True))
          self.FSMList.append(self.treeFSM(22,20,self,little=True))
          self.FSMList.append(self.treeFSM(20,18,self,little=True))
          self.FSMList.append(self.treeFSM(33,19,self))
          self.FSMList.append(self.treeFSM(35,17,self))
          self.FSMList.append(self.treeFSM(37,15,self))
          
          self.FSMList.append(self.treeFSM(39,30,self))
          
          ##hills
          self.FSMList.append(self.hillFSM(27,32,self))
          self.FSMList.append(self.hillFSM(30,22,self))
          self.FSMList.append(self.hillFSM(40,33,self))
          self.FSMList.append(self.hillFSM(13,35,self))
          self.FSMList.append(self.hillFSM(17,39,self))
          self.FSMList.append(self.hillFSM(15,20,self))
          
          #houses
          self.FSMList.append(self.houseFSM(24,30,self))
          self.FSMList.append(self.houseFSM(14,28,self))
          
          self.FSMList.append(self.houseFSM(12,4,self))
          self.FSMList.append(self.houseFSM(16,2,self))
          self.FSMList.append(self.houseFSM(20,4,self))
          self.FSMList.append(self.houseFSM(26,4,self,mayor=True))
          self.FSMList.append(self.houseFSM(34,5,self,dorothy=True))
          self.FSMList.append(self.houseFSM(39,2,self))

        
          ##############################################
          # Populate border dams
          # HARDCODED THAN EVER IN GAME HISTORY
          ##############################################
          DAMSCALE=1.35
          dam=Actor("models/Dam",{"Break":"models/Dam_Break"})
          dam.setScale(DAMSCALE)
          dam.reparentTo(self.environ)    
          self.setPos(dam, 'N', 10, 49)
          dam.setY(dam.getY()-0.3)
          dam.setX(dam.getX()+0.3)
          dam.setH(dam.getH()+20)
          
          ###########################################
          # Top dams 
          ###########################################
          dam_1=loader.loadModel("models/Dam")
          dam_1.reparentTo(self.environ)
          dam_1.setScale(1.47)
          self.setPos(dam_1, 'N', 20, 49)
          dam_1=loader.loadModel("models/Dam")
          dam_1.reparentTo(self.environ)
          dam_1.setScale(1.47)
          self.setPos(dam_1, 'N', 30, 49)     
          
          ###########################################
          # Lateral dams
          ###########################################
          for i in range(5):
            damtmp=dam.copyTo(self.environ) 
            self.setPos(damtmp, 'N', 8-2*i, 46-4*i)
            damtmp.setH(dam.getH()+40)
            
          dam=Actor("models/Dam",{"Break":"models/Dam_Break"})
          dam.setScale(DAMSCALE)
          dam.reparentTo(self.environ)    
          self.setPos(dam, 'N', 40, 49)
          dam.setY(dam.getY()-0.3)
          dam.setX(dam.getX()-0.3)
          dam.setH(dam.getH()-20)
          
          for i in range(4):
            damtmp=dam.copyTo(self.environ) 
            self.setPos(damtmp, 'N', 42+2*i, 46-4*i)
            damtmp.setH(dam.getH()-40)
          damtmp=dam.copyTo(self.environ) 
          self.setPos(damtmp, 'N', 49, 46-4*4)
          damtmp.setX(damtmp.getX()+0.7)
          damtmp.setH(dam.getH()-40)
            
          ###########################################
          # Water Lake
          ###########################################  
          water=loader.loadModel("models/plane")
          wtex=loader.loadTexture("models/water/Water01.jpg")
          water.setTexture(wtex)
          water.setScale(12)
          water.setP(-90)
          water.setZ(water.getZ()+0.25);
          
          water.setR(water.getR()-60)
          water.setY(water.getY()+9)
          water.setX(water.getX()-15)
          water.reparentTo(self.environ)
          
          ambient = AmbientLight('ambient')
          ambient.setColor(Vec4(1,1,1,1))
          ambientNP = water.attachNewNode(ambient.upcastToPandaNode())
          water.setLightOff()
          water.setLight(ambientNP)          
          
          water=loader.loadModel("models/plane")
          wtex=loader.loadTexture("models/water/Water01.jpg")
          water.setTexture(wtex)
          water.setScale(12)
          water.setP(-90)
          water.setZ(water.getZ()+0.25);
          
          water.setR(water.getR()+60)
          water.setY(water.getY()+9)
          water.setX(water.getX()+15)
          water.reparentTo(self.environ)
          
          ambient = AmbientLight('ambient')
          ambient.setColor(Vec4(1,1,1,1))
          ambientNP = water.attachNewNode(ambient.upcastToPandaNode())
          water.setLightOff()
          water.setLight(ambientNP)
          
          water=loader.loadModel("models/plane")
          wtex=loader.loadTexture("models/water/Water01.jpg")
          water.setTexture(wtex)
          water.setScale(20)
          water.setP(-90)
          water.setZ(water.getZ()+0.25);
          
          water.setY(water.getY()+21.5)
          water.reparentTo(self.environ)
          
          ambient = AmbientLight('ambient')
          ambient.setColor(Vec4(1,1,1,1))
          ambientNP = water.attachNewNode(ambient.upcastToPandaNode())
          water.setLightOff()
          water.setLight(ambientNP)

          
          ###############################################
          # Populate borders trees
          ###############################################
          TREESCALE=0.35
          TREESCALE_little=0.12
          def CreateShadow(np,z_scale):
             sh=np.copyTo(self.environ)
             sh.reparentTo(np)
             sh.setX(np.getX()+0.3)
             sh.setScale(1,1,z_scale)
             sh.setTransparency(TransparencyAttrib.MAlpha)     
             sh.setColor(0,0,0,.4)   
             return sh   
          
          tree=loader.loadModel("models/GroomedTree/GroomedTree")
          tree.setScale(TREESCALE_little)
          tree.reparentTo(self.environ)
          self.setPos(tree, 'N', 1, 25)
          tree.setX(tree.getX()-1)
          
          treebig=loader.loadModel("models/Tree")
          treebig.reparentTo(self.environ)
          treebig.setScale(TREESCALE)
          self.setPos(treebig, 'N', 0, 26) 
          treebig.setX(treebig.getX()-1) 
          
          for i in range(3):
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 0, 27-i*7)
              tree.setX(tree.getX()-1)
          
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 1, 26-i*7)
              tree.setX(tree.getX()-1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 0, 24-i*7)
              treebig.setX(treebig.getX()-1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 1, 25-i*7)
              treebig.setX(treebig.getX()-1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 1, 22-i*7)
              treebig.setX(treebig.getX()-1)
          
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 0, 22-i*7)
              tree.setX(tree.getX()-1)
          
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 0, 21-i*7)
              tree.setX(tree.getX()-1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 1, 21-i*7)
              treebig.setX(treebig.getX()-1)

              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 0, 20-i*7)
              treebig.setX(treebig.getX()-1)
              
          tree=loader.loadModel("models/GroomedTree/GroomedTree")
          tree.setScale(TREESCALE_little)
          tree.reparentTo(self.environ)
          self.setPos(tree, 'N', 48, 25)
          tree.setX(tree.getX()+1)
          
          treebig=loader.loadModel("models/Tree")
          treebig.reparentTo(self.environ)
          treebig.setScale(TREESCALE)
          self.setPos(treebig, 'N', 49, 26)
          treebig.setX(tree.getX()+1)  
          
          for i in range(3):
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 49, 27-i*7)
              tree.setX(tree.getX()+1)
          
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 48, 26-i*7)
              tree.setX(tree.getX()+1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 49, 24-i*7)
              treebig.setX(treebig.getX()+1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 48, 25-i*7)
              treebig.setX(treebig.getX()+1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 48, 22-i*7)
              treebig.setX(treebig.getX()+1)
          
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 49, 22-i*7)
              tree.setX(tree.getX()+1)
          
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 49, 21-i*7)
              tree.setX(tree.getX()+1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 48, 21-i*7)
              treebig.setX(treebig.getX()+1)

              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 49, 20-i*7)
              treebig.setX(treebig.getX()+1)
              

    def loadLevel2(self):
          
          self.score_to_win=500
          self.odeworld.setGravity(0, -0.005, -0.01)
          #Number of dams in the level
          #!!!BE COHERENT
          self.dam_n=5          
          ##############################################
          # Populate the world with 
          # finite state machines
          ##############################################
          dam1=self.damFSM(15,49,12,3,self)
          dam2=self.damFSM(20,49,8,4,self)
          dam2=self.damFSM(25,49,8,4,self)
          dam2=self.damFSM(30,49,8,4,self, last=True)
          dam3=self.damFSM(35,49,12,3,self)
          self.FSMList.append(dam1)
          self.FSMList.append(dam2) 
          self.FSMList.append(dam3)

                 
          ##tree to be used for bars       
          self.FSMList.append(self.treeFSM(4,31,self,little=True))
          self.FSMList.append(self.treeFSM(5,29,self,little=True))
          self.FSMList.append(self.treeFSM(5,17,self,little=True))
          self.FSMList.append(self.treeFSM(6,20,self))
          self.FSMList.append(self.treeFSM(8,20,self,little=True))
          self.FSMList.append(self.treeFSM(45,17,self))
          self.FSMList.append(self.treeFSM(44,15,self))
          self.FSMList.append(self.treeFSM(44,19,self,little=True))
          self.FSMList.append(self.treeFSM(46,20,self,little=True))
          self.FSMList.append(self.treeFSM(5,33,self))
          self.FSMList.append(self.treeFSM(4,26,self))
          
          ##tree to be used for deflecting
          self.FSMList.append(self.treeFSM(24,35,self,little=True))
          
          self.FSMList.append(self.treeFSM(24,22,self))
          self.FSMList.append(self.treeFSM(22,20,self,little=True))
          self.FSMList.append(self.treeFSM(20,18,self,little=True))
          self.FSMList.append(self.treeFSM(18,16,self))
          self.FSMList.append(self.treeFSM(16,14,self))
          
          self.FSMList.append(self.treeFSM(34,40,self))
          self.FSMList.append(self.treeFSM(36,38,self))
          self.FSMList.append(self.treeFSM(38,36,self))
          
          
          self.FSMList.append(self.treeFSM(28,25,self))
          self.FSMList.append(self.treeFSM(33,19,self))
          self.FSMList.append(self.treeFSM(35,17,self))
          self.FSMList.append(self.treeFSM(37,15,self))
          self.FSMList.append(self.treeFSM(39,30,self))
          
          ##hills
          self.FSMList.append(self.hillFSM(27,32,self))
          self.FSMList.append(self.hillFSM(30,22,self))
          self.FSMList.append(self.hillFSM(40,33,self))
          self.FSMList.append(self.hillFSM(13,35,self))
          self.FSMList.append(self.hillFSM(17,39,self))
          self.FSMList.append(self.hillFSM(12,20,self))
          self.FSMList.append(self.hillFSM(19,24,self))
          
          #houses
          self.FSMList.append(self.houseFSM(24,30,self))
          self.FSMList.append(self.houseFSM(14,28,self))
          
          self.FSMList.append(self.houseFSM(12,4,self))
          self.FSMList.append(self.houseFSM(16,2,self))
          self.FSMList.append(self.houseFSM(20,4,self))
          self.FSMList.append(self.houseFSM(26,4,self,mayor=True))
          self.FSMList.append(self.houseFSM(34,5,self,dorothy=True))
          self.FSMList.append(self.houseFSM(39,2,self))

        
          ##############################################
          # Populate border dams
          # HARDCODED THAN EVER IN GAME HISTORY
          ##############################################
          DAMSCALE=1.35
          dam=Actor("models/Dam",{"Break":"models/Dam_Break"})
          dam.setScale(DAMSCALE)
          dam.reparentTo(self.environ)    
          self.setPos(dam, 'N', 10, 49)
          dam.setY(dam.getY()-0.3)
          dam.setX(dam.getX()+0.3)
          dam.setH(dam.getH()+20)
          
          ###########################################
          # Top dams 
          ###########################################
          dam_1=loader.loadModel("models/Dam")
          dam_1.reparentTo(self.environ)
          dam_1.setScale(1.47)
          self.setPos(dam_1, 'N', 20, 49)
          dam_1=loader.loadModel("models/Dam")
          dam_1.reparentTo(self.environ)
          dam_1.setScale(1.47)
          self.setPos(dam_1, 'N', 30, 49)     
          
          ###########################################
          # Lateral dams
          ###########################################
          for i in range(5):
            damtmp=dam.copyTo(self.environ) 
            self.setPos(damtmp, 'N', 8-2*i, 46-4*i)
            damtmp.setH(dam.getH()+40)
            
          dam=Actor("models/Dam",{"Break":"models/Dam_Break"})
          dam.setScale(DAMSCALE)
          dam.reparentTo(self.environ)    
          self.setPos(dam, 'N', 40, 49)
          dam.setY(dam.getY()-0.3)
          dam.setX(dam.getX()-0.3)
          dam.setH(dam.getH()-20)
          
          for i in range(4):
            damtmp=dam.copyTo(self.environ) 
            self.setPos(damtmp, 'N', 42+2*i, 46-4*i)
            damtmp.setH(dam.getH()-40)
          damtmp=dam.copyTo(self.environ) 
          self.setPos(damtmp, 'N', 49, 46-4*4)
          damtmp.setX(damtmp.getX()+0.7)
          damtmp.setH(dam.getH()-40)
            
          ###########################################
          # Water Lake
          ###########################################  
          water=loader.loadModel("models/plane")
          wtex=loader.loadTexture("models/water/Water01.jpg")
          water.setTexture(wtex)
          water.setScale(12)
          water.setP(-90)
          water.setZ(water.getZ()+0.25);
          
          water.setR(water.getR()-60)
          water.setY(water.getY()+9)
          water.setX(water.getX()-15)
          water.reparentTo(self.environ)
          
          ambient = AmbientLight('ambient')
          ambient.setColor(Vec4(1,1,1,1))
          ambientNP = water.attachNewNode(ambient.upcastToPandaNode())
          water.setLightOff()
          water.setLight(ambientNP)          
          
          water=loader.loadModel("models/plane")
          wtex=loader.loadTexture("models/water/Water01.jpg")
          water.setTexture(wtex)
          water.setScale(12)
          water.setP(-90)
          water.setZ(water.getZ()+0.25);
          
          water.setR(water.getR()+60)
          water.setY(water.getY()+9)
          water.setX(water.getX()+15)
          water.reparentTo(self.environ)
          
          ambient = AmbientLight('ambient')
          ambient.setColor(Vec4(1,1,1,1))
          ambientNP = water.attachNewNode(ambient.upcastToPandaNode())
          water.setLightOff()
          water.setLight(ambientNP)
          
          water=loader.loadModel("models/plane")
          wtex=loader.loadTexture("models/water/Water01.jpg")
          water.setTexture(wtex)
          water.setScale(20)
          water.setP(-90)
          water.setZ(water.getZ()+0.25);
          
          water.setY(water.getY()+21.5)
          water.reparentTo(self.environ)
          
          ambient = AmbientLight('ambient')
          ambient.setColor(Vec4(1,1,1,1))
          ambientNP = water.attachNewNode(ambient.upcastToPandaNode())
          water.setLightOff()
          water.setLight(ambientNP)

          
          ###############################################
          # Populate borders trees
          ###############################################
          TREESCALE=0.35
          TREESCALE_little=0.12
          def CreateShadow(np,z_scale):
             sh=np.copyTo(self.environ)
             sh.reparentTo(np)
             sh.setX(np.getX()+0.3)
             sh.setScale(1,1,z_scale)
             sh.setTransparency(TransparencyAttrib.MAlpha)     
             sh.setColor(0,0,0,.4)   
             return sh   
          
          tree=loader.loadModel("models/GroomedTree/GroomedTree")
          tree.setScale(TREESCALE_little)
          tree.reparentTo(self.environ)
          self.setPos(tree, 'N', 1, 25)
          tree.setX(tree.getX()-1)
          
          treebig=loader.loadModel("models/Tree")
          treebig.reparentTo(self.environ)
          treebig.setScale(TREESCALE)
          self.setPos(treebig, 'N', 0, 26) 
          treebig.setX(treebig.getX()-1) 
          
          for i in range(3):
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 0, 27-i*7)
              tree.setX(tree.getX()-1)
          
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 1, 26-i*7)
              tree.setX(tree.getX()-1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 0, 24-i*7)
              treebig.setX(treebig.getX()-1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 1, 25-i*7)
              treebig.setX(treebig.getX()-1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 1, 22-i*7)
              treebig.setX(treebig.getX()-1)
          
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 0, 22-i*7)
              tree.setX(tree.getX()-1)
          
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 0, 21-i*7)
              tree.setX(tree.getX()-1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 1, 21-i*7)
              treebig.setX(treebig.getX()-1)

              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 0, 20-i*7)
              treebig.setX(treebig.getX()-1)
              
          tree=loader.loadModel("models/GroomedTree/GroomedTree")
          tree.setScale(TREESCALE_little)
          tree.reparentTo(self.environ)
          self.setPos(tree, 'N', 48, 25)
          tree.setX(tree.getX()+1)
          
          treebig=loader.loadModel("models/Tree")
          treebig.reparentTo(self.environ)
          treebig.setScale(TREESCALE)
          self.setPos(treebig, 'N', 49, 26)
          treebig.setX(tree.getX()+1)  
          
          for i in range(3):
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 49, 27-i*7)
              tree.setX(tree.getX()+1)
          
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 48, 26-i*7)
              tree.setX(tree.getX()+1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 49, 24-i*7)
              treebig.setX(treebig.getX()+1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 48, 25-i*7)
              treebig.setX(treebig.getX()+1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 48, 22-i*7)
              treebig.setX(treebig.getX()+1)
          
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 49, 22-i*7)
              tree.setX(tree.getX()+1)
          
              tree=tree.copyTo(self.environ)
              tree.setScale(TREESCALE_little)
              self.setPos(tree, 'N', 49, 21-i*7)
              tree.setX(tree.getX()+1)
          
              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 48, 21-i*7)
              treebig.setX(treebig.getX()+1)

              treebig=treebig.copyTo(self.environ)
              treebig.setScale(TREESCALE)
              self.setPos(treebig, 'N', 49, 20-i*7)
              treebig.setX(treebig.getX()+1)

      
    def initEnvironment(self):
          #############################################
          # Init the game square (environ) and the sky
          # Init collision solid for the square
          #############################################
          self.environ = loader.loadModel("models/Grass")          
          self.environ.reparentTo(render)
          self.environ.setPos(0, self.ENVDIST,0-1)
          self.environ.setScale(self.ENVSCALE)
                             
          self.sky = loader.loadModel("models/Sky")
          self.sky.reparentTo(render)
          self.sky.setPos(0, self.SKYDIST ,0-28)
          self.sky.setScale(self.SKYSCALE)
          
          #Create a collision solid for the environment
          cNode = CollisionNode('environ')
          cNode.addSolid(CollisionInvSphere(0,0,0,10.2))
          environC = self.environ.attachNewNode(cNode)
          #environC.show()
          
                  
    def setPos(self,e,id,x,y):
          #############################################
          # Starting from the real matrix coordinates 
          # set the real position in the world
          # reparented to the environ
          #############################################
          posx=float((self.XLENGTH/self.MX))*x
          posy=float((self.YLENGTH/self.MY))*y
          X=-self.XLENGTH/2 + posx
          Y=-self.YLENGTH/2 + posy
          e.setX(X)
          e.setY(Y)
          
          #hills are 3x3 matrix
          if(id=='H'): 
              self.M[x-1][y+1]='H'
              self.M[x-1][y]='H'
              self.M[x-1][y-1]='H'
              self.M[x][y+1]='H'
              self.M[x][y]='H'
              self.M[x][y-1]='H'
              self.M[x+1][y+1]='H'
              self.M[x+1][y]='H'
              self.M[x+1][y-1]='H'  
              
          else:
              self.M[x][y]=id
         
         
    def isValidPos(self,x,y):
        ###############################################
        # Defines where it is possible to place a bar
        # Moreover it returns the orientation of the bar
        # for that place
        ###############################################
        def isValid(c):
            if c=='T' or c=='H': return True
            else: return False
        if x+1<self.MX and y+1<self.MY and x-1>=0 and y-1>=0:
            if isValid(self.M[x+1][y+1]) and isValid(self.M[x-1][y-1]) and self.M[x][y]=='N': 
                ret='left'
            elif isValid(self.M[x-1][y+1]) and isValid(self.M[x+1][y-1]) and self.M[x][y]=='N': 
                ret='right' 
            else:
                ret='invalid'
        else:
            ret='invalid'
        return ret
    
    
    def updateValidPos(self):
          ###########################################
          # Place a collision solid in every
          # admissible place for the bar
          # Place a bar finite state machine
          # in every admissible place
          ###########################################
          for p in self.placelist :
              p.removeNode()
          for i in range(0,self.MX):
            for j in range(0,self.MY):
                ret=self.isValidPos(i,j)
                if ret!='invalid':
                    pNode=loader.loadModel("models/plane")
                    pNode.reparentTo(self.environ)
                    pNode.hide()                        
                    self.setPos(pNode, 'N', i, j)
                    
                    #Create a collision solid for this model
                    cNode = CollisionNode('Placebar')
                    cNode.addSolid(CollisionSphere(0,0,1,1))
                    cNode.setCollideMask(self.PANDAPLACEMASK)
                    placeC = pNode.attachNewNode(cNode)
                    #uncomment this line if you wanna see the collision solid
                    #placeC.show() 
                    self.placelist.append(pNode)       
                    
                    #Place a barFSM in that place and pass him information
                    #about surroundings trees
                    tree1=None
                    tree2=None
                    if self.getFSMInPos(i+1,j+1)!= None:
                        if self.getFSMInPos(i+1,j+1).tag=='tree': tree1=self.getFSMInPos(i+1,j+1)
                    if self.getFSMInPos(i-1,j-1)!= None:
                        if self.getFSMInPos(i-1,j-1).tag=='tree': tree2=self.getFSMInPos(i-1,j-1)
                    if self.getFSMInPos(i-1,j+1)!= None:
                        if self.getFSMInPos(i-1,j+1).tag=='tree': tree1=self.getFSMInPos(i-1,j+1)
                    if self.getFSMInPos(i+1,j-1)!= None:
                        if self.getFSMInPos(i+1,j-1).tag=='tree': tree2=self.getFSMInPos(i+1,j-1)
                    self.FSMList.append(self.barFSM(i,j,self,ret,tree1,tree2))
                    
                                                  
    def getFSMInPos(self, x, y):
        ################################################
        # Given the position in the matrix 
        # it return the corresponding fsm
        ################################################
        for i in range(0,len(self.FSMList)):
            if(self.FSMList[i].x==x and self.FSMList[i].y==y):
                return self.FSMList[i]
        return None
    
    
    def getFSMInPosXY(self, X, Y):
        ################################################
        # Given the position in the world 
        # (reparented to environ) it returns 
        # the corresponding fsm
        ################################################
        for i in range(0,len(self.FSMList)):
            if(self.FSMList[i].X==X and self.FSMList[i].Y==Y):
                return self.FSMList[i]
        return None    
              
    
    def initKeys(self): 
          ################################################
          # Init the keyboard interaction
          # When the keyboard is pressed this is 
          # recorded in self.keys
          ################################################   
          #Used for delays in getKey()
          self.keyflag=True      
          
          self.keys = {"cameradeep" : 0, "camerafar": 0, "cameraHleft":0, 
                       "cameraHright":0, "cameraleft":0, "cameraright":0,
                       "cameraup":0, "cameradown":0,"camerapitchup":0,
                       "camerapitchdown":0, "woodyleft":0, "woodyright":0,
                       "woodyforward":0,"space":0, "changeview":0,"doBar":0,
                       "place_bar_weak":0,"place_bar_fresh":0}
    
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
          self.accept("arrow_left", self.setKey, ["woodyleft", 1])
          self.accept("arrow_left-up", self.setKey, ["woodyleft", 0])
          self.accept("arrow_right", self.setKey, ["woodyright", 1])
          self.accept("arrow_right-up", self.setKey, ["woodyright", 0])
          self.accept("arrow_up", self.setKey, ["woodyforward", 1])
          self.accept("arrow_up-up", self.setKey, ["woodyforward", 0])
          self.accept("s",self.setKey,["place_bar_weak",1])
          self.accept("s-up",self.setKey,["place_bar_weak",0])
          self.accept("d",self.setKey,["place_bar_fresh",1])
          self.accept("d-up",self.setKey,["place_bar_fresh",0])
          self.accept("enter",self.setKey,["changeview",1])
          self.accept("enter-up",self.setKey,["changeview",0])
          self.accept("escape", self.gamefsm.request, ["GameOver", self.level]) 
          self.accept("space",self.setKey,["doBar",1])
          self.accept("space-up",self.setKey,["doBar",0])
  
    
    def setKey(self, key, val): 
        ################################################
        # Update the keys list
        ################################################
        self.keys[key] = val
    
    
    def getKey(self, key):
        def delaykey(task):
            self.keyflag=True
        
        if self.disableKeys==True:
            return 0
            
        #Keys that needs a delay. Two sets avaiable for different delays    
        set1=['changeview']
        set2=['place_bar_weak','place_bar_fresh','doBar']
        if key in set1 or key in set2:
            if self.keyflag and self.keys[key]==1:
                self.keyflag=False
                if key in set1 : delay=0.5
                else: delay=0.5
                taskMgr.doMethodLater(delay, delaykey, 'woodyTask')
                return 1
            else:
                return 0
        else: 
            return self.keys[key]
        
    
    def initLight(self):
        ################################################
        # Init the light for the environment
        ################################################
        ambientLight = AmbientLight( 'ambientLight' )
        ambientLight.setColor( Vec4( 0.2, 0.2, 0.2, 1 ) )
        ambientLightNP = render.attachNewNode( ambientLight.upcastToPandaNode() )
        self.environ.setLight(ambientLightNP)
        
        directionalLight = DirectionalLight( "directionalLight" )
        directionalLight.setColor( Vec4( 1, 1, 1, 1 ) )
        directionalLightNP = render.attachNewNode( directionalLight.upcastToPandaNode() )
        # This light is facing forwards, away from the camera.
        directionalLightNP.setHpr(0, -30, 0)
        directionalLightNP.setZ(20)
        self.environ.setLight(directionalLightNP)        
      
        
    def exit(self):
      ################################################
      # Remove all the tasks and environment
      ################################################
      taskMgr.remove('waterTask')
      taskMgr.remove('gameLoop')
      taskMgr.remove('dumpExplode')
      taskMgr.remove('woodyTask')
      taskMgr.remove('cameraTask')
      
      self.ignoreAll()
      self.environ.removeNode()
      self.sky.removeNode()
      
      if self.card!=None:
          self.card.removeNode()

      camera.detachNode()
      
      self.soundfsm.request('Stop')
      
      for i in self.textItems:
          i.destroy()
   
      for i in self.timerItems:
          i.cancel()
          
      for i in self.iconItems:
          i.destroy()
    
      if(self.mySound!=None):
          if(self.mySound.status()==2):
              self.mySound.stop()
      
      self.owned_bars_weak_displayed.destroy()    
      self.owned_bars_fresh_displayed.destroy() 
    
      
    def enter(self, gamefsm, level):
      ################################################
      # Load the world
      ################################################
      self.level=level
      self.mySound=None
      self.initM()
      self.initEnvironment() 
      self.initLight()
      self.gamefsm=gamefsm
      self.initKeys()
      self.disableKeys=False
      self.gameTask =taskMgr.add(self.gameLoop, "gameLoop")
      self.gameTask.last = 0 
      self.dt=0
      
      ###################################################
      # Load ODE (eg: physics) world, surface and collide
      ###################################################
      self.odeworld = OdeWorld()
      self.odespace = OdeSimpleSpace()
      self.odespace.setAutoCollideWorld(self.odeworld)
      self.odecontactgroup = OdeJointGroup()
      self.odespace.setAutoCollideJointGroup(self.odecontactgroup)
      self.odeworld.initSurfaceTable(4)
      self.IDTERRAIN= 0
      self.IDHILLS=   1
      self.IDWATER=   2
      self.IDBAR=     3
      ###################################################
      # setSurfaceEntry parameters
      #    * surfaceID1
      #    * surfaceID2
      #    * mu: This is the Coulomb friction coefficient. It means how much friction the contact has, a value of 0.0 means there will be no friction at all, while a value of OdeUtils.getInfinity() means the contact will never slip.
      #    * bounce: This is how bouncy the surface is. A value of 0.0 means it is not bouncy, a value of 1.0 gives a very bouncy surface.
      #    * bounce_vel: The minimum velocity a body must have before it bounces. If a body collides with a velocity lower than this value, it will not bounce off.
      #    * soft_erp: The error reduction parameter of the contact normal. This is used to simulate soft surfaces.
      #    * soft_cfm: The constraint force mixing parameter of the contact normal. This is used to simulate soft surfaces.
      #    * slip: The coefficient for the force-dependent slip. This makes it possible for bodies to slide past each other.
      #    * dampen: This is used to simulate a [damping] effect. 
      #####################################################
      self.odeworld.setSurfaceEntry(self.IDHILLS,   self.IDWATER, 0.01, 0, OdeUtil.getInfinity(), 0, 0, OdeUtil.getInfinity(), 0)
      self.odeworld.setSurfaceEntry(self.IDBAR,     self.IDWATER, 0.01, 0, OdeUtil.getInfinity(), 0, 0, OdeUtil.getInfinity(), 0)
      self.odeworld.setSurfaceEntry(self.IDTERRAIN, self.IDWATER, 0.1, 0, OdeUtil.getInfinity(), 0, 0, OdeUtil.getInfinity(), 0)
      
      self.WATERDIST=   0.25
      self.WATERMASK=   BitMask32(0x00000001) 
      self.HILLSMASK=   BitMask32(0x00000002)  
      self.TERRAINMASK= BitMask32(0x00000003)
      self.BARMASK=     BitMask32(0x00000004)
      boxGeom = OdeBoxGeom(self.odespace, self.XLENGTH,self.YLENGTH,self.WATERDIST)
      #boxGeom.setPosition(boxGeom.getPosition()+Point3(0,0,0.05))
      boxGeom.setCollideBits(self.WATERMASK)
      boxGeom.setCategoryBits(self.TERRAINMASK)  
      self.odespace.setSurfaceType(boxGeom,self.IDTERRAIN)            
      
      
      ###########################################
      # Panda Collision detection 
      ###########################################
      self.cTrav = CollisionTraverser()

      self.collisionHandlerQueue = CollisionHandlerQueue() 
      #Collision masks
      self.PANDAWOODYPUSHERMASK=        BitMask32(0x00000001)
      self.PANDABARMASK=                BitMask32(0x00000001) 
      self.PANDAWATERMASK=              BitMask32(0x00000001) 
      self.PANDAHILLSMASK=              BitMask32(0x00000001)
      self.PANDATREEMASK=               BitMask32(0x00000001)
      self.PANDAHOUSEMASK=              BitMask32(0x00000001)
      self.PANDAPLACEMASK=              BitMask32(0x00000002)
      self.PANDAWOODYSTDMASK=           BitMask32(0x00000002)
      
      
      ###########################################
      # arrays of text and timer and icons objects
      ########################################### 
      self.textItems=[]
      self.timerItems=[]
      self.iconItems=[]
      
      ###########################################
      # initialize items to compute overall score
      ###########################################
      self.score_from_normal=0
      self.score_from_dorothy=0
      self.score_from_mayor=0
      self.num_normal=0
      self.num_dorothy=0
      self.num_mayor=0
      self.total_score=0
      
      ###########################################
      # card for the final video
      ###########################################
      self.card=None
      
      ############################################
      # initialize items for bars count
      ###########################################
      self.owned_bars_fresh_text_displayed=OnscreenText(text='Fresh'+'\n'+'Bars:',style=3, fg=(1,0.7,0.4,1), scale = 0.065,pos=(1.25,-0.4),font=loader.loadFont('fonts/PLUMP.TTF'),mayChange=True)
      self.owned_bars_weak_text_displayed=OnscreenText(text='Weak'+'\n'+'Bars:',style=3, fg=(1,0.7,0.4,1), scale = 0.065,pos=(1.25,-0.75),font=loader.loadFont('fonts/PLUMP.TTF'),mayChange=True)
      self.textItems.append(self.owned_bars_fresh_text_displayed)
      self.textItems.append(self.owned_bars_weak_text_displayed)
      self.owned_bars_fresh=0
      self.owned_bars_weak=0
      self.owned_bars_fresh_displayed=OnscreenText(text=str(self.owned_bars_fresh),style=3, fg=(1,0.7,0.4,1), scale = 0.11,pos=(1.25,-0.6),font=loader.loadFont('fonts/PLUMP.TTF'),mayChange=True)
      self.owned_bars_weak_displayed=OnscreenText(text=str(self.owned_bars_weak),style=3, fg=(1,0.7,0.4,1), scale = 0.11,pos=(1.25,-0.95),font=loader.loadFont('fonts/PLUMP.TTF'),mayChange=True)
      self.textItems.append(self.owned_bars_fresh_displayed)
      self.textItems.append(self.owned_bars_weak_displayed)
        
      
      self.woodyfsm=self.woodyFSM(25,25,self)
      
      ##########################################
      ## put the fence at the bottom
      ##########################################
      #fence_1=loader.loadModel("models/Dam")
      #fence_1.reparentTo(self.environ)
      #fence_1.setScale(1.00)
      #self.setPos(fence_1,'N',25,0)
      
      
      ###########################################
      # FSM list contains object of the world
      # with a well defined position
      # every object in this list has to specify
      # an x,y attribute (eg: his position in the
      # world matrix) 
      # Starting from x,y also the corresponding
      # X,Y (coordinates reparented to environ)
      # must be provided
      ########################################### 
      self.FSMList=[]
      #Will be set in the level function  
      self.dam_n=0
      
      ##########################################
      # Level information
      ##########################################
      self.LASTLEVEL=2
      self.final_level=False
      #self.level=2
      #Currently two levels are present
      if self.level==self.LASTLEVEL:   self.final_level=True
      #Load the current level
      if self.level==1 :  self.loadLevel1()
      elif self.level==2: self.loadLevel2()

      ###########################################
      # the sound fsm needs to know who is the 
      # main character in order to attach 
      # 3d sound to it
      ########################################### 
      self.soundfsm=self.soundFSM(self, self.woodyfsm.woody)
      
      ###########################################
      # camera fsm
      ########################################### 
      self.camerafsm=self.cameraFSM(self, self.woodyfsm.woody)
      
      ###########################################
      # Define where woody can place the bar
      ###########################################
      self.placelist=[]
      self.updateValidPos()
      
      
    def levelCompleted(self):
        font = loader.loadFont('fonts/PLUMP.TTF')
        self.tx = OnscreenText(text="Level Completed!!!",style=3, fg=(1,0.7,0.4,1), scale = 0.12,pos=(0,0),font=font)
        self.textItems.append(self.tx)
       
        self.soundfsm.playLevelCompleted()
        
        tim=Timer(3.0,self.gamefsm.request, args=["GameOver",self.level+1])
        self.timerItems.append(tim)
        tim.start()
    
    
    def checkout(self):
        ##################################
        ##Check the end of the level
        ##################################
        self.dam_n-=1
        if(self.dam_n==0):
            self.computeScore()
            self.clearScreenfromText()
            self.x=-50
            self.countScore(0)
            
                   
    def computeScore(self):
        ###################################
        ##compute the score
        ################################### 
        for fsm in self.FSMList:
            if fsm.tag=='house' and fsm.state!='Explode':
                if (fsm.dorothy==False and fsm.mayor==False):
                    self.num_normal+=1
                    self.score_from_normal+=fsm.score
                if (fsm.dorothy==True):
                    self.num_dorothy+=1
                    self.score_from_dorothy+=fsm.score
                if (fsm.mayor==True):
                    self.num_mayor+=1
                    self.score_from_mayor+=fsm.score 

 
    def countScore(self, type):
        ######################################
        ## print the score and its components
        ######################################        
        self.x=self.x+50
        font = loader.loadFont('fonts/PLUMP.TTF')
        if (self.x>=50): 
            self.tx.destroy()
            self.soundfsm.playCash()
        if(type==0):
            self.tx = OnscreenText(text=(codecs.utf_8_encode("Normal houses:.........."+str(self.num_normal)+" x 50 = "+str(self.x))[0]), fg=(1,0.7,0.4,1), scale = 0.08, pos=(0,0.6),font=font, shadow= (0,0,0,1))
            self.textItems.append(self.tx)
            
            if(self.x < self.score_from_normal):
                
                tim=Timer(0.2,self.countScore, args=[0])
                self.timerItems.append(tim)
                tim.start()
            else: 
                self.x=-50
                self.countScore(1)
        if(type==1):
            self.tx = OnscreenText(text=(codecs.utf_8_encode("Mayor house:.........."+str(self.num_mayor)+" x 100 = "+str(self.x))[0]), fg=(1,0.7,0.4,1), scale = 0.08, pos=(0,0.3),font=font, shadow= (0,0,0,1))
            self.textItems.append(self.tx)
         
            if(self.x < self.score_from_mayor):
              
                tim=Timer(0.2,self.countScore, args=[1])
                self.timerItems.append(tim)
                tim.start()
            else: 
                self.x=-50
                self.countScore(2)
        if(type==2):
            self.tx = OnscreenText(text=(codecs.utf_8_encode("Dorothy house:.........."+str(self.num_dorothy)+" x 200 = "+str(self.x))[0]), fg=(1,0.7,0.4,1), scale = 0.08, pos=(0,0.0),font=font, shadow= (0,0,0,1))
            self.textItems.append(self.tx)
          
            if(self.x < self.score_from_dorothy):
          
                tim=Timer(0.2,self.countScore, args=[2])
            else: 
                self.x=-50
                tim=Timer(0.2,self.countScore, args=[3])
            self.timerItems.append(tim)
            tim.start()
        if(type==3):
            self.total_score=self.score_from_normal+self.score_from_mayor+self.score_from_dorothy            
            tx = OnscreenText(text=(codecs.utf_8_encode("Total Score:.........."+str(self.total_score))[0]), fg=(1,0.7,0.4,1), scale = 0.12, pos=(0,-0.5),font=font, shadow= (0,0,0,1))
            self.textItems.append(tx)
            tim=Timer(4,self.clearScreenfromText)
            self.timerItems.append(tim)
            tim.start()
            self.win_or_lose()
    
    
    def win_or_lose(self):

        self.soundfsm.request('Stop')
        if self.isCompleted():
            if(self.final_level):
                tim=Timer(5,self.playFinalVideo, args=[0])
            else:
                tim=Timer(5,self.levelCompleted, args=[])
        else:
            tim=Timer(5,self.playFinalVideo, args=[1])
        self.timerItems.append(tim)
        tim.start()
    
    
    def isCompleted(self):
        if(self.total_score>=self.score_to_win): return True
        else: return False
    
    
    def clearScreenfromText(self):
      
        self.disableKeys=True ###Disable all keys 
        for i in self.textItems:
            i.destroy()
        
        for i in self.iconItems:
            i.destroy()
          
        self.owned_bars_weak_displayed.destroy()    
        self.owned_bars_fresh_displayed.destroy()
        
      
    def playFinalVideo(self,type):

        if(type==1):
            myMovieTexture=loader.loadTexture("Video/Game_Over.avi")
            self.mySound=loader.loadSfx("Video/Game_Over.avi")
        else:
            myMovieTexture=loader.loadTexture("Video/Victory.avi")
            self.mySound=loader.loadSfx("Video/Victory.avi")
        cm = CardMaker("My Fullscreen Card");
        cm.setFrameFullscreenQuad()
        cm.setUvRange(myMovieTexture)
        self.card = NodePath(cm.generate())
        self.card.reparentTo(render2d)
        self.card.setTexture(myMovieTexture)
        myMovieTexture.synchronizeTo(self.mySound)
        self.mySound.setVolume(5)
        self.mySound.play()
        self.checkLevel()
   
    
    def checkLevel(self):
      # Every time we complete the level we update
      # the state about the current level
      if self.isCompleted(): 
          if self.level<self.LASTLEVEL:
              self.level+=1
          else:
              self.level=3
      tim=Timer(10.0,self.gamefsm.request, args=["GameOver", self.level])
      self.timerItems.append(tim)
      tim.start()           
     
              
    def gameLoop(self, task):
          #Calculate how much time has elapsed
          self.globaltime=task.time
          self.dt = task.time - task.last
          task.last = task.time
          
          #Check for collision
          self.cTrav.traverse(render)
          
          #Check if woody is near some tree or near some place where he can place the bar
          #TODO: why this cannot be cheched inside woody fsm, my personal try failed because of imprecision
          nearTree=False
          nearPlaceForBar=False
          for i in range(self.collisionHandlerQueue.getNumEntries()):
              entry = self.collisionHandlerQueue.getEntry(i) 
              if entry.getFromNode().getName() == 'WoodyStandard' and entry.getIntoNode().getName()=='Placetree': 
                  self.woodyfsm.setNearTree(True,entry.getIntoNodePath().getParent())
                  nearTree=True
              elif entry.getFromNode().getName() == 'WoodyStandard' and entry.getIntoNode().getName()=='Placebar': 
                  self.woodyfsm.setNearPlaceForBar(True,entry.getIntoNodePath().getParent())
                  nearPlaceForBar=True
          
          if(not nearTree): self.woodyfsm.setNearTree(False)
          if(not nearPlaceForBar): self.woodyfsm.setNearPlaceForBar(False)
                   
          
          return Task.cont
       
     
    class woodyFSM(FSM.FSM): 
        
        SPEEDWOODY=3
        
        def __init__(self,x,y,world):
          FSM.FSM.__init__(self,'woodyFSM')  
          
          self.world=world
          self.woody = Actor("models/Woody",
                             {"Run":"models/Woody_Run","Rest":"models/Woody_Rest"})
          self.woody.pose("Rest",5)
          self.idea=loader.loadModel("models/LightBulb/LightBulb")  
          self.woody.reparentTo(world.environ)
          self.woody.setScale(0.1)
          self.world.setPos(self.woody,'N',x,y)
          self.woody.setZ(self.woody.getZ()+0.2)
        
          
          self.nearTree=False
          self.nearPlaceForBar=False
          self.isMoving=False
          self.request('Play')
          self.gameTask = taskMgr.add(self.woodytask, "woodyTask")
        
          #Woody cannot go inside any object of the world that
          #We use panda Pusher
          self.pusher = CollisionHandlerPusher()
          cNode = CollisionNode('WoodyPusher')
          cNode.addSolid(CollisionSphere(0,0,3,1.1))
          cNode.setCollideMask(self.world.PANDAWOODYPUSHERMASK)
          self.woodyC = self.woody.attachNewNode(cNode)
          #self.woodyC.show()    
          self.world.cTrav.addCollider(self.woodyC, self.pusher)
          self.pusher.addCollider(self.woodyC,self.woody, base.drive.node())
          
          #This helps to detect interesting places for woody,
          #like nearTree and nearPlaceForBar
          cNode = CollisionNode('WoodyStandard')
          cNode.addSolid(CollisionSphere(0,0,3,1.1))
          cNode.setCollideMask(self.world.PANDAWOODYSTDMASK)
          self.woodyC = self.woody.attachNewNode(cNode)
          #self.woodyC.show()
          self.world.cTrav.addCollider(self.woodyC, self.world.collisionHandlerQueue)
        
        def movewoody(self):

            if(self.world.getKey('woodyleft')==1):
                self.woody.setH(self.woody.getH()+300*self.world.dt)
            if(self.world.getKey('woodyright')==1):
                self.woody.setH(self.woody.getH()-300*self.world.dt)
            if (self.world.getKey("woodyforward")!=0) :
                    backward = self.woody.getNetTransform().getMat().getRow3(1)
                    backward.setZ(0)
                    backward.normalize()
                    self.woody.setPos(self.woody.getPos() - backward*(self.world.dt*self.SPEEDWOODY))
                            
            if (self.world.getKey("woodyforward")!=0) or (self.world.getKey("woodyleft")!=0) or (self.world.getKey("woodyright")!=0):
                if self.isMoving is False:
                    self.woody.loop("Run")
                    self.isMoving = True
                    self.world.soundfsm.playWoodyStep()
            else:
                if self.isMoving:
                    self.woody.stop()
                    self.woody.pose("Rest",5)
                    self.isMoving = False
                    self.world.soundfsm.stopWoodyStep()
                           
        def doBar(self):
            ########################################
            # We must be sure that we are near
            # a tree. We retrieve the tree
            # and we destroy it
            # Finally update point and change state
            ########################################
            pos=self.tree.getPos(self.world.environ)
            X=pos[0]
            Y=pos[1]           
            treeFSM=self.world.getFSMInPosXY(X,Y)
            treeFSM.request('Destroy')
            self.world.soundfsm.playCrunch()
            self.world.updateValidPos()
            
            ##update the owned bars
            if (treeFSM.little):
                self.world.owned_bars_weak=self.world.owned_bars_weak+1
                self.world.owned_bars_weak_displayed.destroy()
                self.world.owned_bars_weak_displayed=OnscreenText(text=str(self.world.owned_bars_weak),style=3, fg=(1,0.7,0.4,1), scale = 0.11,pos=(1.25,-0.95),font=loader.loadFont('fonts/PLUMP.TTF'),mayChange=True)
                self.world.textItems.append(self.world.owned_bars_weak_displayed)
            else:
                self.world.owned_bars_fresh=self.world.owned_bars_fresh+1
                self.world.owned_bars_fresh_displayed.destroy()
                self.world.owned_bars_fresh_displayed=OnscreenText(text=str(self.world.owned_bars_fresh),style=3, fg=(1,0.7,0.4,1), scale = 0.11,pos=(1.25,-0.6),font=loader.loadFont('fonts/PLUMP.TTF'),mayChange=True)
                self.world.textItems.append(self.world.owned_bars_fresh_displayed)
            
            def changestate(task):
                self.request('PlayWithBar')
            if((self.world.owned_bars_weak==1 or self.world.owned_bars_fresh==1) and self.state=='Play'):
                taskMgr.doMethodLater(0.5,changestate, "woodyTask", appendTask=True)
            
                
        def isNearTree(self):
            return self.nearTree
        
        def setNearTree(self,bool,tree=None):
            self.nearTree=bool
            self.tree=tree
                                                
        def placeBar(self,type):
            ########################################
            # We must be sure that we are near
            # a place for the bar. We retrieve the 
            # position of that place in the bar fsm
            # that must be stored here thanks to 
            # world.updateValidPos()
            ########################################
            pos=self.placeforbar.getPos(self.world.environ)
            barfsm=self.world.getFSMInPosXY(pos[0],pos[1])
            self.type=type
            barfsm.createBar(self.type)    
            
            ###############################################
            # Points and change state
            ###############################################
            ##one bar has been placed
            if(self.type==0):
                self.world.owned_bars_weak=self.world.owned_bars_weak-1
                self.world.owned_bars_weak_displayed.destroy()
                self.world.owned_bars_weak_displayed=OnscreenText(text=str(self.world.owned_bars_weak),style=3, fg=(1,0.7,0.4,1), scale = 0.11,pos=(1.25,-0.95),font=loader.loadFont('fonts/PLUMP.TTF'),mayChange=True)
                self.world.textItems.append(self.world.owned_bars_weak_displayed)
                if (self.world.owned_bars_weak % 3 ==0):
                    self.icon = OnscreenImage(image = 'icons/Woody_Mad.jpg', pos = (-1.2,0,0), scale=0.15)
                if (self.world.owned_bars_weak % 3 ==1):
                    self.icon = OnscreenImage(image = 'icons/Dorothy_Happy.jpg', pos = (-1.2,0,-0.4), scale=0.15)
                if (self.world.owned_bars_weak % 3 ==2):
                    self.icon = OnscreenImage(image = 'icons/Mayor_Happy.jpg', pos = (-1.2,0,-0.8), scale=0.15)
                self.world.iconItems.append(self.icon)
                self.tim=Timer(2,self.icon.destroy)
                self.tim.start()
                self.world.timerItems.append(self.tim)
                self.world.soundfsm.playYeah()
            if(self.type==1):
                self.world.owned_bars_fresh=self.world.owned_bars_fresh-1
                self.world.owned_bars_fresh_displayed.destroy()
                self.world.owned_bars_fresh_displayed=OnscreenText(text=str(self.world.owned_bars_fresh),style=3, fg=(1,0.7,0.4,1), scale = 0.11,pos=(1.25,-0.6),font=loader.loadFont('fonts/PLUMP.TTF'),mayChange=True)
                self.world.textItems.append(self.world.owned_bars_fresh_displayed)
                if (self.world.owned_bars_fresh % 3 ==0):
                    self.icon = OnscreenImage(image = 'icons/Woody_Happy.jpg', pos = (-1.2,0,0), scale=0.15)
                if (self.world.owned_bars_fresh % 3 ==1):
                    self.icon = OnscreenImage(image = 'icons/Dorothy_Happy.jpg', pos = (-1.2,0,-0.4), scale=0.15)
                if (self.world.owned_bars_fresh % 3 ==2):
                    self.icon = OnscreenImage(image = 'icons/Mayor_Happy.jpg', pos = (-1.2,0,-0.8), scale=0.15)
                self.world.iconItems.append(self.icon)
                self.tim=Timer(2,self.icon.destroy)
                self.tim.start()
                self.world.timerItems.append(self.tim)
                self.world.soundfsm.playYuhu()
            if(self.world.owned_bars_weak==0 and self.world.owned_bars_fresh==0 ):
                self.request('Play')
            
        def isNearPlaceForBar(self):
            return self.nearPlaceForBar     
        
        def setNearPlaceForBar(self,bool,placeforbar=None):
            self.nearPlaceForBar=bool
            self.placeforbar=placeforbar
          
        def showIdea(self,big=False):
            self.idea.reparentTo(self.woody)
            if big :
                self.idea.setScale(8)
                self.idea.setZ(self.woody.getZ()+12)
            else:
                self.idea.setScale(4)
                self.idea.setZ(self.woody.getZ()+9)
        
        def hideIdea(self):
            self.idea.detachNode()
                 
        def woodytask(self,task):          
                        
           if(self.state=='Play'):
                self.movewoody()
                if self.isNearTree():
                    self.showIdea()
                    if self.world.getKey('doBar')==1 :
                        self.doBar()
                else:
                    self.hideIdea()
                     
           if self.state=='PlayWithBar':
                self.movewoody()
                if self.isNearTree() or self.isNearPlaceForBar():
                    if self.isNearTree():
                            self.showIdea()
                            if self.world.getKey('doBar')==1 :
                                 self.doBar()
                    if self.isNearPlaceForBar():  
                             self.showIdea(big=True)
                             if self.world.getKey('place_bar_weak')==1 :
                                 if(self.world.owned_bars_weak>=1):
                                     self.placeBar(0)
                             elif self.world.getKey('place_bar_fresh')==1 :
                                 if(self.world.owned_bars_fresh>=1):
                                     self.placeBar(1)  
                else: self.hideIdea()     
                
           return Task.cont
                
        
    class damFSM(FSM.FSM):
        DAMSCALE=1.35
        
        def __init__(self,x,y,timer,shoots,world, last=False):
            FSM.FSM.__init__(self,'damFSM')
            
            self.tag='dam'
            self.world=world
            self.x=x
            self.y=y
            self.timer=timer
            self.last=last
            self.water=self.world.waterFSM(world,x,y)
            self.shoots=shoots
            
            self.dam=Actor("models/Dam",{"Break":"models/Dam_Break"})
            self.dam.reparentTo(world.environ)
            self.dam.setScale(self.DAMSCALE)
            world.setPos(self.dam, 'N', x,y)
            self.X=self.dam.getX()
            self.Y=self.dam.getY()
            
            #create a collision solid for this model
            cNode = CollisionNode('dam')
            cNode.addSolid(CollisionSphere(0,0,1,2.4))
            damC = self.dam.attachNewNode(cNode)
            #damC.show()
            
            ##########################################
            # Show the count down for that Dam
            # and request explosion when it expires
            ##########################################
            def countdown(t,p):
                
                font = loader.loadFont('fonts/PLUMP.TTF') 
                self.tx.destroy()
                self.tx = OnscreenText(text=(codecs.utf_8_encode(str(t))[0]), fg=(1,0.7,0.4,1), scale = 0.08, pos=(p,0.9),font=font, shadow= (0,0,0,1))
                self.world.textItems.append(self.tx)
                t-=1
                if(t >= 0):
                    tim=Timer(1.0,countdown, args=[t,p])
                    self.world.timerItems.append(tim)
                    tim.start()
                else: 
                    self.request('Explode')   
                    self.world.soundfsm.playThunder()      
                    self.shoots-=1
                    if self.shoots>0:
                        t=timer
                        countdown(t,p)
                    else:
                        self.water.request('Completed')
            posabsmax=3.0             
            pos=-posabsmax*0.5+posabsmax*((float(x)/float(self.world.MX-1)))
            self.tx= OnscreenText(text="Start", fg=(1,0.5,0.5,1), scale = 0.1, pos=(pos,0.9) )                  
            countdown(timer,pos)

                         
        def enterExplode(self):
            
            if self.oldState=='Off':
                self.water.request('Start')
                #Explode
                self.dam.pose("Break",5)
                self.dam.reparentTo(self.world.environ)
                self.dam.setScale(self.DAMSCALE)
                self.world.setPos(self.dam, 'N', self.x,self.y)
                #Just a flag to decide when to start the music
                if self.last: 
                    self.world.soundfsm.playSoundtrack() 
            else :
                self.water.request('Start')
                   
       
    class waterFSM(FSM.FSM):
                 
            WATERSCALE=0.5
            WATERP=-90
            
            
            def __init__(self, world, x, y):
                FSM.FSM.__init__(self,'avatarFSM')
                
                self.tag='water'
                self.world=world
                self.x=x
                self.y=y
                
                self.waterhead=loader.loadModel("models/Tube")
                #self.waterhead.setH(self.waterhead.getH()-90)
                self.waterhead.setR(self.waterhead.getR()+90)
                self.waterhead.setScale(0.15, 0.15, 0.15)
                self.waterhead.reparentTo(self.world.environ)
                wtex=loader.loadTexture("models/water/Water02.jpg")
                self.waterhead.setTexture(wtex)
                
                self.water=loader.loadModel("models/plane")
                wtex=loader.loadTexture("img/water.png")
                self.water.setTexture(wtex)
                self.water.setScale(self.WATERSCALE)
                self.water.setP(self.WATERP)
                world.setPos(self.water, 'N', x,y)
                self.X=self.water.getX()
                self.Y=self.water.getY()
                
                #ODE body list for water particles
                self.bodylist=[]
                
                #fix light: temporary fix to see blue water
                ambient = AmbientLight('ambient')
                ambient.setColor(Vec4(1,1,1,1))
                ambientNP = self.water.attachNewNode(ambient.upcastToPandaNode())
                self.water.setLightOff()
                self.water.setLight(ambientNP)
                
                ################################
                # We immediatly starts the 
                # physic simulation tasks
                # Enter state will generate
                # the particles
                ################################
                taskMgr.add(self.simulationTask, "waterTask", appendTask=True)
                self.finishflag=False
                
            def enterStart(self):
                ##############################
                # Entering in the start
                # state is equivalent to
                # generate one particle of
                # water
                ##############################
                self.genWater()
                
            def genWater(self):
                ###################################################
                # Load water with physics
                ###################################################
                # Setup the geometry
                waterNP = self.water.copyTo(self.world.environ)
                waterHead = self.waterhead.copyTo(self.world.environ)
                waterNP.setPos(self.X, self.Y, self.world.WATERDIST) 
                # Create the body and set the mass
                boxBody = OdeBody(self.world.odeworld)
                M = OdeMass()
                M.setSphere(10, 1.0)
                boxBody.setMass(M)
                boxBody.setPosition(waterNP.getPos(self.world.environ))
                boxBody.setQuaternion(waterNP.getQuat(self.world.environ))
                boxBody.setForce(random.uniform(-1,1)*50, 0, 0)
                # Create a SphereGeom for the water
                boxGeom = OdeSphereGeom(self.world.odespace, 0.1)
                boxGeom.setCollideBits(self.world.HILLSMASK)
                boxGeom.setCategoryBits(self.world.WATERMASK)
                boxGeom.setBody(boxBody)  
                self.world.odespace.setSurfaceType(boxGeom,self.world.IDWATER) 
                
                self.bodylist.append((waterNP, boxBody, waterHead))
                
            def vanishWater(self,water):   
                water.removeNode()
                return Task.done          
             
            def simulationTask(self,task):
                ###################################################
                # Water class finish his work when the bodylist
                # is empty (eg: no water in the environment)
                # and when his state is 'Completed' (eg: the 
                # corresponding dam will not request more water
                # with genwater()
                ###################################################
                if len(self.bodylist)==0 and self.state=='Completed' and not self.finishflag:
                    self.finishflag=True
                    self.world.checkout()
                    #return task.done
                
                ###################################################
                # Physic collision
                ###################################################
                # Setup the contact joints
                self.world.odespace.autoCollide() 
                # Step the simulation and set the new positions
                self.world.odeworld.quickStep(globalClock.getDt())
                
                YCOLLPAR=0.8
                XCOLLPAR=0.8
                XCOLLPARBAR=0.8
                YCOLLPARBAR=0.8
                #From physics bullet update water position  
                for np, body, head in self.bodylist:
                    if math.fabs(body.getPosition()[1])>self.world.getLastY() or math.fabs(body.getPosition()[0])>self.world.getLastX():
                            np.removeNode()
                            head.removeNode()
                            body.destroy()
                            self.bodylist.remove((np,body,head))  
                    else:    
                            newWater = self.water.copyTo(self.world.environ)
                            newWater.setPosQuat(self.world.environ, body.getPosition(), self.water.getQuat(render))
                            taskMgr.doMethodLater(5, self.vanishWater, 'waterTask', extraArgs=[newWater])

                            if body.getLinearVel()[1]!=0:
                                dx=body.getLinearVel()[0]
                                dy=body.getLinearVel()[1]*-1
                                angle=math.degrees(math.atan(dx/dy))
                            newWater.setH(angle)
                            head.setH(angle)
                            head.setPos(newWater.getPos())
                            head.setZ(head.getZ()-0.05)
                            head.setY(head.getY()-0.1)
                            head.setP(head.getP()+2)
                            
                            
                            for fsm in self.world.FSMList :
                                if abs(newWater.getPos(self.world.environ)[0]-fsm.X) < XCOLLPAR and abs(newWater.getPos(self.world.environ)[1]-fsm.Y) < YCOLLPAR and fsm.tag=='house' :
                                    fsm.request('Explode')
                                    fsm.exploded=True
                                if abs(newWater.getPos(self.world.environ)[0]-fsm.X) < XCOLLPAR*2 and abs(newWater.getPos(self.world.environ)[1]-fsm.Y) < YCOLLPAR*2 and fsm.tag=='house' and fsm.mayor :
                                    fsm.request('Explode')
                                    fsm.exploded=True
                                if abs(newWater.getPos(self.world.environ)[0]-fsm.X) < XCOLLPARBAR and abs(newWater.getPos(self.world.environ)[1]-fsm.Y) < YCOLLPARBAR and fsm.tag=='bar':
                                    fsm.checkExplode()
                            
                            #create a collision solid for this model
                            cNode = CollisionNode('Water')
                            cNode.addSolid(CollisionSphere(0,0,0,1))
                            cNode.setCollideMask(self.world.PANDAWATERMASK)
                            waterC = newWater.attachNewNode(cNode)
                            #waterC.show() 
                            
                self.world.odecontactgroup.empty() # Clear the contact joints
                return task.cont
      
      
    class treeFSM(FSM.FSM):
      
      TREESCALE=0.35
      TREESCALE_little=0.12
      
      def __init__(self,x,y,world,little=False):
        FSM.FSM.__init__(self,'treeFSM')
        
        self.tag='tree'    
        self.world=world
        self.x=x
        self.y=y
        self.little=little
      
        if (self.little==True):
            self.tree=loader.loadModel("models/GroomedTree/GroomedTree")
            self.tree.reparentTo(world.environ)
            self.tree.setScale(self.TREESCALE_little)
            self.CreateShadow(self.tree,0.3)    
        else:
            self.tree=loader.loadModel("models/Tree")
            self.tree.reparentTo(world.environ)
            self.tree.setScale(self.TREESCALE)
            self.CreateShadow(self.tree,0.4)    
        
        
        world.setPos(self.tree,'T',x,y)
        self.X=self.tree.getX()
        self.Y=self.tree.getY()
        
        #Woody cannot go inside a tree (pusher)
        cNode = CollisionNode('Tree')
        cNode.addSolid(CollisionSphere(0,0,3,2))
        cNode.setCollideMask(self.world.PANDATREEMASK)
        treeC = self.tree.attachNewNode(cNode)
        #treeC.show()
        
        #Woody must detect when he is near a tree (collisionhandlerqueue)
        self.cPlaceNode = CollisionNode('Placetree')
        self.cPlaceNode.addSolid(CollisionSphere(0,0,5,4))
        self.cPlaceNode.setCollideMask(self.world.PANDAPLACEMASK)
        treeC = self.tree.attachNewNode(self.cPlaceNode)
        #treeC.show()

      def CreateShadow(self,np,z_scale):
         
         sh=np.copyTo(self.world.environ)
         sh.reparentTo(np)
         sh.setX(np.getX()+0.3)
         sh.setScale(1,1,z_scale)
         
         sh.setTransparency(TransparencyAttrib.MAlpha)     
         sh.setColor(0,0,0,.4)   
         return sh         
    
      def enterDestroy (self):
          self.tree.detachNode()
          self.world.setPos(self.tree, 'N', self.x, self.y)
          
      def clearPlaceNode (self):
          self.cPlaceNode.clearSolids()
          
          
    class hillFSM(FSM.FSM):
        
      HILLSCALE=0.35
     
       
      def __init__(self,x,y,world):  
        FSM.FSM.__init__(self,'hillFSM')
        
        self.tag='hill'    
        self.world=world
        self.x=x
        self.y=y
      
        self.hill=loader.loadModel("models/Rock")        
        self.hill.reparentTo(world.environ)                
        self.hill.setScale(self.HILLSCALE)
        self.CreateShadow(self.hill)
        
        world.setPos(self.hill,'H',x,y)
        self.X=self.hill.getX()
        self.Y=self.hill.getY()
        
        #create a collision solid for this model
        cNode = CollisionNode('Hill')
        cNode.addSolid(CollisionSphere(0.7,0,1,2.6))
        cNode.setCollideMask(self.world.PANDAHILLSMASK)
        hillC = self.hill.attachNewNode(cNode)
        #hillC.show()
        
        ###############################################
        # Physics ODE collision node
        ###############################################
        pNode=loader.loadModel("models/plane")
        pNode.reparentTo(self.world.environ)
        pNode.setHpr(-45,0,0)
        pNode.hide()
        hillGeom = OdeBoxGeom(self.world.odespace, 1,1,1)
        hillGeom.setCollideBits(self.world.WATERMASK)
        hillGeom.setCategoryBits(self.world.HILLSMASK)
        hillGeom.setPosition(self.hill.getPos(self.world.environ)+Point3(0,0,self.world.WATERDIST))
        hillGeom.setQuaternion(pNode.getQuat(self.world.environ))
        self.world.odespace.setSurfaceType(hillGeom,self.world.IDHILLS) 
        
      def CreateShadow(self,np):
         sh = np.getParent().attachNewNode("shadow")
         sh.setScale(1,1,.3)
         
         sh.setTransparency(TransparencyAttrib.MAlpha)     
         sh.setColor(0,0,0,.4)
         np.instanceTo(sh)   
         return sh         
    
    
    class barFSM(FSM.FSM):
           
      def __init__(self,x,y,world,orientation,tree1=None,tree2=None):  
        FSM.FSM.__init__(self,'barFSM')
        
        self.tag='bar'    
        self.world=world
        self.x=x
        self.y=y
        self.orientation=orientation
        self.pNode=loader.loadModel("models/plane")
        self.pNode.reparentTo(self.world.environ)
        if self.orientation=='left': orientation=45
        else: orientation=-45  
        self.pNode.setHpr(orientation,0,90)
        self.pNode.hide()
        self.world.setPos(self.pNode,'N',x,y)
        self.X=self.pNode.getX()
        self.Y=self.pNode.getY()
        self.tree1=tree1
        self.tree2=tree2 
        #ODE geometry to detach 
        self.barGeom=None
    
      def clearTree(self):
          if self.tree1!=None: self.tree1.clearPlaceNode()
          if self.tree2!=None: self.tree2.clearPlaceNode() 
          
      def createBar(self,type):
          #########################################
          # When a bar is created every
          # adiacent tree is disabled 
          # (eg: cannot be taken
          #########################################
          self.clearTree()
          self.type=type
          #########################################
          # Load tha panda model 
          # and his Panda collision detection
          #########################################
          if self.type==1:
              self.bar= Actor("models/WoodBlock_Fresh",{"Break":"models/WoodBlock_FreshBreak"})
          else:
              self.bar= Actor("models/WoodBlock_Weak",{"Break":"models/WoodBlock_WeakBreak"})
          self.bar.reparentTo(self.world.environ)
          self.bar.setScale(1.6)
          self.bar.setX(self.X)
          self.bar.setY(self.Y)
          if self.orientation=='left': self.bar.setH(self.bar.getH()+135)
          else: self.bar.setH(self.bar.getH()+45) 
          #create a collision solid for this model
          cNode = CollisionNode('Bar')
          cNode.addSolid(CollisionSphere(0,0,0,0.5))
          cNode.setCollideMask(self.world.PANDABARMASK)
          barC = self.bar.attachNewNode(cNode)
          #barC.show()          
          self.world.updateValidPos()
          
          ###############################################
          # Physics ODE collision node
          ###############################################
          barGeom = OdeCylinderGeom(self.world.odespace, 0.5, 2)
          barGeom.setCollideBits(self.world.WATERMASK)
          barGeom.setCategoryBits(self.world.BARMASK)
          barGeom.setPosition(self.pNode.getPos()+Point3(0,0,self.world.WATERDIST))
          barGeom.setQuaternion(self.pNode.getQuat(self.world.environ))
          self.world.odespace.setSurfaceType(barGeom,self.world.IDBAR)
          self.barGeom=barGeom
          self.request('Created')
          
      def checkExplode(self):
          if self.state=='Created' and self.type==0:
              self.request('Explode')     
          
      def enterExplode(self):
            self.bar.pose("Break",5)
            taskMgr.doMethodLater(1, self.detach, "waterTask", extraArgs=[], appendTask=True)
      
      def detach(self,task):
            self.bar.detachNode()
            self.barGeom.disable()
            self.barGeom.destroy()
        
        
    class houseFSM(FSM.FSM):
        
      HOUSESCALE=0.3
      H_MAYORSCALE=0.2
      H_DOROTHYSCALE=0.3
        
      def __init__(self,x,y,world,mayor=False,dorothy=False):  
        FSM.FSM.__init__(self,'houseFSM')
        
        self.tag='house'    
        self.world=world
        self.x=x
        self.y=y
        self.mayor=mayor
        self.dorothy=dorothy
        self.exploded=False
        
        
        if(self.mayor==False and self.dorothy==False):
            self.house=Actor("models/cabin/Cabin",{"Break":"models/cabin/Cabin_Break"})
            self.house.reparentTo(world.environ)
            self.house.setScale(self.HOUSESCALE)
            cNode = CollisionNode('House')
            cNode.addSolid(CollisionSphere(0,1,0,4.3))
            cNode.setCollideMask(self.world.PANDAHOUSEMASK)
            houseC = self.house.attachNewNode(cNode)
            self.score=50
        if(self.mayor==True):
            self.house=Actor("models/cabin/CabinMayor",{"Break":"models/cabin/CabinMayor_Break"})
            self.house.reparentTo(world.environ)
            self.house.setScale(self.H_MAYORSCALE)
            cNode = CollisionNode('House')
            cNode.addSolid(CollisionSphere(0,1,0,12))
            cNode.setCollideMask(self.world.PANDAHOUSEMASK)
            houseC = self.house.attachNewNode(cNode)
            self.score=100
        if(self.dorothy==True):
            self.house=Actor("models/cabin/CabinDorothy",{"Break":"models/cabin/CabinDorothy_Break"})
            self.house.reparentTo(world.environ)
            self.house.setScale(self.H_DOROTHYSCALE)
            cNode = CollisionNode('House')
            cNode.addSolid(CollisionSphere(0,1,0,6))
            cNode.setCollideMask(self.world.PANDAHOUSEMASK)
            houseC = self.house.attachNewNode(cNode)
            self.score=200
            
        self.CreateShadow(self.house)        
        world.setPos(self.house,'House',x,y)

        self.X=self.house.getX()
        self.Y=self.house.getY()
        
        #houseC.show()      
      def CreateShadow(self,np):
         sh = np.getParent().attachNewNode("shadow")
         sh.setScale(1,1,.3)
         sh.setX (0.4+np.getX())
         sh.setY (0.1+np.getY())
         sh.setTransparency(TransparencyAttrib.MAlpha)     
         sh.setColor(0,0,0,.4)
         np.instanceTo(sh)   
         return sh         
    
      def enterExplode(self):
        if(self.exploded==False):
            self.house.pose("Break",5)  
            if (self.dorothy==True):
                self.icon = OnscreenImage(image = 'icons/Dorothy_Sad.jpg', pos = (-1.2,0,-0.4), scale=0.15)
                self.world.iconItems.append(self.icon)
                self.tim=Timer(2,self.icon.destroy)
                self.tim.start()
                self.world.timerItems.append(self.tim)
                self.world.soundfsm.playAhh()
            elif (self.mayor==True):
                self.icon = OnscreenImage(image = 'icons/Mayor_Sad.jpg', pos = (-1.2,0,-0.8), scale=0.15)
                self.world.iconItems.append(self.icon)
                self.tim=Timer(2,self.icon.destroy)
                self.tim.start()
                self.world.timerItems.append(self.tim)
                self.world.soundfsm.playDoh()
            else:
                self.icon = OnscreenImage(image = 'icons/Woody_Sad.jpg', pos = (-1.2,0,0), scale=0.15)
                self.world.iconItems.append(self.icon)
                self.tim=Timer(2,self.icon.destroy)
                self.tim.start()
                self.world.timerItems.append(self.tim)                                                                                
                self.world.soundfsm.playOh_no()
            self.exploded=True
            self.world.setPos(self.house, 'N', self.x,self.y)
            self.world
            
    
#    class villagerFSM(FSM.FSM): 
#        
#        SPEEDVILLAGER=3
#        
#        def __init__(self,x,y,villager_type,house,world):
#          FSM.FSM.__init__(self,'villagerFSM')  
#          
#          self.house=house
#          self.world=world
#          if(villager_type==1):
#              self.villager = Actor("models/villager/Villager01",
#                             {"Run":"models/villager/Villager_Run","Rest":"models/villager/Villager_Rest",
#                              "Cower":"models/villager/Villager_Cower","Shake":"models/villager/Villager_Shake",
#                              "Stand":"models/villager/Villager_Stand"})
#          if(villager_type==2):
#              self.villager = Actor("models/villager/Villager02",
#                             {"Run":"models/villager/Villager_Run","Rest":"models/villager/Villager_Rest",
#                              "Cower":"models/villager/Villager_Cower","Shake":"models/villager/Villager_Shake",
#                              "Stand":"models/villager/Villager_Stand"}) 
#          if(villager_type==3):
#              self.villager = Actor("models/villager/Villager03",
#                             {"Run":"models/villager/Villager_Run","Rest":"models/villager/Villager_Rest",
#                              "Cower":"models/villager/Villager_Cower","Shake":"models/villager/Villager_Shake",
#                              "Stand":"models/villager/Villager_Stand"})  
#                 
#          self.villager.setScale(0.1)
#          self.world.setPos(self.villager,'N',x,y)
#          self.villager.setZ(self.villager.getZ()+0.2)
#          self.request('None')
#          self.gameTask = taskMgr.add(self.villagertask, "villagerTask")
#          #villagerInterval1= self.villager.posInterval(13,Point3(0,-10,0), startPos=Point3(0,10,0))
#          #villagerInterval2= self.villager.posInterval(13,Point3(0,10,0), startPos=Point3(0,-10,0))
#          #self.villagerPace = Sequence(villagerInterval1, villagerInterval2, name = "villagerRun")    
#          
#            
#        def villagertask(self,task):
#         
#          if(self.state=='None'):
#              True
#              
#          if(self.state=='Attach'):
#              self.villager.reparentTo(self.world.environ)
#              self.request('Stand')
#              #self.request('Run')
#          
#          #if(self.state=='Run'):
#              #self.villagerPace.loop()
#              #self.villager.loop("Run")
#          
#          if(self.state=='Cow'):
#              self.villager.play("Cower")
#              self.request('Shake')
#          
#          if(self.state=='Shake'):
#              if(self.villager.getAnimControl("Cower").isPlaying()==False):
#                self.villager.loop("Shake")
#                self.request("Stay_shaked")
#          
#          if(self.state=='Stay_shaked'):
#            True
#          
#          if(self.state=='Exploded'):
#              self.villager.stop()
#              self.villager.play("Stand")
#              self.request("Stand")
#          
#          if(self.state=='Stand'):
#              if(self.villager.getAnimControl("Stand").isPlaying()==False):
#                  self.villager.loop("Rest")
#            
#          return Task.cont
#                
                
    class soundFSM(FSM.FSM):
        
        ##############################################################
        # Two states are provided
        #     On : you can play the sounds with the provided functions
        #     Stop: all the sounds are stopped
        ##############################################################
        
        SOUNDTRACKVOLUME=10
        WOODYSTEPVOLUME=5
        POINTS_VOLUME=15
        CRUNCH_WOODY_VOLUME=0.5
        OH_NO_WOODY_VOLUME=1
        YEAH_WOODY_VOLUME=1
        YUHU_WOODY_VOLUME=1
        LEVEL_COMPLETED_VOLUME=15
        DOH_VOLUME=1
        AHH_VOLUME=1
        def __init__(self,world,woody):
            FSM.FSM.__init__(self,'soundFSM')
            
            self.world=world
            
            self.soundtrack = loader.loadSfx("sounds/soundtrack.mp3")
            self.thunder = loader.loadSfx("sounds/thunder.wav")
            #sounds regarding characters sounds
            self.crunch=loader.loadSfx("sounds/crunch.wav")
            self.oh_no = loader.loadSfx("sounds/oh_no.wav")
            self.yeah = loader.loadSfx("sounds/yeah2.wav")
            self.yuhu = loader.loadSfx("sounds/yuhu.wav")
            self.ahh = loader.loadSfx("sounds/ahh2.wav")
            self.doh = loader.loadSfx("sounds/doh2.wav")
            
            #point sound
            self.cash= loader.loadSfx("sounds/cash_register.wav")
            
            #level completed
            self.level_completed= loader.loadSfx("sounds/level_completed.wav")

            self.soundtrack.setLoop(1)
            self.soundtrack.setVolume(self.SOUNDTRACKVOLUME)
            
            audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], camera)
            self.footstep = audio3d.loadSfx('sounds/grass2.wav')
            audio3d.attachSoundToObject( self.footstep, woody )

            base.cTrav = CollisionTraverser() 
            # Enable Audio
            base.enableAllAudio()
            # loop sounds
            audio3d.setSoundVelocityAuto(self.footstep)
            audio3d.setListenerVelocityAuto()
            
            self.request('On')
            
        def playSoundtrack(self):
            if self.state=='On':
                self.soundtrack.play()
            
        def playThunder(self):
            if self.state=='On':
                self.thunder.play()
            
        def playWoodyStep(self):
            if self.state=='On':
                self.footstep.setVolume(self.WOODYSTEPVOLUME)
                self.footstep.setLoop(5)
                self.footstep.play()
            
        def stopWoodyStep(self):
            self.footstep.stop()      
            
        def enterStop(self): 
            self.soundtrack.stop()
            self.thunder.stop()
            self.footstep.stop()
            self.oh_no.stop()
            self.yeah.stop()
            self.yuhu.stop()
            self.cash.stop()
            self.ahh.stop()
            self.doh.stop()
            self.crunch.stop()
        

        def playCrunch(self):
             if self.state=='On':
                self.crunch.setVolume(self.CRUNCH_WOODY_VOLUME)                
                self.crunch.play()      
            
        def playOh_no(self):
            if self.state=='On':
                self.oh_no.setVolume(self.OH_NO_WOODY_VOLUME)                
                self.oh_no.play()      
        
        def playYeah(self):
            if self.state=='On':
                self.yeah.setVolume(self.YEAH_WOODY_VOLUME)                
                self.yeah.play()

        def playYuhu(self):
            if self.state=='On':
                self.yuhu.setVolume(self.YUHU_WOODY_VOLUME)                
                self.yuhu.play()
        def playAhh(self):
            if self.state=='On':
                self.ahh.setVolume(self.AHH_VOLUME)                
                self.ahh.play()       
        
                
        def playDoh(self):
            if self.state=='On':
                self.doh.setVolume(self.DOH_VOLUME)                
                self.doh.play()          
        
        def playCash(self):
            if self.state=='On':
                self.cash.setVolume(self.POINTS_VOLUME)                
                self.cash.play()       
        
        def playLevelCompleted(self):
           
                self.level_completed.setVolume(self.LEVEL_COMPLETED_VOLUME)                
                self.level_completed.play()                  
           
                                          
    class cameraFSM(FSM.FSM):
        
      def __init__(self,world,woody):  
        FSM.FSM.__init__(self,'cameraFSM')
            
        self.world=world
        self.woody=woody
        base.disableMouse()
        camera.reparentTo(self.world.environ)
        #input is too fast, we need to slow it down
        self.ignoreinput=False
        
        taskMgr.add(self.controlCamera, "cameraTask")
        self.request('WoodyCamera')
        
      def controlCamera(self,task):
          if self.world.getKey('changeview')==1:
              if self.state=='WoodyCamera':
                  self.request('OverviewCamera')
              else:
                  self.request('WoodyCamera')
                  
          if(self.state=='WoodyCamera'):
            self.woodyCamera()
          if(self.state=='OverviewCamera'):
            self.overviewCamera()
            
          return Task.cont  
      
      def woodyCamera(self):
          camera.lookAt(self.woody)
          camera.setY(self.woody.getY()-7)
          camera.setZ(self.woody.getZ()+3)        
          
      def overviewCamera(self):
         camera.setZ(15)
         camera.setY(-27)
         camera.lookAt(self.world.environ)
            
         if(self.world.getKey('camerafar')==1):
            camera.setY(camera.getY()-1)
         if(self.world.getKey('cameradeep')==1):
            camera.setY(camera.getY()+1)
         if(self.world.getKey('cameraHleft')==1):
            camera.setH(camera.getH()+1)
         if(self.world.getKey('cameraHright')==1):
            camera.setH(camera.getH()-1) 
         if(self.world.getKey('cameraleft')==1):
            camera.setX(camera.getX()-1)
         if(self.world.getKey('cameraright')==1):
            camera.setX(camera.getX()+1) 
         if(self.world.getKey('cameraup')==1):
            camera.setZ(camera.getZ()+1) 
         if(self.world.getKey('cameradown')==1):
            camera.setZ(camera.getZ()-1) 
         if(self.world.getKey('camerapitchup')==1):
            camera.setP(camera.getP()+1) 
         if(self.world.getKey('camerapitchdown')==1):
            camera.setP(camera.getP()-1)
             