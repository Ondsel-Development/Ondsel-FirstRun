# SPDX-License-Identifier: MIT
# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2023 2023 Ondsel, Inc.                                  *
# *                                                                         *
# *   This file is part of Ondsel Preference Pack                           *
# *                                                                         *
# *   See LICENSE file for details about copyright.                         *
# *                                                                         *
# ***************************************************************************

import FreeCAD as App
import FreeCADGui as Gui
import json
import os
from PySide import QtCore
import install_mod

version = App.Version()
version = version[0].__str__() + '.' + version[1].__str__()
params = App.ParamGet('User parameter:BaseApp')
mw = Gui.getMainWindow()
modpath = os.path.dirname(__file__)

def onStart():
    if mw.property("eventLoop"):
        timer.stop()
        timer.timeout.disconnect(onStart)
        
        with open(os.path.join(modpath,'mods.json'), "r") as fp:
            mods = json.load(fp)

        mw.addon_installers = []
        for mod in mods["addons"]:
            param_path = f'Ondsel/{version}/mods/{mod["name"]}'
            if mod["installToUser"] and not params.GetGroup(param_path).GetBool('Installed', False):
                mw.addon_installers.append(install_mod.installer(mod["name"],mod["url"],mod["branch"],param_path))
        for mod in mods["preferencePacks"]:
            param_path = f'Ondsel/{version}/mods/{mod["name"]}'
            if mod["installToUser"] and not params.GetGroup(param_path).GetBool('Installed', False):
                mw.addon_installers.append(install_mod.installer(mod["name"],mod["url"],mod["branch"],param_path))

timer = QtCore.QTimer()
timer.timeout.connect(onStart)
timer.start(500)