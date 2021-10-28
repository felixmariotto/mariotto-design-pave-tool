
import Rhino
import scriptcontext as sc

def GemBrep( radius=1, mustInvert=False ):
    
    origin = Rhino.Geometry.Point3d(0,0,0)
    up = Rhino.Geometry.Vector3d(0,0,1)
    down = Rhino.Geometry.Vector3d(0,0,-1)
    
    # circle curve
    
    circle = Rhino.Geometry.Circle(radius)
    curve = circle.ToNurbsCurve()
    
    # cylinder
    
    height = radius * 0.5
    extrusion = Rhino.Geometry.Extrusion.Create(curve, height, False)
    cyl_brep = extrusion.ToBrep()
    
    # cone
    
    plane = Rhino.Geometry.Plane(origin, up)
    cone = Rhino.Geometry.Cone(plane, radius, radius)
    cone_brep = cone.ToBrep(False)
    xform = Rhino.Geometry.Transform.Translation(0, 0, radius * -1)
    cone_brep.Transform(xform)
    
    # join cylinder and cone, then cap, then add to the document
    
    joined = Rhino.Geometry.Brep.JoinBreps([cyl_brep, cone_brep], 0.001)
    joined_brep = joined[0]
    joined_brep = joined_brep.CapPlanarHoles(0.001)
    
    # if required in parameter, we flip the gem upside down
    
    if mustInvert:
        xform = Rhino.Geometry.Transform.Rotation(up, down, origin)
        joined_brep.Transform(xform)
    
    #
    
    return joined_brep
