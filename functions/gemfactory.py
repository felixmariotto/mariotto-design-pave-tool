
import Rhino
import scriptcontext as sc
from random import random
from imp import reload
import obj
import gembrep

reload(obj)
reload(gembrep)

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
        
        # Create the gem object
        brep = gembrep.GemBrep(0.5)
        brepID = sc.doc.Objects.AddBrep(brep)
        ref = Rhino.DocObjects.ObjRef(brepID)
        geometry = ref.Object().Geometry
        attributes = ref.Object().Attributes
        
        # Add the instance definition
        self.idef_index = sc.doc.InstanceDefinitions.Add(self.name, "", origin, brep, attributes)
        
        # delete source object
        sc.doc.Objects.Remove( ref.Object() )
    
    def makeInstance(self):
        xform = Rhino.Geometry.Transform.Identity
        sc.doc.Objects.AddInstanceObject(self.idef_index, xform)
        sc.doc.Views.Redraw()

gemF = GemFactory( 'foo' )
gemF.makeInstance()

"""
def callback(sender, args):
    print( args.CurrentPoint )

gp = Rhino.Input.Custom.GetPoint()
gp.DynamicDraw += callback
gp.Get()
"""