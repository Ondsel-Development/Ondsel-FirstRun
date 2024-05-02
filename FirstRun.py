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
import shutil
from PySide import QtCore
import install_mod
import uninstall_mod

version = App.Version()
version = version[0].__str__() + '.' + version[1].__str__()
params = App.ParamGet('User parameter:BaseApp')
mw = Gui.getMainWindow()
modpath = os.path.dirname(__file__)
userModPath=os.path.join(App.getUserAppDataDir(),"Mod")

def onStart():
    if mw.property("eventLoop"):
        timer.stop()
        timer.timeout.disconnect(onStart)

        mw.addon_installers = []

        # uninstall addons that should be loaded from the bundle
        for mod in ['OpenDark','sheetmetal']:
          param_path = f'Ondsel/mods/{mod}'
          if os.path.exists(os.path.join(userModPath,mod)) and not params.GetGroup(param_path).GetBool('Uninstalled',False):
            mw.addon_installers.append(uninstall_mod.uninstaller(name=mod,param_path=param_path))     
        
        # Install updatable addons
        with open(os.path.join(modpath,'mods.json'), "r") as fp:
                    mods = json.load(fp)

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