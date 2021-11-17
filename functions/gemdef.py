
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
        pass
    
    def findOrCreateGemDef(self, name):
        # See if block name already exists
        self.gem_instance_def = sc.doc.InstanceDefinitions.Find(name, True)
        if not self.gem_instance_def:
            brep = gembrep.GemBrep(0.5)
            attributes = sc.doc.CreateDefaultAttributes()
            self.idef_index = sc.doc.InstanceDefinitions.Add(name, "", origin, brep, attributes)
            self.gem_instance_def = sc.doc.InstanceDefinitions[self.idef_index]
        else:
            i = 0
            for instanceDef in sc.doc.InstanceDefinitions:
                if instanceDef == self.gem_instance_def:
                    self.idef_index = i
                i += 1
    
    def updateGemDefName(self, newName):
        sc.doc.InstanceDefinitions.Modify(self.idef_index, newName, "", True)
