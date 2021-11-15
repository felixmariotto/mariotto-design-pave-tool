
import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs
import gemfactory
from imp import reload

reload(gemfactory)

#

class c:
    
    def __init__(self):
        self.gemfactory = gemfactory.GemFactory('test_name')
        self.onIncrease.append( self.handleGemIncrease )
        self.onDecrease.append( self.handleGemDecrease )
        self.currentGemDiameter = 1.0
    
    def handleGemIncrease(self):
        self.currentGemDiameter += 0.1
        self.gemfactory.setGemDiameter(self.currentGemDiameter)
    
    def handleGemDecrease(self):
        self.currentGemDiameter -= 0.1
        self.gemfactory.setGemDiameter(self.currentGemDiameter)
    
    def addGem(self):
        try:
            # create a new gem
            self.gemInstance = self.gemfactory.makeGem(self.surf, self.currentGemDiameter)
            return self.gemInstance
        except Exception, e:
            print(e)
    
    def addGems(self):
        # get the surface on which to position the gem
        go = Rhino.Input.Custom.GetObject()
        go.SetCommandPrompt('select the surface on which to orient a gem')
        go.GeometryFilter = Rhino.DocObjects.ObjectType.Surface
        go.Get()
        if go.CommandResult() != Rhino.Commands.Result.Success:
            return
        obj_ref = go.Object(0)
        self.surf = obj_ref.Geometry().Surfaces[0]
        
        # add gems until the user presses Escape
        while self.addGem():
            pass
        else:
            pass
            # do something when all gems have been positioned