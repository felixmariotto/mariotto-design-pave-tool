
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
        self.gem_instance_def = sc.doc.InstanceDefinitions.Find(self.name, True)
        if not self.gem_instance_def:
            print('create def')
            brep = gembrep.GemBrep(0.5)
            attributes = sc.doc.CreateDefaultAttributes()
            self.idef_index = sc.doc.InstanceDefinitions.Add(self.name, "", origin, brep, attributes)
            self.gem_instance_def = sc.doc.InstanceDefinitions[self.idef_index]
        else:
            i = 0
            for instanceDef in sc.doc.InstanceDefinitions:
                if instanceDef == self.gem_instance_def:
                    self.idef_index = i
                i += 1
        
        """
        # Create the gem instance definition
        brep = gembrep.GemBrep(0.5)
        attributes = sc.doc.CreateDefaultAttributes()
        self.idef_index = sc.doc.InstanceDefinitions.Add(self.name, "", origin, brep, attributes)
        """
    
    def updateGemDefName(self, newName):
        print('update definition with new name :', newName)