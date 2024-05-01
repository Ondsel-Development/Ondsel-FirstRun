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

        # Uninstall opendark and sheetmetal once
        od_path=os.path.join(userModPath,"OpenDark")
        sm_path=os.path.join(userModPath,"sheetmetal")

        if not params.GetGroup(f'Ondsel/mods/OpenDark').GetBool('uninstalled',False):
          if os.path.exists(od_path):
            shutil.rmtree(od_path)
          params.GetGroup(f'Ondsel/mods/OpenDark').SetBool('uninstalled',True)
        if not params.GetGroup(f'Ondsel/mods/sheetmetal').GetBool('uninstalled',False):
          if os.path.exists(sm_path):
            shutil.rmtree(sm_path)
          params.GetGroup(f'Ondsel/mods/sheetmetal').SetBool('uninstalled',True)      
        
        # Install updatable addons
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