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
from PySide import QtGui, QtCore, QtUiTools
import install_mod

version = App.Version()
version = version[0].__str__() + '.' + version[1].__str__()
params = App.ParamGet('User parameter:BaseApp')
mw = Gui.getMainWindow()
modpath = os.path.dirname(__file__)
icon_sizes = [16,24,32,48]
nav_styles = ['Gui::BlenderNavigationStyle','Gui::CADNavigationStyle','Gui::GestureNavigationStyle',
              'Gui::MayaGestureNavigationStyle','Gui::OpenCascadeNavigationStyle','Gui::InventorNavigationStyle',
              'Gui::OpenSCADNavigationStyle','Gui::RevitNavigationStyle','Gui::TinkerCADNavigationStyle',
              'Gui::TouchpadNavigationStyle']
locales = Gui.supportedLocales()
languages = list(locales.keys())

class FirstRunDialog(QtGui.QDialog):
    def __init__(self):
        super(FirstRunDialog, self).__init__()
        self.ui = Gui.PySideUic.loadUi(os.path.join( modpath, 'Resources', 'OndselFirstRun.ui' ))
        self.setLayout(self.ui.layout())
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    # Define a function to apply preferences
    def apply_preferences(self):
        index = self.ui.Languages.currentIndex()
        params.GetGroup('Preferences/General').SetString('Language',languages[index])
        Gui.setLocale(languages[index])

        index = self.ui.comboBox_UnitSystem.currentIndex()
        params.GetGroup('Preferences/Units').SetInt('UserSchema',index)
        App.Units.setSchema(index)

        index = self.ui.toolbarIconSize.currentIndex()
        params.GetGroup('Preferences/General').SetInt('ToolbarIconSize',icon_sizes[index])
        mw.setIconSize(QtCore.QSize(icon_sizes[index],icon_sizes[index]))

        index = self.ui.comboNavigationStyle.currentIndex()
        params.GetGroup('Preferences/View').SetString('NavigationStyle',nav_styles[index])

        params.GetGroup('Ondsel').SetBool('FirstRunDone', True)
        App.saveParameter()

    def load_preferences(self):
        self.ui.Languages.clear()
        self.ui.Languages.addItems(languages)
        language = params.GetGroup('Preferences/General').GetString('Language', 'English')
        try:
            index = languages.index(language)
        except ValueError:
            index = languages.index('English')
        self.ui.Languages.setCurrentIndex(index)

        index = params.GetGroup('Preferences/Units').GetInt('UserSchema')
        self.ui.comboBox_UnitSystem.setCurrentIndex(index)

        icon_size = params.GetGroup('Preferences/General').GetInt('ToolbarIconSize',24)
        try:
            index = icon_sizes.index(icon_size)
        except ValueError:
            index = 1
        self.ui.toolbarIconSize.setCurrentIndex(index)

        nav_style = params.GetGroup('Preferences/View').GetString('NavigationStyle', 'Gui::BlenderNavigationStyle')
        try:
            index = nav_styles.index(nav_style)
        except ValueError:
            index = 0
        self.ui.comboNavigationStyle.setCurrentIndex(index)

def showFirstRunDialog():
    dialog = FirstRunDialog()
    dialog.load_preferences()
    result = dialog.exec_()

    if result == QtGui.QDialog.Accepted:
        dialog.apply_preferences()

def onStart():
    if mw.property("eventLoop"):
        timer.stop()
        timer.timeout.disconnect(onStart)
        if not params.GetGroup('Ondsel').GetBool('FirstRunDone', False):
            showFirstRunDialog()
        
        with open(os.path.join(modpath,'mods.json'), "r") as fp:
            mods = json.load(fp)

        mw.addon_installers = []
        for mod in mods["addons"]:
            param_path = f'Ondsel/{version}/mods/{mod["name"]}'
            if not params.GetGroup(param_path).GetBool('Installed', False):
                mw.addon_installers.append(install_mod.installer(mod["name"],mod["url"],mod["branch"],param_path))
        for mod in mods["preferencePacks"]:
            param_path = f'Ondsel/{version}/mods/{mod["name"]}'
            if not params.GetGroup(param_path).GetBool('Installed', False):
                mw.addon_installers.append(install_mod.installer(mod["name"],mod["url"],mod["branch"],param_path))

timer = QtCore.QTimer()
timer.timeout.connect(onStart)
timer.start(500)