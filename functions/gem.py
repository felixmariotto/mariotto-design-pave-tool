
import Rhino
import scriptcontext as sc
from imp import reload
import obj

reload(obj)

#

identityMatrix = Rhino.Geometry.Transform.Identity

class Gem(obj.Object3D):
    
    def __init__(self, radius, defID):
        super(Gem, self).__init__()
        self.radius = radius
        self.defID = defID
        self.instanceID = sc.doc.Objects.AddInstanceObject(defID, identityMatrix)
    
    def getInstance(self):
        return sc.doc.Objects.FindId( self.instanceID )
    
    def moveAt(self, point3d):
        translationVec = point3d - self.position
        transform = Rhino.Geometry.Transform.Translation(translationVec)
        self.copyPosition(point3d)
        sc.doc.Objects.Transform(self.instanceID, transform, True)

"""
import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs
from random import random
from imp import reload
import obj
import gembrep

reload(obj)
reload(gembrep)

class Gem(obj.Object3D):
    
    def __init__(self, radius=1):
        super(Gem, self).__init__()
        self.radius = radius
        # self.name = 'gem ' + str( int( random() * 10e10 ) )
        self.groupID = sc.doc.Groups.Add()
        self.objects = []
        self.makeContent()
    
    def makeContent(self):
        self.objects.append( self.Cylinder() )
        sc.doc.Views.Redraw()
    
    def updateContent(self):
        for object in self.objects:
            if object['isCylinder']:
                self.updateCylinder(object)
        #
        sc.doc.Views.Redraw()
    
    def dispose(self):
        print('dispose gem')
    
    def setPosition(self, x, y, z):
        obj.Object3D.setPosition(self, x, y, z)
        self.updateContent()
    
    def copyPosition(self, point):
        obj.Object3D.copyPosition(self, point)
        self.updateContent()
    
    def setNormal(self, x, y, z):
        obj.Object3D.setNormal(self, x, y, z)
        self.updateContent()
    
    def copyNormal(self, vector):
        obj.Object3D.copyNormal(self, vector)
        self.updateContent()
    
    def Cylinder(self):
        #brep
        brep = gembrep.GemBrep(self.radius, True)
        brepID = sc.doc.Objects.AddBrep(brep)
        sc.doc.Groups.AddToGroup(self.groupID, brepID)
        #object3D
        object3D = obj.Object3D()
        object3D.copyPosition( self.position )
        object3D.copyNormal( self.normal )
        #dic
        objectDic = {
            'brep': brep,
            'object3D': object3D,
            'brepID': brepID,
            'isCylinder': True
        }
        return objectDic
    
    def updateCylinder(self, object):
        # translation
        posdiff = self.position - object['object3D'].position
        translation = Rhino.Geometry.Transform.Translation(posdiff)
        object['brepID'] = sc.doc.Objects.Transform(object['brepID'], translation, True)
        object['object3D'].position.Transform(translation)
        # rotation
        rotation = Rhino.Geometry.Transform.Rotation(object['object3D'].normal, self.normal, self.position)
        object['brepID'] = sc.doc.Objects.Transform(object['brepID'], rotation, True)
        object['object3D'].copyNormal(self.normal)

#

# Block base point
base_point = Rhino.Geometry.Point3d(0, 0, 0)

# Block definition name
idef_name = "my-def"

# See if block name already exists
existing_idef = sc.doc.InstanceDefinitions.Find(idef_name, True)
if existing_idef:
    print "Block definition", idef_name, "already exists"

# Create the gem object
brep = gembrep.GemBrep(0.5)
brepID = sc.doc.Objects.AddBrep(brep)
ref = Rhino.DocObjects.ObjRef(brepID)
geometry = ref.Object().Geometry
attributes = ref.Object().Attributes

# Add the instance definition
idef_index = sc.doc.InstanceDefinitions.Add(idef_name, "", base_point, geometry, attributes)
xform = Rhino.Geometry.Transform(10.0)
sc.doc.Objects.AddInstanceObject(idef_index, xform)

if idef_index<0:
    print "Unable to create block definition", idef_name

sc.doc.Views.Redraw()
"""