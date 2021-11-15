
import Rhino
import scriptcontext as sc
from imp import reload
import gembrep
import gem
reload(gembrep)
reload(gem)

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
    
    def dynamicDrawCallback(self, sender, args):
        try:
            # rotate
            res = self.surf.ClosestPoint( args.CurrentPoint )
            norm = self.surf.NormalAt(res[1], res[2])
            print( norm )
            
            # translate
            self.lastGem.moveAt(args.CurrentPoint)
            sc.doc.Views.Redraw()
        except Exception, e:
            print(e)
    
    def moveGem(self, gem):
        pass
    
    def makeGem(self, surface=None):
        self.lastGem = gem.Gem(1, self.idef_index)
        self.surf = surface
        
        gp = Rhino.Input.Custom.GetPoint()
        gp.DynamicDraw += self.dynamicDrawCallback
        if surface:
            gp.Constrain(surface, False)
        gp.PermitObjectSnap(False)
        gp.Get()
        # If the last instance positioning was cancelled, we delete this instance
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            self.lastGem.dispose()
            return False
        else:
            return self.lastGem
