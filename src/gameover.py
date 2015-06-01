import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
import sys
from pandac.PandaModules import FontPool
import codecs 

class GameOver(DirectObject):  
           
    def enter(self,myfsm, level):
        self.level=level
        self.items=[]
        font = loader.loadFont('fonts/PLUMP.TTF')
        base.setBackgroundColor(0,0,0)
        self.logo = OnscreenImage(image = 'models/StartScreen.jpg', pos = (0,0,0), scale=1)
       
        if (level==1):
            #base.setBackgroundColor(1,1,1)
            #self.logo = OnscreenImage(image = 'img/Woody01.jpg', pos = (0,0,0.22), scale=0.8)
            #self.title = OnscreenText(text=(codecs.utf_8_encode("GAME OVER - i=intro, g=game, esc=exit")[0]),fg=(0.76,0.21,0,02),
                    #scale = 0.07, pos=(0,-0.8),font=font, shadow= (0,0,0,1))
            self.tx = OnscreenText(text=(codecs.utf_8_encode("Level 1")[0]), fg=(0.76,0.21,0,02), scale = 0.09, pos=(-0.57,-0.58),font=font, shadow= (0,0,0,1))
            self.tx2 = OnscreenText(text=(codecs.utf_8_encode("i: intro")[0]), fg=(0.76,0.21,0,02), scale = 0.07, pos=(-0.57,-0.7),font=font, shadow= (0,0,0,1))
            self.tx3 = OnscreenText(text=(codecs.utf_8_encode("s: Restart game")[0]), fg=(0.76,0.21,0,02), scale = 0.07, pos=(-0.57,-0.8),font=font, shadow= (0,0,0,1))
            self.tx4 = OnscreenText(text=(codecs.utf_8_encode("esc: exit")[0]), fg=(0.76,0.21,0,02), scale = 0.07, pos=(-0.57,-0.9),font=font, shadow= (0,0,0,1))
            self.accept("s", myfsm.request, ["Game",level])
        if (level==2):
            self.tx = OnscreenText(text=(codecs.utf_8_encode("Level 2")[0]), fg=(0.76,0.21,0,02), scale = 0.09, pos=(-0.57,-0.58),font=font, shadow= (0,0,0,1))
            self.tx2 = OnscreenText(text=(codecs.utf_8_encode("i: intro")[0]), fg=(0.76,0.21,0,02), scale = 0.07, pos=(-0.57,-0.7),font=font, shadow= (0,0,0,1))
            self.tx3 = OnscreenText(text=(codecs.utf_8_encode("s: start game")[0]), fg=(0.76,0.21,0,02), scale = 0.07, pos=(-0.57,-0.8),font=font, shadow= (0,0,0,1))
            self.tx4 = OnscreenText(text=(codecs.utf_8_encode("esc: exit")[0]), fg=(0.76,0.21,0,02), scale = 0.07, pos=(-0.57,-0.9),font=font, shadow= (0,0,0,1))
            self.accept("s", self.Instructions, [myfsm])
        if (level==3):
            self.tx = OnscreenText(text=(codecs.utf_8_encode("Game"+"\n"+"Completed")[0]), fg=(0.76,0.21,0,02), scale = 0.09, pos=(-0.63,-0.48),font=font, shadow= (0,0,0,1))
            self.tx2 = OnscreenText(text=(codecs.utf_8_encode("i: intro")[0]), fg=(0.76,0.21,0,02), scale = 0.07, pos=(-0.63,-0.7),font=font, shadow= (0,0,0,1))
            self.tx3 = OnscreenText(text=(codecs.utf_8_encode("c: Credits")[0]), fg=(0.76,0.21,0,02), scale = 0.07, pos=(-0.63,-0.8),font=font, shadow= (0,0,0,1))
            self.tx4 = OnscreenText(text=(codecs.utf_8_encode("esc: exit")[0]), fg=(0.76,0.21,0,02), scale = 0.07, pos=(-0.63,-0.9),font=font, shadow= (0,0,0,1))
            self.accept("c", self.Credits, [myfsm])
        
        self.items.append(self.tx)
        self.items.append(self.tx2)
        self.items.append(self.tx3)
        self.items.append(self.tx4)
        self.items.append(self.logo)
        self.accept("escape", sys.exit)
        self.accept("i", myfsm.request, ["Intro"])
    
    
    def Instructions(self,myfsm):
        self.score_to_win=500
        base.setBackgroundColor(0,0,0)
        for i in self.items:
            i.destroy()
        self.logo = OnscreenImage(image = 'models/BG_Screen01.jpg', pos = (0,0,0), scale=1.5)
        font = loader.loadFont('fonts/PLUMP.TTF')
        self.accept("s", myfsm.request, ["Game", self.level])
        self.accept("escape", sys.exit)
        self.logo2= OnscreenImage(image = 'models/Normal.png', pos = (-1.25,0,0.3), scale=0.115)
        self.logo3= OnscreenImage(image = 'models/mayor.png', pos = (-1.25,0.0,0), scale=0.115)
        self.logo4= OnscreenImage(image = 'models/Dorothy.png', pos = (-1.25,0,-0.3), scale=0.115)
        self.tx = OnscreenText(text=(codecs.utf_8_encode("To complete this level you must get "+"\n"+str(self.score_to_win)+" points")[0]), fg=(1,0.7,0.4,1), scale = 0.09, pos=(0,0.7),font=font, shadow= (0,0,0,1))
        self.tx1= OnscreenText(text=(codecs.utf_8_encode("One normal house gives you 50 points"+"\n"+"\n"+"\n"+"\n"+
                                                       "The mayor house gives you 100 points"+"\n"+"\n"+"\n"+"\n"+
                                                       "The Dorothy house gives you 200 points"+"\n"+"\n"+"\n"+"\n")[0]), fg=(1,0.7,0.4,1), scale = 0.07, pos=(0,0.3),font=font, shadow= (0,0,0,1))
        self.tx2 = OnscreenText(text=(codecs.utf_8_encode("PLEASE WOODY, SAVE THE VILLAGE!!!")[0]), fg=(1,0.7,0.4,1), scale = 0.1, pos=(0,-0.65),font=font, shadow= (0,0,0,1))
        self.tx3 = OnscreenText(text=(codecs.utf_8_encode("S: start game - P: previous - ESC: Exit")[0]), fg=(0.76,0.21,0,02), scale = 0.065, pos=(0,-0.87),font=font, shadow= (0,0,0,1))
        self.items.append(self.tx)
        self.items.append(self.tx2)
        self.items.append(self.tx3)
        self.items.append(self.tx1)
        self.items.append(self.logo)
        self.items.append(self.logo2)
        self.items.append(self.logo3)
        self.items.append(self.logo4)
        
    def Credits(self,myfsm):
        base.setBackgroundColor(0,0,0)
        for i in self.items:
            i.destroy()
        font = loader.loadFont('fonts/PLUMP.TTF')
        self.accept("i", myfsm.request, ["Intro"])
        self.accept("escape", sys.exit)
        self.tx = OnscreenText(text=(codecs.utf_8_encode("Credits")[0]), fg=(1,1,1,1), scale = 0.1, pos=(0,0.85),font=font, shadow= (0,0,0,1))
        self.tx1= OnscreenText(text=(codecs.utf_8_encode("Gameplay Designer and Developer"+"\n"+"\n"+
                                                       "Andrea Tommaso Bonanno"+"\n"+"\n"+"\n"+
                                                       "Physics Implementation"+"\n"+"\n"+
                                                       "Alfredo Motta"+"\n"+"\n"+"\n"+
                                                       "Sound effects and developer"+"\n"+"\n"+
                                                       "Valerio Panzica La Manna"+"\n"+"\n"+"\n"+
                                                       "Art"+"\n"+"\n"+
                                                       "Ephraim Zev Zimmerman")[0]), fg=(1,1,1,1), scale = 0.07, pos=(0,0.64),font=font, shadow= (0,0,0,1))

        self.tx2 = OnscreenText(text=(codecs.utf_8_encode("I: Intro - ESC: Exit")[0]), fg=(0.76,0.21,0,02), scale = 0.065, pos=(0,-0.9),font=font, shadow= (0,0,0,1))
        self.items.append(self.tx)
        self.items.append(self.tx1)
        self.items.append(self.tx2)
            
    def exit(self):
        base.setBackgroundColor(0.2,0.75,1)
        for i in self.items:
            i.destroy()
        self.ignoreAll()  