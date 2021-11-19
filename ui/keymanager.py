
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
        print(str(key) + ' key was pressed')
        if key == 16: # SHIFT
            print('detected SHIFT key')
            self.shift_is_pressed = not self.shift_is_pressed
            if self.shift_is_pressed:
                for callback in self.OnIncrease:
                    print('will call a callback')
                    callback()
        elif key == 17: # CONTROL
            print('detected CONTROL key')
            self.ctrl_is_pressed = not self.ctrl_is_pressed
            if self.ctrl_is_pressed:
                for callback in self.OnDecrease:
                    print('will call a callback')
                    callback()

#

class KeyPressManager():
    def __init__(self):
        print('KeyPressManager initiated')
        # this is just a coding tool, to remove the old version before to test the new one.
        stky = sc.sticky.pop('key-handler', None)
        if stky:
            print('stky disabled')
            stky.disable()
        # add the event handler
        stky = KeyboardEventHandler()
        sc.sticky['key-handler'] = stky
        self.handler = stky
        self.callbacks = []
        print('KeyPressManager ended init')
    
    def addIncreaseCallback(self, callback):
        if self.handler:
            self.handler.OnIncrease.append(callback)
    
    def addDecreaseCallback(self, callback):
        if self.handler:
            self.handler.OnDecrease.append(callback)
