
"""
Module responsible for adding gems to the pave, according to user input.
"""

import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs
import gemfactory
from imp import reload

reload(gemfactory)

#

class c:
    
    def __init__(self):
        self.gemfactory = gemfactory.GemFactory(self)
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
            self.gemInstance = self.gemfactory.makeGem(self.brepBase, self.currentGemDiameter)
            self.writeData() # from notes.py module
            return self.gemInstance
        except Exception, e:
            print(e)
    
    def addGems(self):
        # get the brep on which to position the gem
        go = Rhino.Input.Custom.GetObject()
        go.SetCommandPrompt('select the polysurface on which to orient a gem')
        go.GeometryFilter = Rhino.DocObjects.ObjectType.Brep
        go.Get()
        obj_ref = go.Object(0)
        geom = obj_ref.Geometry()
        if isinstance(geom, Rhino.Geometry.BrepFace):
            brep = geom.Brep
        else:
            brep = geom
        self.brepBase = brep
        
        # add gems until the user presses Escape
        while self.addGem():
            pass
        else:
            pass
            # do something when all gems have been positioned