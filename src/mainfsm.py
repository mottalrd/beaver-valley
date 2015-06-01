from direct.fsm import FSM
from world import World
from intro import Intro
from gameover import GameOver 

class GameFSM(FSM.FSM):
    
    def enterIntro(self):
        introworld.enter(self)
        
    def exitIntro(self):
        introworld.exit()
        
    def enterGame(self, level):
        gameworld.enter(self, level)
        
    def exitGame(self):
        gameworld.exit()
           
    def enterGameOver(self, level):
        gameoverworld.enter(self,level)
        
    def exitGameOver(self):
        gameoverworld.exit()

       
introworld=Intro()
gameworld=World()
gameoverworld=GameOver()

myfsm = GameFSM('gameFSM')
myfsm.request('Intro')
      

run()  