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
from addonmanager_uninstaller import AddonUninstaller
import Addon
import functools
from PySide import QtCore

class uninstaller:
    def __init__( self, name: str, param_path = "",installation_path = "" ):
        self.param_path = param_path
        addon_to_remove = Addon.Addon(name=name)
        self.worker_thread = QtCore.QThread()
        self.uninstaller = AddonUninstaller(addon_to_remove)
        if len(installation_path):
            self.uninstaller.installation_path=installation_path
        self.uninstaller.moveToThread(self.worker_thread)
        self.uninstaller.success.connect(self.removal_succeeded)
        self.uninstaller.failure.connect(self.removal_failed)
        self.uninstaller.finished.connect(self.worker_thread.quit)
        self.worker_thread.started.connect(self.uninstaller.run)
        self.worker_thread.start() # Returns immediately

    def removal_succeeded(self):
        App.Console.PrintLog(f'Uninstalled {self.uninstaller.addon_to_remove.name} from user directory\n')
        if len(self.param_path):
            params = App.ParamGet('User parameter:BaseApp').GetGroup(self.param_path)
            params.SetBool('Uninstalled', True)

    def removal_failed(self):
        App.Console.PrintLog(f'Failed uninstalling {self.uninstaller.addon_to_remove.name}\n')
