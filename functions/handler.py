
"""
Handler is contructed from the different functionalities of the pave.
One handler is responsible for one pave.
"""

from imp import reload

import gemadder
import notes
import gemdef

reload( gemadder )
reload( notes )
reload( gemdef )

class Handler(gemadder.c, notes.c, gemdef.c):
    
    def __init__(self):
        self.name = None
        self.gems = []
        self.onIncrease = []
        self.onDecrease = []
        gemadder.c.__init__(self)
        notes.c.__init__(self)
        gemdef.c.__init__(self)
    
    def handleIncrease(self): # triggered when the user press Shift
        for callback in self.onIncrease:
            callback()
    
    def handleDecrease(self): # triggered when the user press Ctrl
        for callback in self.onDecrease:
            callback()
    
    def updateName(self, newName):
        if not self.name:
            self.findOrCreateGemDef(newName)
        else:
            self.updateGemDefName(newName)
        self.name = newName