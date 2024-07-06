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
    params.GetGroup('Ondsel/mods/AssemblyWorkbench').SetBool('firstForceEnableDone', True)
    App.Console.PrintLog('Force enabled AssemblyWorkbench')

if not params.GetGroup('Ondsel/mods/Assembly').GetBool('firstEnableExperimental', False):
    params.GetGroup('Preferences/Mod/Assembly').SetBool('ExperimentalFeatures',True)
    params.GetGroup('Ondsel/mods/Assembly').SetBool('firstEnableExperimental', True)

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

if not params.GetGroup('Ondsel/mods/TechDraw').GetBool('firstForceEnableSingleDimension', False):
    params.GetGroup('Preferences/Mod/TechDraw').SetBool('SingleDimensioningTool',True)
    params.GetGroup('Preferences/Mod/TechDraw').SetBool('SeparatedDimensioningTools',False)
    params.GetGroup('Ondsel/mods/TechDraw').SetBool('firstForceEnableSingleDimension', True)

if not params.GetGroup('Ondsel/mods/AddonManager').GetBool('firstSetScoreUrl', False):
    params.GetGroup('Preferences/Addons').SetString('AddonsScoreURL',"https://ondsel.com/RecommendedAddons.json")
    params.GetGroup('Ondsel/mods/AddonManager').SetBool('firstSetScoreUrl', True)

if not params.GetGroup('Ondsel').GetBool('firstSetHeadlightIntensity', False):
    params.GetGroup('Preferences/View').SetInt('HeadlightIntensity', 80)
    params.GetGroup('Ondsel').SetBool('firstSetHeadlightIntensity', True)

if not params.GetGroup('Ondsel').GetBool('firstSet_WorkbenchSelectorType', False):
    params.GetGroup('Preferences/Workbenches').SetInt('WorkbenchSelectorType', 1)
    if params.GetGroup('Preferences/MainWindow').GetString('WSPosition') != 'WSToolbar':
        params.GetGroup('Preferences/MainWindow').SetString('WSPosition','WSToolbar')
    params.GetGroup('Ondsel').SetBool('firstSet_WorkbenchSelectorType', True)

if not params.GetGroup('Ondsel').GetBool('firstSetQtStyle', False):
    params.GetGroup('Preferences/General').SetString('QtStyle', 'Fusion')
    params.GetGroup('Ondsel').SetBool('firstSetQtStyle', True)

App.saveParameter()
