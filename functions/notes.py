
"""
This module is responsible for writting and reading information in the 3dm file.
We want information about pave settings to be recoverable when you close Rhino
and reopen it.
"""

import scriptcontext as sc

# sc.doc.Notes

class c:
    def __init__(self):
        pass
    
    def writeData(self):
        print('write data in notes')
    
    def readData(self):
        print('read data in notes')
