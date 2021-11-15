
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
    
    def moveGem(self, gem):
        
        def dynamicDrawCallback(sender, args):
            try:
                res = self.surf.ClosestPoint( args.CurrentPoint )
                norm = self.surf.NormalAt(res[1], res[2]) * -1
                gem.move(args.CurrentPoint, norm)
                sc.doc.Views.Redraw()
            except Exception, e:
                print(e)
        
        gp = Rhino.Input.Custom.GetPoint()
        gp.DynamicDraw += dynamicDrawCallback
        if self.surf:
            gp.Constrain(self.surf, False)
        gp.PermitObjectSnap(False)
        gp.Get()
        return gp.CommandResult() == Rhino.Commands.Result.Success
    
    def makeGem(self, surface=None):
        self.lastGem = gem.Gem(1, self.idef_index)
        self.surf = surface
        
        # If the last instance positioning was cancelled, we delete this instance
        if self.moveGem(self.lastGem):
            return self.lastGem
        else:
            self.lastGem.dispose()
            return False
