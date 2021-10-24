
import Rhino
import scriptcontext as sc

class c:
    
    def __init__(self):
        self.circle_center = Rhino.Geometry.Point3d(0, 0, 0)
    
    # dynamic redraw callback, to update the position of the gem
    # while the user moves the cursor on the surface.
    def callback(self, sender, args):
        try:
            translation = args.CurrentPoint - self.circle_center
            
            self.circle_center.X = args.CurrentPoint.X
            self.circle_center.Y = args.CurrentPoint.Y
            self.circle_center.Z = args.CurrentPoint.Z
            
            xf = Rhino.Geometry.Transform.Translation(translation)
        
            sc.doc.Objects.Transform(self.circleID, xf, True)
            sc.doc.Views.Redraw()
        except Exception, e:
            print(e)
    
    def addGems(self):
        
        # get the surface on which to position the gem
        go = Rhino.Input.Custom.GetObject()
        go.SetCommandPrompt('select the surface on which to orient a circle')
        go.GeometryFilter = Rhino.DocObjects.ObjectType.Surface
        go.Get()
        if go.CommandResult() != Rhino.Commands.Result.Success:
            return
        obj_ref = go.Object(0)
        self.surf = obj_ref.Geometry().Surfaces[0]
        
        # reset the circle position that will be updated in the callback
        self.circle_center.X = 0
        self.circle_center.Y = 0
        self.circle_center.Z = 0
        
        # create a new circle
        circle = Rhino.Geometry.Circle(1)
        self.circleID = sc.doc.Objects.AddCircle(circle)
        
        #
        gp = Rhino.Input.Custom.GetPoint()
        gp.Constrain( self.surf, False )
        gp.DynamicDraw += self.callback
        gp.Get()