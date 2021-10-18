
import Eto.Forms as forms
import Eto.Drawing as drawing

class TabContent(forms.Panel):

    def __init__(self):
        #
        label = forms.Label()
        label.Text = "Text Label"
        #
        layout = forms.DynamicLayout()
        layout.DefaultSpacing = drawing.Size(5, 5)
        layout.Padding = drawing.Padding(10)
        #
        layout.Add(label)
        #
        self.Content = layout

class Form(forms.TabPage):
    
    def __init__(self):
        self.Text = "pave n"
        control = forms.Panel()
        control.Content = TabContent()
        self.Content = control