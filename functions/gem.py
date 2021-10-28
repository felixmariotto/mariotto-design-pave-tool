
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
        plane = Rhino.Geometry.Plane(self.position, self.normal)
        circle = Rhino.Geometry.Circle(plane, self.radius)
        brep = Rhino.Geometry.Cylinder(circle, 1).ToBrep(True, True)
        brepID = sc.doc.Objects.AddBrep(brep)
        sc.doc.Groups.AddToGroup(self.groupID, brepID)
        print( sc.doc.Groups.GroupObjectCount(self.groupID) )
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

brep = gembrep.GemBrep()
sc.doc.Objects.AddBrep(brep)
sc.doc.Views.Redraw()
