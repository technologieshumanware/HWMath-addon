# BrailleNoteEvolve add-on
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# Copyright (C) 2026 Technologies Humanware

# entry point for HWMath
import mathPres
from .KSMathProvider import KSMathProvider

import addonHandler
import globalPluginHandler
import globalCommands
import wx
import config
import winreg
from scriptHandler import script

import gui
from gui.settingsDialogs import SettingsPanel, NVDASettingsDialog

from logHandler import log
from globalCommands import SCRCAT_CONFIG
from typing import Callable

addonHandler.initTranslation()
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

addonHandler.initTranslation()
_: Callable[[str], str]

reader = KSMathProvider()
reader.init()
mathPres.registerProvider(reader, speech=True, braille=True, interaction=True)

# Constants for math codes (must match HWMath addon)
MATH_CODE_NEMETH = "Nemeth"
MATH_CODE_UEB = "UEB"
MATH_CODE_FR = "FR"

MATH_CODE_MAP = {
	# Translators: Math code choice for Nemeth Braille			
    _("Nemeth"): MATH_CODE_NEMETH,
	# Translators: Math code choice for Unified English Braille (UEB)
    _("UEB"): MATH_CODE_UEB,
	# Translators: Math code choice for French Braille
    _("FR"): MATH_CODE_FR
}

def getLocalizedMathCode(constant):
    """Get localized label for math code constant."""
    for label, const in MATH_CODE_MAP.items():
        if const == constant:
            return label
    return next(iter(MATH_CODE_MAP.keys()))

instanceGP = None

confspec = {
    "mathCodeChoice": 'string(default="Nemeth")',
}

config.conf.spec["HWMath"] = confspec


class AddonSettingsPanel(SettingsPanel):

    title = ADDON_SUMMARY

    def makeSettings(self, settingsSizer):
        self._math_code_choices = list(MATH_CODE_MAP.keys())
        # Translators: This is the label for a combobox in the addon settings panel.
        self._math_code_title = _("Braille code for MathML content:")
        braille_settings_gui_helper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

        self._math_code_choice = braille_settings_gui_helper.addLabeledControl(self._math_code_title, wx.Choice, choices=self._math_code_choices)
        cur_choice = getLocalizedMathCode(config.conf["HWMath"]["mathCodeChoice"])
        
        for index, name in enumerate(self._math_code_choices):
            if name == cur_choice:
                self._math_code_choice.SetSelection(index)
                break
            else:
                log.debugWarning("Could not set _math_code_choices list to current  setting")

    def postInit(self):
        self._math_code_choice.SetFocus()

    def onSave(self):
        config.conf["HWMath"]["mathCodeChoice"] =  MATH_CODE_MAP[self._math_code_choices[self._math_code_choice.GetSelection()]]
        instanceGP._saveSettingToRegistry()
        
        




class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = globalCommands.SCRCAT_BRAILLE

    def __init__(self):
        log.debug("HWMath plugin init-")
        global instanceGP
        super().__init__()
        instanceGP = self
        self.isEnabled = False
        self._saveSettingToRegistry()
        NVDASettingsDialog.categoryClasses.append(AddonSettingsPanel)

    def _saveSettingToRegistry(self):
        # Write that in registry for other apps to access it
        registry_key = r"SOFTWARE\Humanware\Settings"
        value = config.conf["HWMath"]["mathCodeChoice"] 
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_key) as k:
            winreg.SetValueEx(k, "MathBrailleCode", None, winreg.REG_SZ, value )



    def onSettings(self, evt):
        gui.mainFrame.popupSettingsDialog(NVDASettingsDialog, AddonSettingsPanel)

    @script(
        # Translators: Describes a command.
        description=_("Shows the %s settings.") % ADDON_SUMMARY,
        category=SCRCAT_CONFIG
    )
    def script_settings(self, gesture):
        wx.CallAfter(self.onSettings, None)

    def handleConfigProfileSwitch(self):
        if self.isEnabled:
            self.disable()
            self.enable()

    def terminate(self):
        reader.terminate()
        self.disable()
        NVDASettingsDialog.categoryClasses.remove(AddonSettingsPanel)

    def enable(self):
        if self.isEnabled:
            return
        self.isEnabled = True

    def disable(self):
        if not self.isEnabled:
            return False
        self.isEnabled = False
