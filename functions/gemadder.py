
import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs

class c:
    
    def __init__(self):
        self.circle_center = Rhino.Geometry.Point3d(0, 0, 0)
        self.up = Rhino.Geometry.Vector3d(0, 0, 1)
    
    # dynamic redraw callback, to update the position of the gem
    # while the user moves the cursor on the surface.
    def callback(self, sender, args):
        try:
            # translate the gem
            translation = args.CurrentPoint - self.circle_center
            
            self.circle_center.X = args.CurrentPoint.X
            self.circle_center.Y = args.CurrentPoint.Y
            self.circle_center.Z = args.CurrentPoint.Z
            
            xf = Rhino.Geometry.Transform.Translation(translation)
            sc.doc.Objects.Transform(self.circleID, xf, True)
            
            # rotate the gem
            res = self.surf.ClosestPoint( args.CurrentPoint )
            norm = self.surf.NormalAt(res[1], res[2])
            xf = Rhino.Geometry.Transform.Rotation(self.up, norm, args.CurrentPoint)
            sc.doc.Objects.Transform(self.circleID, xf, True)
            self.up.X = norm.X
            self.up.Y = norm.Y
            self.up.Z = norm.Z
            
            # redraw
            sc.doc.Views.Redraw()
        except Exception, e:
            print(e)
    
    def addGem(self):
        try:
            # reset the circle position that will be updated in the callback
            self.circle_center.X = 0
            self.circle_center.Y = 0
            self.circle_center.Z = 0
            
            # reset the circle up vector, which will be updated in the callback
            self.up.X = 0
            self.up.Y = 0
            self.up.Z = 1
            
            # create a new circle
            circle = Rhino.Geometry.Circle(1)
            self.circleID = sc.doc.Objects.AddCircle(circle)
            
            #
            gp = Rhino.Input.Custom.GetPoint()
            gp.Constrain( self.surf, False )
            gp.PermitObjectSnap(False)
            gp.DynamicDraw += self.callback
            gp.Get()
            if gp.CommandResult() != Rhino.Commands.Result.Success:
                # remove the gem
                rs.DeleteObject( self.circleID )
                # return false so that the endless loop of circle positioning is terminated
                return False
            else :
                return True
        except Exception, e:
            print(e)
    
    def addGems(self):
        # get the surface on which to position the gem
        go = Rhino.Input.Custom.GetObject()
        go.SetCommandPrompt('select the surface on which to orient a gem')
        go.GeometryFilter = Rhino.DocObjects.ObjectType.Surface
        go.Get()
        if go.CommandResult() != Rhino.Commands.Result.Success:
            return
        obj_ref = go.Object(0)
        self.surf = obj_ref.Geometry().Surfaces[0]
        
        while self.addGem():
            pass
        else:
            pass
            # do something when all gems have been positioned