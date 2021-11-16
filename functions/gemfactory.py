
import Rhino
import scriptcontext as sc
from imp import reload
import gembrep
import gem
reload(gembrep)
reload(gem)
import datetime

# Block base point
origin = Rhino.Geometry.Point3d(0, 0, 0)

###
class GemFactory:
    
    def __init__(self, name):
        
        self.name = "awesome_gem - " + name
        
        # See if block name already exists
        existing_idef = sc.doc.InstanceDefinitions.Find(self.name, True)
        if existing_idef:
            print "Block definition", self.name, "already exists"
        
        # Create the gem instance definition
        brep = gembrep.GemBrep(0.5)
        attributes = sc.doc.CreateDefaultAttributes()
        self.idef_index = sc.doc.InstanceDefinitions.Add(self.name, "", origin, brep, attributes)
    
    def setGemDiameter(self, diameter):
        if self.currentGem:
            self.currentGem.setNewDiameter( diameter )
    
    def moveGem(self, gem):
        
        def dynamicDrawCallback(sender, args):
            try:
                closestFace = getClosestFace(self.brepBase.Faces, args.CurrentPoint)
                res = closestFace.ClosestPoint(args.CurrentPoint)
                norm = closestFace.NormalAt(res[1], res[2])
                gem.move(args.CurrentPoint, norm)
                sc.doc.Views.Redraw()
            except Exception, e:
                print(e)
        
        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt('Click on the polysurface to add a gem. Press SHIFT to increase and CTRL to decrease the size.')
        gp.DynamicDraw += dynamicDrawCallback
        if self.brepBase:
            gp.Constrain(self.brepBase, -1, -1, False)
        gp.PermitObjectSnap(False)
        gp.Get()
        return gp.CommandResult() == Rhino.Commands.Result.Success
    
    def makeGem(self, brepBase=None, diameter=1):
        self.lastGem = gem.Gem(diameter, self.idef_index)
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