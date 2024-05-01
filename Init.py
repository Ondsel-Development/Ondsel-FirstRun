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

import os
import platform
import shutil
import FreeCAD as App

params = App.ParamGet('User parameter:BaseApp')
userModPath=os.path.join(FreeCAD.getUserAppDataDir(),"Mod")

od_path=os.path.join(userModPath,"OpenDark")
sm_path=os.path.join(userModPath,"sheetmetal")
if not params.GetGroup('Ondsel/mods/OpenDark').GetBool('uninstalled',False):
  if os.path.exists(od_path):
    shutil.rmtree(od_path)
  params.GetGroup('Ondsel/mods/OpenDark').SetBool('uninstalled',True)
if not params.GetGroup('Ondsel/mods/sheetmetal').GetBool('uninstalled',False):
  if os.path.exists(sm_path):
    shutil.rmtree(sm_path)
  params.GetGroup('Ondsel/mods/sheetmetal').SetBool('uninstalled',True)

if not params.GetGroup('Ondsel/mods/AssemblyWorkbench').GetBool('firstForceEnableDone', False):
    disabledWBs = params.GetGroup('Preferences/Workbenches').GetString('Disabled')
    if disabledWBs.__contains__('AssemblyWorkbench'):
        disabledWBs = disabledWBs.split(',')
        disabledWBs.remove('AssemblyWorkbench')
        disabledWBs = ','.join(disabledWBs)
        params.GetGroup('Preferences/Workbenches').SetString('Disabled',disabledWBs)
        params.GetGroup('Preferences/Workbenches').RemString('Ordered')
    params.GetGroup('Ondsel/mods/AssemblyWorkbench').SetBool('firstForceEnableDone', True)
    App.Console.PrintLog('Force enabled AssemblyWorkbench')

if not params.GetGroup('Ondsel/mods/ArchWorkbench').GetBool('firstForceDisableDone', False):
    disabledWBs = params.GetGroup('Preferences/Workbenches').GetString('Disabled')
    if not disabledWBs.__contains__('ArchWorkbench'):
        disabledWBs = disabledWBs.split(',')
        disabledWBs.append('ArchWorkbench')
        disabledWBs = ','.join(disabledWBs)
        params.GetGroup('Preferences/Workbenches').SetString('Disabled',disabledWBs)
        params.GetGroup('Preferences/Workbenches').RemString('Ordered')
    params.GetGroup('Ondsel/mods/ArchWorkbench').SetBool('firstForceDisableDone', True)
    App.Console.PrintLog('Force disabled ArchWorkbench')

if not params.GetGroup('Ondsel/mods/Websites').GetBool('firstForceClean', False):
    params.GetGroup('Preferences').RemGroup('Websites')
    params.GetGroup('Ondsel/mods/Websites').SetBool('firstForceClean', True)

toolbar_on_menu = params.GetGroup('Preferences/MainWindow').GetString('WSPosition') != 'WSToolbar'
if platform.system() == 'Darwin' and toolbar_on_menu:
    params.GetGroup('Preferences/MainWindow').SetString('WSPosition','WSToolbar')
    App.Console.PrintLog('Force disabled showing workbench selector in menu since it\'s not supported in macOS')

App.saveParameter()
