
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
        self.onIncrease.append( self.handleAddedGemIncrease )
        self.onDecrease.append( self.handleAddedGemDecrease )
        self.currentGemDiameter = 1.0
    
    def handleAddedGemIncrease(self):
        self.currentGemDiameter += 0.1
        print( self.currentGemDiameter )
    
    def handleAddedGemDecrease(self):
        self.currentGemDiameter -= 0.1
        print( self.currentGemDiameter )
    
    def addGem(self):
        try:
            # create a new gem
            self.gemInstance = self.gemfactory.makeInstance(self.surf)
            return True
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