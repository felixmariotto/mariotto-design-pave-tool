
import Rhino
import scriptcontext as sc
from imp import reload
import obj

reload(obj)

#

origin = Rhino.Geometry.Point3d(0,0,0)

class Gem(obj.Object3D):
    
    def __init__(self, diameter, defID):
        super(Gem, self).__init__()
        self.diameter = diameter
        self.defID = defID
        instanceMatrix = Rhino.Geometry.Transform.Scale(origin, diameter)
        self.instanceID = sc.doc.Objects.AddInstanceObject(defID, instanceMatrix)
    
    def getInstance(self):
        return sc.doc.Objects.FindId( self.instanceID )
    
    def move(self, newPos, newNorm):
        # translation
        translationVec = newPos - self.position
        transform = Rhino.Geometry.Transform.Translation(translationVec)
        self.copyPosition(newPos)
        # rotation
        startVec = self.normal
        rotTransform = Rhino.Geometry.Transform.Rotation(startVec, newNorm, newPos)
        self.copyNormal(newNorm)
        # apply
        transform = rotTransform * transform
        sc.doc.Objects.Transform(self.instanceID, transform, True)
    
    def setNewDiameter(self, diameter):
        ratio = diameter / self.diameter
        self.diameter = diameter
        scaleMatrix = Rhino.Geometry.Transform.Scale(self.position, ratio)
        sc.doc.Objects.Transform(self.instanceID, scaleMatrix, True)
    
    def dispose(self):
        sc.doc.Objects.Remove(self.getInstance())
