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
from addonmanager_installer import AddonInstaller
import Addon
import functools
from PySide import QtCore

class installer:
    def __init__( self, name: str, url: str, branch: str, param_path = "",installation_path = "" ):
        self.param_path = param_path
        addon_to_install = Addon.Addon(name=name, url=url, branch=branch)
        self.worker_thread = QtCore.QThread()
        self.installer = AddonInstaller(addon_to_install)
        if len(installation_path):
            self.installler.installation_path=installation_path
        self.installer.moveToThread(self.worker_thread)
        self.installer.success.connect(self.installation_succeeded)
        self.installer.failure.connect(self.installation_failed)
        self.installer.finished.connect(self.worker_thread.quit)
        self.worker_thread.started.connect(self.installer.run)
        self.worker_thread.start() # Returns immediately

    def installation_succeeded(self):
        App.Console.PrintLog(f'Installed {self.installer.addon_to_install.name}\n')
        if len(self.param_path):
            params = App.ParamGet('User parameter:BaseApp').GetGroup(self.param_path)
            params.SetBool('Installed', True)

    def installation_failed(self):
        App.Console.PrintLog(f'Failed installing {self.installer.addon_to_install.name}\n')
