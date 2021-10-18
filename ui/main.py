
"""
main UI module of rhino_awesome_pave.
"""

import System
import Eto.Forms as forms
import Eto.Drawing as drawing

from imp import reload

import pavetab
reload(pavetab)

###

class Form(forms.Form):
    
    # Initializer
    def __init__(self):
        self.Rnd = System.Random()
        self.Title = "Sample Eto Tabbed Dialog"
        self.Padding = drawing.Padding(10)
        self.Resizable = True
        self.Content = self.Create()
    
    # Create the dialog content
    def Create(self):
        # create default tab
        self.TabControl = forms.TabControl()
        self.TabControl.TabPosition = forms.DockPosition.Top
        tab = pavetab.Form()
        self.TabControl.Pages.Add(tab)
        # create stack layout item for tabs
        tab_items = forms.StackLayoutItem(self.TabControl, True)
        # create layout for buttons
        button_layout = forms.StackLayout()
        button_layout.Orientation = forms.Orientation.Horizontal
        button_layout.Items.Add(None)
        button_layout.Items.Add(self.AddTab())
        button_layout.Items.Add(self.RemoveTab())
        button_layout.Items.Add(None)
        # create stack layout for content
        layout = forms.StackLayout()
        layout.Spacing = 5
        layout.HorizontalContentAlignment = forms.HorizontalAlignment.Stretch
        # add the stuff above to this layout
        layout.Items.Add(button_layout)
        layout.Items.Add(tab_items)
        return layout
    
    # AddTab button click handler
    def AddTabClick(self, sender, e):
        # tab.Text = "Tab" + str(self.TabControl.Pages.Count + 1)
        tab = pavetab.Form()
        self.TabControl.Pages.Add(tab)
    
    # Creates an add tab button
    def AddTab(self):
        button = forms.Button()
        button.Text = "Add Tab"
        button.Click += self.AddTabClick
        return button
    
    # RemoveTab button click handler
    def RemoveTabClick(self, sender, e):
        if (self.TabControl.SelectedIndex >= 0 and self.TabControl.Pages.Count > 0):
            self.TabControl.Pages.RemoveAt(self.TabControl.SelectedIndex)
    
    # Creates a remove tab button
    def RemoveTab(self):
        button = forms.Button()
        button.Text = "Remove Tab"
        button.Click += self.RemoveTabClick
        return button