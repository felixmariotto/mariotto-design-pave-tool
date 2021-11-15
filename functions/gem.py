
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
    
    def dispose(self):
        print('delete this instance')
