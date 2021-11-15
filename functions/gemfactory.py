
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
ot = Rhino.DocObjects.Tables.ObjectTable

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
            instance = sc.doc.Objects.FindId( self.last_instance_ID )
            currentPos = Rhino.Geometry.Point3d(
                instance.InstanceXform.M03,
                instance.InstanceXform.M13,
                instance.InstanceXform.M23
            )
            print( currentPos )
            sc.doc.Views.Redraw()
        except Exception, e:
            print(e)
    
    def makeInstance(self):
        vector = Rhino.Geometry.Vector3d(2,3,4)
        xform = Rhino.Geometry.Transform.Translation(vector)
        self.last_instance_ID = sc.doc.Objects.AddInstanceObject(self.idef_index, xform)
        
        gp = Rhino.Input.Custom.GetPoint()
        gp.DynamicDraw += self.dynamicDrawCallback
        gp.Get()

gemF = GemFactory( 'foo' )
gemF.makeInstance()
