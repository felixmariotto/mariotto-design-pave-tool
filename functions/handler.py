
from imp import reload

import gemadder
reload( gemadder )

class Handler(gemadder.c):
    
    def __init__(self):
        gemadder.c.__init__(self)
        self.x = 'bla'