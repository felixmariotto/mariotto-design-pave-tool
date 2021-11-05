
import Eto.Forms as forms
import Eto.Drawing as drawing

class TabContent(forms.Panel):

    def __init__(self):
        #
        add_button = self.AddButton()
        remove_button = self.RemoveButton()
        #
        layout = forms.DynamicLayout()
        layout.DefaultSpacing = drawing.Size(5, 5)
        layout.Padding = drawing.Padding(10)
        #
        layout.AddSeparateRow(add_button, remove_button, None)
        layout.Add(None)
        #
        self.Content = layout
    
    def OnButtonClick(self, sender, e):
        self.handler.addGems()
    
    def AddButton(self):
        button = forms.Button(MinimumSize = drawing.Size.Empty)
        button.Text = "Add gems"
        button.Click += self.OnButtonClick
        return button
    
    def onRemoveClick(self, sender, e):
        print('remove gems')
    
    def RemoveButton(self):
        button = forms.Button(MinimumSize = drawing.Size.Empty)
        button.Text = "Remove gems"
        button.Click += self.onRemoveClick
        return button

def Form(name, handler):
    tp = forms.TabPage()
    tp.Text = "pave " + name
    control = forms.Panel()
    control.Content = TabContent()
    control.Content.handler = handler;
    tp.Content = control
    return tp