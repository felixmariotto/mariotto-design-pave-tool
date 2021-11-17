
"""
main UI module of rhino_awesome_pave.
"""

import scriptcontext as sc

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
        # basic style
        self.Title = "rhino_awesome_pave"
        self.ClientSize = drawing.Size(300, 200)
        self.Padding = drawing.Padding(10)
        self.Resizable = True
        # state management
        self.tab_count = 0
        # content
        self.pave_tabs = []
        self.Content = self.Create()
    
    # Create the dialog content
    def Create(self):
        self.TabControl = forms.TabControl()
        self.TabControl.TabPosition = forms.DockPosition.Top
        # Look for instance definitions with a reserved name.
        # For each of them we create a pave tab.
        for instanceDef in sc.doc.InstanceDefinitions:
            if instanceDef.HasName and instanceDef.Name.find('rh_awe_pav') > -1:
                self.CreateTab(instanceDef.Name)
        # create default tab if no old pave was found
        if self.tab_count == 0:
            self.CreateTab()
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
    
    # add a new tab to self.TabControl
    def CreateTab(self, name=None):
        self.tab_count += 1
        name = name or 'rh_awe_pav_' + str(self.tab_count)
        # here we pass in an instance of Handler (functions/handler.py)
        tab = pavetab.Form( name, self.H() )
        self.TabControl.Pages.Add(tab)
        self.pave_tabs.append(tab)
    
    # AddTab button click handler
    def AddTabClick(self, sender, e):
        self.CreateTab()
    
    # Creates an add tab button
    def AddTab(self):
        button = forms.Button()
        button.Text = "New Pave"
        button.Click += self.AddTabClick
        return button
    
    # RemoveTab button click handler
    def RemoveTabClick(self, sender, e):
        if (self.TabControl.SelectedIndex >= 0 and self.TabControl.Pages.Count > 0):
            self.TabControl.Pages.RemoveAt(self.TabControl.SelectedIndex)
    
    # Creates a remove tab button
    def RemoveTab(self):
        button = forms.Button()
        button.Text = "Delete Pave"
        button.Click += self.RemoveTabClick
        return button
    
    def handleIncrease(self):
        for pave_tab in self.pave_tabs:
            pave_tab.Content.Content.handler.handleIncrease()
    
    def handleDecrease(self):
        for pave_tab in self.pave_tabs:
            pave_tab.Content.Content.handler.handleDecrease()