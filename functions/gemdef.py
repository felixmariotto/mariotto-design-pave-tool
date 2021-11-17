
"""
responsible for creating and updating a gem instance definition
"""

import Rhino
import scriptcontext as sc
from imp import reload
import gembrep
reload(gembrep)

# Block base point
origin = Rhino.Geometry.Point3d(0, 0, 0)

class c:
    def __init__(self):
        self.name = 'test-name'
        
        # See if block name already exists
        existing_idef = sc.doc.InstanceDefinitions.Find(self.name, True)
        if existing_idef:
            print "Block definition", self.name, "already exists"
            
        # Create the gem instance definition
        brep = gembrep.GemBrep(0.5)
        attributes = sc.doc.CreateDefaultAttributes()
        self.idef_index = sc.doc.InstanceDefinitions.Add(self.name, "", origin, brep, attributes)