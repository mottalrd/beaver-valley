import direct.directbase.DirectStart
from direct.task import Task
from pandac.PandaModules import *
from direct.actor import Actor
import math

#Load the first environment model
environ = loader.loadModel("models/Background")
environ.reparentTo(render)


run()
