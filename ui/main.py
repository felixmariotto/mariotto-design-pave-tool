
import Eto.Forms as forms
import Eto.Drawing as drawing

class Form(forms.Form):
    
    def __init__(self):
        
        self.Title = "rhino_awesome_pave"
        self.Padding = drawing.Padding(10)
        self.Resizable = True
        self.ClientSize = drawing.Size(300, 70)