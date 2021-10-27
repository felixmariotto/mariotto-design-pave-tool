
# This class is an object containing position and direction information.
# It is used as parent class of Gem, and used internally for all the gem's
# components (surfaces, curves...)


import Rhino

class Object3D(object):
    
    def __init__(self):
        self.position = Rhino.Geometry.Point3d(0,0,0)
        self.normal = Rhino.Geometry.Vector3d(0,0,1)
    
    def setPosition( self, x, y, z ):
        self.position.X = x
        self.position.Y = y
        self.position.Z = z
    
    def setNormal( self, x, y, z ):
        self.normal.X = x
        self.normal.Y = y
        self.normal.Z = z
        self.normal.Unitize()
    
    def copyPosition( self, point ):
        self.position.X = point.X
        self.position.Y = point.Y
        self.position.Z = point.Z
    
    def copyNormal( self, vector ):
        self.normal.X = vector.X
        self.normal.Y = vector.Y
        self.normal.Z = vector.Z
        self.normal.Unitize()
