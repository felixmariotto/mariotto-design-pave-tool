
import Rhino
import scriptcontext as sc
from random import random

awesome_gem_count = 0

class Gem(object):
    
    def __init__(self, radius=1):
        self.position = Rhino.Geometry.Point3d(0,0,0)
        self.normal = Rhino.Geometry.Vector3d(0,0,1)
        self.radius = radius
        self.name = 'gem ' + str( int( random() * 10e10 ) )
        self.group = sc.doc.Groups.Add(  )
        print( self.name )
    
    def setPosition( self, x, y, z ):
        self.position.X = x
        self.position.Y = y
        self.position.Z = z
    
    def setNormal( self, x, y, z ):
        self.normal.X = x
        self.normal.Y = y
        self.normal.Z = z
        self.normal.Unitize()
    
    def draw(self):
        cylinder = self.Cylinder()
        cylinderID = sc.doc.Objects.AddBrep(cylinder)
        sc.doc.Views.Redraw()
    
    def Cylinder(self):
        plane = Rhino.Geometry.Plane(self.position, self.normal)
        circle = Rhino.Geometry.Circle(plane, self.radius)
        cylinder = Rhino.Geometry.Cylinder(circle, 1)
        return cylinder.ToBrep(True, True)

gem = Gem( 5 )
gem.setPosition( 0, 20, 0 )
gem.setNormal( -1, -1, 0 )
gem.draw()