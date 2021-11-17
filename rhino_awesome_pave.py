
"""
root file of rhino_awesome_pave.
Its only job is to make an instance of the main UI and add
it to Rhino window.
"""

from imp import reload

from ui import main
from ui import keymanager
from functions import handler

reload(main)
reload(keymanager)
reload(handler)

import Rhino

main.Form.H = handler.Handler

def rhino_awesome_pave():
    form = main.Form()
    form.Owner = Rhino.UI.RhinoEtoApp.MainWindow
    form.Show()
    kpm = keymanager.KeyPressManager()
    kpm.addIncreaseCallback( form.handleIncrease )
    kpm.addDecreaseCallback( form.handleDecrease )

if __name__ == '__main__':
    rhino_awesome_pave()
