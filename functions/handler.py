
from imp import reload

import gemadder
reload( gemadder )

class Handler(gemadder.c):
    
    def __init__(self):
        self.gems = []
        gemadder.c.__init__(self)