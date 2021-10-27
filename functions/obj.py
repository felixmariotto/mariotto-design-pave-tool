
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
