
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
        self.allowDiamUpdate = False
    
    def handleGemIncrease(self):
        if self.allowDiamUpdate :
            self.currentGemDiameter += 0.1
            self.gemfactory.setGemDiameter(self.currentGemDiameter)
    
    def handleGemDecrease(self):
        if self.allowDiamUpdate :
            self.currentGemDiameter -= 0.1
            self.gemfactory.setGemDiameter(self.currentGemDiameter)
    
    def addGem(self):
        try:
            # create a new gem
            self.gemInstance = self.gemfactory.makeGem(self.baseObject, self.currentGemDiameter)
            self.writeData() # from notes.py module
            return self.gemInstance
        except Exception, e:
            print(e)
    
    def addGems(self):
        # get the object on which to position the gem
        go = Rhino.Input.Custom.GetObject()
        go.GeometryFilter = Rhino.DocObjects.ObjectType.Surface | Rhino.DocObjects.ObjectType.Mesh
        go.SetCommandPrompt('select the object on which to place gems')
        go.Get()
        
        if go.CommandResult() != Rhino.Commands.Result.Success: return
        
        obj_ref = go.Object(0)
        geom = obj_ref.Geometry()
        
        # set baseObject depending on user's pick
        if isinstance(geom, Rhino.Geometry.BrepFace):
            self.baseObject = geom.Brep
        elif isinstance(geom, Rhino.Geometry.Brep):
            self.baseObject = geom
        elif isinstance(geom, Rhino.Geometry.Mesh):
            self.baseObject = geom
        #elif isinstance(geom, Rhino.Geometry.SubDFace):
        #    self.baseObject = geom.ParentSubD
        #elif isinstance(geom, Rhino.Geometry.SubD):
        #    self.baseObject = geom
        
        if not self.baseObject: return
        
        # allow the user to change the next diameter diameter
        self.allowDiamUpdate = True
        
        # add gems until the user presses Escape
        while self.addGem():
            pass
        # do something when all gems have been positioned
        else:
            self.allowDiamUpdate = False
            