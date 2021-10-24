
"""
root file of rhino_awesome_pave.
Its only job is to make an instance of the main UI and add
it to Rhino window.
"""

from imp import reload

from ui import main
reload(main)

from functions import handler
reload(handler)

import Rhino.UI

main.Form.H = handler.Handler

def rhino_awesome_pave():
    form = main.Form()
    form.Owner = Rhino.UI.RhinoEtoApp.MainWindow
    form.Show()

if __name__ == '__main__':
    rhino_awesome_pave()