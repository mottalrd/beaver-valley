import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import FontPool
import codecs 
from threading import Timer
import sys
from direct.gui.DirectFrame import DirectFrame

class Intro(DirectObject):
    
    def enter(self,myfsm):
        
        self.soundtrack = loader.loadSfx("sounds/daydreaming.wav")
        self.soundtrack.play()
        font = loader.loadFont('fonts/PLUMP.TTF')
        base.setBackgroundColor(0,0,0)
        self.items=[]
        self.logo = OnscreenImage(image = 'img/Logo.png', pos = (0,0,0.1), scale=0.65)
        self.tx = OnscreenText(text=(codecs.utf_8_encode("presents")[0]), fg=(1,1,1,1), scale = 0.05, pos=(0,-0.1),font=font, shadow= (0,0,0,1))  
        self.items.append(self.logo)
        self.items.append(self.tx)

        def showIntro():
            for i in self.items:
                i.destroy()
            self.soundtrack.stop()    
            base.setBackgroundColor(0,0,0)
            self.logo = OnscreenImage(image = 'models/StartScreen.jpg', pos = (0,0,0), scale=1)
            self.tx = OnscreenText(text=(codecs.utf_8_encode("s=start game")[0]), fg=(0.76,0.21,0,02), scale = 0.07, pos=(-0.6,-0.75),font=font, shadow= (0,0,0,1))
            self.tx2 = OnscreenText(text=(codecs.utf_8_encode("esc=exit")[0]), fg=(0.76,0.21,0,02), scale = 0.07, pos=(-0.6,-0.9),font=font, shadow= (0,0,0,1))
            self.items.append(self.logo)
            self.items.append(self.tx)
            self.items.append(self.tx2)
            self.soundtrack = loader.loadSfx("sounds/solo_ritmato.mp3")
            self.soundtrack.setLoop(1)
            self.soundtrack.play()
            self.accept("escape", sys.exit)
            self.accept("s", self.Instructions, [myfsm, 1])
            
        self.tim=Timer(4,showIntro)
        self.tim.start()
    
    
    def Instructions(self,myfsm, page):
        base.setBackgroundColor(0,0,0)
        for i in self.items:
            i.destroy()
        self.logo = OnscreenImage(image = 'models/BG_Screen01.jpg', pos = (0,0,0), scale=1.5)
        font = loader.loadFont('fonts/PLUMP.TTF')
        self.accept("s", myfsm.request, ["Game", 1])
        self.accept("escape", sys.exit)
        
        if(page==1):
            self.accept("n", self.Instructions, [myfsm, page+1])
            self.tx = OnscreenText(text=(codecs.utf_8_encode("You are the carpenter beaver")[0]), fg=(1,0.7,0.4,1), scale = 0.08, pos=(0,0.65),font=font, shadow= (0,0,0,1))
            self.tx1= OnscreenText(text=(codecs.utf_8_encode("Woody")[0]), fg=(1,0.7,0.4,1), scale = 0.1, pos=(0,0.45),font=font, shadow= (0,0,0,1))
            self.tx2 = OnscreenText(text=(codecs.utf_8_encode("Your mission is to deflect the water coming"+"\n"+ "from dams upstream the village")[0]), fg=(1,0.7,0.4,1), scale = 0.07, pos=(0,-0.5),font=font, shadow= (0,0,0,1))
            self.logo2= OnscreenImage(image = 'icons/Woody_Happy.jpg', pos = (0,0.0,0), scale=0.35)
            self.tx3 = OnscreenText(text=(codecs.utf_8_encode("N: next - S: start game - ESC: Exit")[0]), fg=(0.76,0.21,0,02), scale = 0.065, pos=(0,-0.87),font=font, shadow= (0,0,0,1))
            self.items.append(self.tx2)
            self.items.append(self.tx3)
            
        if(page==2):
            self.accept("n", self.Instructions, [myfsm, page+1])
            self.accept("p", self.Instructions, [myfsm, page-1])
            self.tx = OnscreenText(text=(codecs.utf_8_encode("You can use two kind of bars to protect the village")[0]), fg=(1,0.7,0.4,1), scale = 0.065, pos=(0,0.85),font=font, shadow= (0,0,0,1))
            self.tx1= OnscreenText(text=(codecs.utf_8_encode("Weak bars: they break after deflecting"+"\n"+" a single chunk of water "+"\n"+"\n"+"\n"+
                                                             "Get them from weak trees"+"\n"+"\n"+"\n"+"\n"+
                                                             "Fresh bars: they are very resistant and never break"+"\n"+"\n"+"\n"+
                                                             "Get them from fresh trees"+"\n"+"\n"+"\n"+"\n"+
                                                             "Commands:"+"\n"+
                                                             "Move around: arrow keys, Get a bar: spacebar"+"\n"+
                                                             "Place a weak bar: s, Place a fresh bar: d"+"\n"+"Change view: Enter")[0]), fg=(1,0.7,0.4,1), scale = 0.065, pos=(0,0.63),font=font, shadow= (0,0,0,1))
            self.tx2 = OnscreenText(text=(codecs.utf_8_encode("N: next - P: previous - S: start game - ESC: Exit")[0]), fg=(0.76,0.21,0,02), scale = 0.065, pos=(0,-0.87),font=font, shadow= (0,0,0,1))
            self.logo2= OnscreenImage(image = 'models/tree1.png', pos = (-0.9,0,0.35), scale=0.14)
            self.logo3= OnscreenImage(image = 'models/tree2.png', pos = (-0.9,0.0,-0.18), scale=0.14)
            self.items.append(self.logo3)
            self.items.append(self.tx2)
            
        if(page==3):
            self.accept("n", self.Instructions, [myfsm, page+1])
            self.accept("p", self.Instructions, [myfsm, page-1])
            self.tx = OnscreenText(text=(codecs.utf_8_encode("When you can place a bar or take a tree,"+"\n"+"\n"+"a bulb appears above Woody     "+"\n"+"\n"+
                                                             "You can place a bar between:")[0]), fg=(1,0.7,0.4,1), scale = 0.065, pos=(0,0.9),font=font, shadow= (0,0,0,1))
            self.tx1= OnscreenText(text=(codecs.utf_8_encode("1. Two trees, whatever kind"+"\n"+"\n"+"\n"+"\n"+
                                                             "2. One tree and one rock"+"\n"+"\n"+"\n"+"\n"+
                                                             "3. Two rocks"+"\n"+"\n"+"\n"+
                                                             "Commands:"+"\n"+
                                                             "Move around: arrow keys, Get a bar: spacebar"+"\n"+
                                                             "Place a weak bar: s, Place a fresh bar: d"+"\n"+"Change view: Enter")[0]), fg=(1,0.7,0.4,1), scale = 0.07, pos=(0,0.38),font=font, shadow= (0,0,0,1))
            self.tx2 = OnscreenText(text=(codecs.utf_8_encode("N: next - P: previous - S: start game - ESC: Exit")[0]), fg=(0.76,0.21,0,02), scale = 0.065, pos=(0,-0.87),font=font, shadow= (0,0,0,1))
            self.logo2= OnscreenImage(image = 'models/tree1.png', pos = (-1,0,0.4), scale=0.14)
            self.logo3= OnscreenImage(image = 'models/tree2.png', pos = (1,0.0,0.4), scale=0.14)
            self.logo4= OnscreenImage(image = 'img/bulb.png', pos = (0.9,0,0.78), scale=0.08)
            self.logo5= OnscreenImage(image = 'img/rock.png', pos = (-1,0.0,-0.25), scale=0.14)
            self.logo6= OnscreenImage(image = 'img/rock.png', pos = (1,0.0,-0.25), scale=0.14)
            self.logo7= OnscreenImage(image = 'models/tree1.png', pos = (-1,0.0,0.07), scale=0.14)
            self.logo8= OnscreenImage(image = 'img/rock.png', pos = (1,0.0,0.07), scale=0.14)
            #self.logo3= OnscreenImage(image = 'models/rock.png', pos = (-0.9,0,0.3), scale=0.14)
            self.items.append(self.logo3)
            self.items.append(self.logo4)
            self.items.append(self.logo5)
            self.items.append(self.logo6)
            self.items.append(self.logo7)
            self.items.append(self.logo8)
            self.items.append(self.tx2)
            
        if(page==4):
            self.accept("p", self.Instructions, [myfsm, page-1])
            ###########################################
            # score to be reached to win
            ###########################################
            self.score_to_win=400
            self.logo2= OnscreenImage(image = 'models/Normal.png', pos = (-1.25,0,0.3), scale=0.115)
            self.logo3= OnscreenImage(image = 'models/mayor.png', pos = (-1.25,0.0,0), scale=0.115)
            self.logo4= OnscreenImage(image = 'models/Dorothy.png', pos = (-1.25,0,-0.3), scale=0.115)
            self.tx = OnscreenText(text=(codecs.utf_8_encode("To complete this level you must get "+"\n"+str(self.score_to_win)+" points")[0]), fg=(1,0.7,0.4,1), scale = 0.09, pos=(0,0.7),font=font, shadow= (0,0,0,1))
            self.tx1= OnscreenText(text=(codecs.utf_8_encode("One normal house gives you 50 points"+"\n"+"\n"+"\n"+"\n"+
                                                       "The mayor house gives you 100 points"+"\n"+"\n"+"\n"+"\n"+
                                                       "The Dorothy house gives you 200 points"+"\n"+"\n"+"\n"+"\n")[0]), fg=(1,0.7,0.4,1), scale = 0.07, pos=(0,0.3),font=font, shadow= (0,0,0,1))
            self.tx2 = OnscreenText(text=(codecs.utf_8_encode("PLEASE WOODY, SAVE THE VILLAGE!!!")[0]), fg=(1,0.7,0.4,1), scale = 0.1, pos=(0,-0.65),font=font, shadow= (0,0,0,1))
            self.tx3 = OnscreenText(text=(codecs.utf_8_encode("S: start game - P: previous - ESC: Exit")[0]), fg=(0.76,0.21,0,02), scale = 0.065, pos=(0,-0.87),font=font, shadow= (0,0,0,1))
            self.items.append(self.tx2)
            self.items.append(self.tx3)
            self.items.append(self.logo3)
            self.items.append(self.logo4)
        
        self.items.append(self.tx)
        self.items.append(self.tx1)
        self.items.append(self.logo)
        self.items.append(self.logo2)
        
        

    def exit(self):
        self.soundtrack.stop()
        for i in self.items:
                i.destroy()
        self.tim.cancel()
        base.setBackgroundColor(0,0,0)
        self.ignoreAll()