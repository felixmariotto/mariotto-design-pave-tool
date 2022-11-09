
import Rhino
from System.Drawing import Color
import Rhino.DocObjects.CoordinateSystem as CS
import scriptcontext as sc
from imp import reload
import gem
reload(gem)

###
class GemFactory:
    
    def __init__(self, gemadder):
        self.gemadder = gemadder
        
    def setGemDiameter(self, diameter):
        if self.currentGem:
            self.currentGem.setNewDiameter( diameter )
    
    def moveGem(self, gem):
        
        # every frame move the gem where the cursor is pointing and orient it towards the normal
        def dynamicGemMoveCallback(sender, args):
            try:
                # get the normal at the cursor position, depending on the base object's type
                if isinstance(self.baseObject, Rhino.Geometry.Brep):
                    closestFace = getClosestFace(self.baseObject.Faces, args.CurrentPoint)
                    uv = closestFace.ClosestPoint(args.CurrentPoint)
                    norm = closestFace.NormalAt(uv[1], uv[2])
                elif isinstance(self.baseObject, Rhino.Geometry.Mesh):
                    meshPoint = self.baseObject.ClosestMeshPoint(args.CurrentPoint, 0.0) # MeshPoint is a special class in Rhino
                    meshPoint.Mesh.FaceNormals.ComputeFaceNormals()
                    norm = meshPoint.Mesh.FaceNormals.Item[meshPoint.FaceIndex]
                # transform the gem
                gem.move(args.CurrentPoint, norm)
                sc.doc.Views.Redraw()
            except Exception, e:
                print(e)
        
        # draw the diameter of the gem to be positioned, right beside the cursor.
        def dynamicGemTextCallback(sender, args):
            xform = args.Viewport.GetTransform(CS.World, CS.Screen)
            current_point = args.CurrentPoint
            current_point.Transform(xform)
            screen_point = Rhino.Geometry.Point2d(current_point.X, current_point.Y)
            # msg = "screen {0}, {1}".format(screen_point.X, screen_point.Y)
            msg = "  {0}".format(self.currentGem.diameter)
            args.Display.Draw2dText(msg, Color.Blue, screen_point, False, 30)
        
        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt('Click on the base object to add a gem. Press SHIFT to increase and CTRL to decrease the size.')
        
        gp.DynamicDraw += dynamicGemMoveCallback
        gp.DynamicDraw += dynamicGemTextCallback
        
        if self.baseObject:
            if isinstance(self.baseObject, Rhino.Geometry.Brep):
                gp.Constrain(self.baseObject, -1, -1, False)
            elif isinstance(self.baseObject, Rhino.Geometry.SubD):
                print "DOESN'T WORK ON SUBD YET !!"
            elif isinstance(self.baseObject, Rhino.Geometry.Mesh):
                gp.Constrain(self.baseObject, False)
            
        gp.PermitObjectSnap(False) # quickfix: the selection would snap on the gem brep itself otherwise, a workaround must be found to enable object snap.
        gp.Get()
        
        return gp.CommandResult() == Rhino.Commands.Result.Success
    
    def makeGem(self, baseObject=None, diameter=1):
        self.lastGem = gem.Gem(diameter, self.gemadder.idef_index)
        self.currentGem = self.lastGem
        self.baseObject = baseObject
        
        # If the last instance positioning was cancelled, we delete this instance
        response = self.moveGem(self.lastGem)
        self.currentGem = None
        if response:
            return self.lastGem
        else:
            self.lastGem.dispose()
            return False

def getClosestFace(facesEnum, point3d):
    closestFace = None
    closestDist = float('inf')
    for face in facesEnum:
        res = face.ClosestPoint( point3d )
        closestPoint = face.PointAt(res[1], res[2])
        dist = point3d.DistanceTo(closestPoint)
        if dist < closestDist:
            closestDist = dist
            closestFace = face
    return closestFace