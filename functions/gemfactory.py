
import Rhino
from System.Drawing import Color
import scriptcontext as sc
from imp import reload
import gem
reload(gem)

###
class GemFactory:
    
    def __init__(self, gemadder):
        self.gemadder = gemadder
        
    def setGemDiameter(self, diameter):
        if self.currentGem:
            self.currentGem.setNewDiameter( diameter )
    
    def moveGem(self, gem):
        
        def dynamicGemMoveCallback(sender, args):
            try:
                closestFace = getClosestFace(self.brepBase.Faces, args.CurrentPoint)
                res = closestFace.ClosestPoint(args.CurrentPoint)
                norm = closestFace.NormalAt(res[1], res[2])
                gem.move(args.CurrentPoint, norm)
                sc.doc.Views.Redraw()
            except Exception, e:
                print(e)
        
        def dynamicGemTextCallback(sender, args):
            xform = args.Viewport.GetTransform(CS.World, CS.Screen)
            current_point = args.CurrentPoint
            current_point.Transform(xform)
            screen_point = Rhino.Geometry.Point2d(current_point.X, current_point.Y)
            msg = "screen {0}, {1}".format(screen_point.X, screen_point.Y)
            args.Display.Draw2dText(msg, Color.Blue, screen_point, False)
        
        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt('Click on the polysurface to add a gem. Press SHIFT to increase and CTRL to decrease the size.')
        
        gp.DynamicDraw += dynamicGemMoveCallback
        gp.DynamicDraw += dynamicGemTextCallback
        
        if self.brepBase:
            gp.Constrain(self.brepBase, -1, -1, False)
            
        gp.PermitObjectSnap(False) # quickfix: the selection would snap on the gem brep itself otherwise, a workaround must be found to enable object snap.
        gp.Get()
        
        return gp.CommandResult() == Rhino.Commands.Result.Success
    
    def makeGem(self, brepBase=None, diameter=1):
        self.lastGem = gem.Gem(diameter, self.gemadder.idef_index)
        self.currentGem = self.lastGem
        self.brepBase = brepBase
        
        # If the last instance positioning was cancelled, we delete this instance
        rs = self.moveGem(self.lastGem)
        self.currentGem = None
        if rs:
            return self.lastGem
        else:
            self.lastGem.dispose()
            return False

def getClosestFace(facesEnum, point3d):
    closestFace = None
    closestDist = float('inf')
    for face in facesEnum:
        res = face.ClosestPoint( point3d )
        closestPoint = face.PointAt(res[1], res[2])
        dist = point3d.DistanceTo(closestPoint)
        if dist < closestDist:
            closestDist = dist
            closestFace = face
    return closestFace