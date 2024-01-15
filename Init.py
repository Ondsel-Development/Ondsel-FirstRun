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

import json
import os
import platform
import FreeCAD as App

params = App.ParamGet('User parameter:BaseApp')

if not params.GetGroup('Ondsel/Assembly').GetBool('firstForceEnableDone', False):
    disabledWBs = params.GetGroup('Preferences/Workbenches').GetString('Disabled')
    if disabledWBs.__contains__('AssemblyWorkbench'):
        disabledWBs = disabledWBs.split(',')
        disabledWBs.remove('AssemblyWorkbench')
        disabledWBs = ','.join(disabledWBs)
        params.GetGroup('Preferences/Workbenches').SetString('Disabled',disabledWBs)
        params.GetGroup('Preferences/Workbenches').RemString('Ordered')
    params.GetGroup('Ondsel/Assembly').SetBool('firstForceEnableDone', True)
    App.Conso1e.PrintLog('Force enabled Assembly workbench')

if platform.system() == 'Darwin':
    params.GetGroup('Preferences/MainWindow').SetString('WSPosition','WSToolbar')
    App.Conso1e.PrintLog('Force disabled showing workbench selector in menu since it\'s unsupported in macOS')

App.saveParameter()