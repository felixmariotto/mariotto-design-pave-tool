
import Rhino
import scriptcontext as sc
from random import random
from imp import reload
import obj

reload(obj)

class Gem(obj.Object3D):
    
    group = sc.doc.Groups.Add()
    
    def __init__(self, radius=1):
        super(Gem, self).__init__()
        self.radius = radius
        # self.name = 'gem ' + str( int( random() * 10e10 ) )
        self.group = sc.doc.Groups.Add()
        self.makeGeometry()
    
    def makeGeometry(self):
        cylinder = self.Cylinder()
        cylinder.SetUserString( 'foo', '42' )
        # print( cylinder.GetUserString('foo') )
        cylinderID = sc.doc.Objects.AddBrep(cylinder)
    
    def updateGeometry(self):
        sc.doc.Views.Redraw()
    
    def Cylinder(self):
        plane = Rhino.Geometry.Plane(self.position, self.normal)
        circle = Rhino.Geometry.Circle(plane, self.radius)
        cylinder = Rhino.Geometry.Cylinder(circle, 1)
        return cylinder.ToBrep(True, True)

gem1 = Gem()
gem2 = Gem()
gem1.position.X = 15
print( gem2.position.X )