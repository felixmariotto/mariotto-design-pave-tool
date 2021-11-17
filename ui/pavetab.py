
"""
UI panel that's responsible for interaction with one pave setting.
This panel is duplicated for each new pave setting.
When instanced with Form(), it get passed an instance of Handler,
which is the functional module for handling the pave in the scene.
"""

import Eto.Forms as forms
import Eto.Drawing as drawing

class TabContent(forms.Panel):

    def __init__(self):
        add_button = self.AddButton()
        remove_button = self.EditButton()
        self.pave_text = self.PaveText('test')
        #
        layout = forms.DynamicLayout()
        layout.DefaultSpacing = drawing.Size(5, 5)
        layout.Padding = drawing.Padding(10)
        #
        layout.AddSeparateRow(forms.Label(Text = 'Pave name:'), self.pave_text)
        layout.AddSeparateRow(add_button, remove_button, None)
        layout.Add(None)
        #
        self.Content = layout
    
    def setHandler(self, handler):
        self.handler = handler
    
    def setTabPage(self, tab_page):
        self.tab_page = tab_page
        self.pave_text.Text = tab_page.Text
    
    def OnButtonClick(self, sender, e):
        self.handler.addGems()
    
    def AddButton(self):
        button = forms.Button(MinimumSize = drawing.Size.Empty)
        button.Text = "Add gems"
        button.Click += self.OnButtonClick
        return button
    
    def onEditClick(self, sender, e):
        print('edit gems')
    
    def EditButton(self):
        button = forms.Button(MinimumSize = drawing.Size.Empty)
        button.Text = "Edit gems"
        button.Click += self.onEditClick
        return button
    
    def onPaveTextChange(self, sender, e):
        self.tab_page.Text = e.NewText
        self.handler.updateName(e.NewText)
    
    def PaveText(self, string):
        text_box = forms.TextBox()
        text_box.Text = string
        text_box.TextChanging += self.onPaveTextChange
        return text_box

def Form(name, handler):
    # this will link an instance definition to the pave
    handler.findOrCreateGemDef(name)
    #
    tab_page = forms.TabPage()
    tab_page.Text = name
    control = forms.Panel()
    control.Content = TabContent()
    control.Content.setHandler(handler)
    control.Content.setTabPage(tab_page)
    tab_page.Content = control
    return tab_page