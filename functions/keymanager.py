
import Rhino
import scriptcontext as sc

class KeyboardEventHandler():
    def __init__(self):
        Rhino.RhinoApp.KeyboardEvent += self.event
        self.shift_is_pressed = False
        self.ctrl_is_pressed = False
        self.OnIncrease = []
        self.OnDecrease = []
    
    def disable(self):
        Rhino.RhinoApp.KeyboardEvent -= self.event
    
    def event(self, key):
        if key == 16: # SHIFT
            self.shift_is_pressed = not self.shift_is_pressed
            if self.shift_is_pressed:
                for callback in self.OnIncrease:
                    callback()
        elif key == 17: # CONTROL
            self.ctrl_is_pressed = not self.ctrl_is_pressed
            if self.ctrl_is_pressed:
                for callback in self.OnDecrease:
                    callback()

#

class KeyPressManager():
    def __init__(self):
        # this is just a coding tool, to remove the old version before to test the new one.
        stky = sc.sticky.pop('key-handler', None)
        if stky:
            stky.disable()
        # add the event handler
        stky = KeyboardEventHandler()
        sc.sticky['key-handler'] = stky
        self.handler = stky
        self.callbacks = []
    
    def addIncreaseCallback(self, callback):
        if self.handler:
            self.handler.OnIncrease.append(callback)
    
    def addDecreaseCallback(self, callback):
        if self.handler:
            self.handler.OnDecrease.append(callback)

## usage

def handleIncrease():
    print('handle increase')

def handleDecrease():
    print('handle decrease')

kpm = KeyPressManager()
kpm.addIncreaseCallback( handleIncrease )
kpm.addDecreaseCallback( handleDecrease )