
import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs

import gem

from imp import reload

reload(gem)

class c:
    
    def __init__(self):
        self.gem_center = Rhino.Geometry.Point3d(0, 0, 0)
        self.up = Rhino.Geometry.Vector3d(0, 0, 1)
        self.onIncrease.append( self.handleAddedGemIncrease )
        self.onDecrease.append( self.handleAddedGemDecrease )
        self.currentGemDiameter = 1.0
    
    def handleAddedGemIncrease(self):
        self.currentGemDiameter += 0.1
        print( self.currentGemDiameter )
    
    def handleAddedGemDecrease(self):
        self.currentGemDiameter -= 0.1
        print( self.currentGemDiameter )
    
    # dynamic redraw callback, to update the position of the gem
    # while the user moves the cursor on the surface.
    def callback(self, sender, args):
        try:
            # translate the gem
            translation = args.CurrentPoint - self.gem_center
            
            self.gem_center.X = args.CurrentPoint.X
            self.gem_center.Y = args.CurrentPoint.Y
            self.gem_center.Z = args.CurrentPoint.Z
            
            self.g.copyPosition( self.gem_center )
            
            # rotate the gem
            res = self.surf.ClosestPoint( args.CurrentPoint )
            norm = self.surf.NormalAt(res[1], res[2])
            
            self.g.copyNormal( norm )
            
            self.up.X = norm.X
            self.up.Y = norm.Y
            self.up.Z = norm.Z
            
        except Exception, e:
            print(e)
    
    def addGem(self):
        try:
            # reset the circle position that will be updated in the callback
            self.gem_center.X = 0
            self.gem_center.Y = 0
            self.gem_center.Z = 0
            
            # reset the circle up vector, which will be updated in the callback
            self.up.X = 0
            self.up.Y = 0
            self.up.Z = 1
            
            # create a new gem
            self.g = gem.Gem(self.currentGemDiameter * 0.5)
            
            #
            gp = Rhino.Input.Custom.GetPoint()
            gp.Constrain(self.surf, False)
            gp.PermitObjectSnap(False)
            gp.DynamicDraw += self.callback
            gp.Get()
            if gp.CommandResult() != Rhino.Commands.Result.Success:
                self.g.dispose()
                # return false so that the endless loop of circle positioning is terminated
                return False
            else :
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