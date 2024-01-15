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

if not params.GetGroup('Ondsel/mods/AssemblyWorkbench').GetBool('firstForceEnableDone', False):
    disabledWBs = params.GetGroup('Preferences/Workbenches').GetString('Disabled')
    if disabledWBs.__contains__('AssemblyWorkbench'):
        disabledWBs = disabledWBs.split(',')
        disabledWBs.remove('AssemblyWorkbench')
        disabledWBs = ','.join(disabledWBs)
        params.GetGroup('Preferences/Workbenches').SetString('Disabled',disabledWBs)
        params.GetGroup('Preferences/Workbenches').RemString('Ordered')
    params.GetGroup('Ondsel/AssemblyWorkbench').SetBool('firstForceEnableDone', True)
    App.Console.PrintLog('Force enabled AssemblyWorkbench')

if not params.GetGroup('Ondsel/mods/ArchWorkbench').GetBool('firstForceDisableDone', False):
    disabledWBs = params.GetGroup('Preferences/Workbenches').GetString('Disabled')
    if not disabledWBs.__contains__('ArchWorkbench'):
        disabledWBs = disabledWBs.split(',')
        disabledWBs.add('ArchWorkbench')
        disabledWBs = ','.join(disabledWBs)
        params.GetGroup('Preferences/Workbenches').SetString('Disabled',disabledWBs)
        params.GetGroup('Preferences/Workbenches').RemString('Ordered')
    params.GetGroup('Ondsel/ArchWorkbench').SetBool('firstForceDisableDone', True)
    App.Console.PrintLog('Force disabled ArchWorkbench')

if not params.GetGroup('Ondsel/mods/Websites').GetBool('firstForceClean', False):
    params.GetGroup('Preferences').RemGroup('Websites')
    params.GetGroup('Ondsel/mods/Websites').SetBool('firstForceClean', True)

if platform.system() == 'Darwin':
    params.GetGroup('Preferences/MainWindow').SetString('WSPosition','WSToolbar')
    App.Console.PrintLog('Force disabled showing workbench selector in menu since it\'s not supported in macOS')

App.saveParameter()