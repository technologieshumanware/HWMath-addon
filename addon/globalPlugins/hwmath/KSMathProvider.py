# BrailleNoteEvolve add-on
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# Copyright (C) 2026 Technologies Humanware


from logHandler import log

import mathPres
import sys
import os
from core import postNvdaStartup
from gui.message import MessageDialog, DialogType
sys.path.append(os.path.join(os.path.dirname(__file__),"."))

initSuccess = True

def showError(message: str):
    dialog = MessageDialog(
        parent=None,
        message=message,
        #Translators: dialog title when announcing an error
        title=_("HWMath Error"),
        dialogType=DialogType.ERROR
    )
    dialog.Show()

def checkInitFailed():
    if not initSuccess:
        # Translators: This is a label to inform the user this addon could not be loaded correctly
        showError(_("HWMath Add-on could not be loaded correctly."))

try:
    # If initialization failed, show an error dialog when nvda is ready
    postNvdaStartup.register(checkInitFailed)

    pythonnet_path = os.path.dirname(os.path.realpath(__file__)) + '\\pythonnet'
    if sys.path.count(pythonnet_path) > 0:
        print(pythonnet_path + " already inserted")
    else:
        sys.path.insert(0, pythonnet_path)

    import pythonnet
    pythonnet.load("coreclr")
    import clr

    translationlib_path = os.path.dirname(os.path.realpath(__file__)) + '\\WebDriverLib'
    if sys.path.count(translationlib_path) > 0:
        print(translationlib_path + " already inserted")
    else:
        sys.path.insert(0, translationlib_path)

    clr.AddReference('WebDriverLib')

    from WebDriverLib import Services

except Exception as e:
    log.error(f"Unable to load WebDriverLib: {e}")
    initSuccess = False

class KSMathProvider(mathPres.MathPresentationProvider):
    
    try :
        mathProviderService = Services.MathProviderService()
    except Exception as e:
        log.error(f"Unable to resolve MathProviderService: {e}")
        initSuccess = False

    def init(self):
        log.warning("KSMathProvider init")

    def terminate(self):
        self.mathProviderService.CloseAndDisposeChromeDriver()

    def getSpeechForMathMl(self, mathMl):
        """Get speech output for specified MathML markup.
        @param mathMl: The MathML markup.
        @type mathMl: str
        @return: A speech sequence.
        @rtype: List[str, SpeechCommand]
        """
        try:
            log.info(f"Get speech from mathML expression: {mathMl}")
            return [self.mathProviderService.GetSpeechForMathML(mathMl)]
        except Exception as e:
            log.error(f"Could not get speech from mathMl input: {e}")
            return ""

    def getBrailleForMathMl(self, mathMl):
        """Get braille output for specified MathML markup.
        @param mathMl: The MathML markup.
        @type mathMl: str
        @return: A string of Unicode braille.
        @rtype: unicode
        """
        try:
            log.info(f"Get braille form mathML expression: {mathMl}")
            return self.mathProviderService.GetBrailleFromMathML(mathMl)
        except Exception as e:
            log.error(f"Could not get braille from mathMl input: {e}")   

    def interactWithMathMl(self, mathMl):
        """Begin interaction with specified MathML markup.
        @param mathMl: The MathML markup.
        """
        # That's where we can plug our editor, have buttons to send to KeyMath, etc...
        # first, we might need another pass at getting the braille, (we probably just did it a moment ago...
        # so a translation helper would save a bit of CPU)
        log.warning("interactWithMathMl not available yet")
        # let's say we pop up an editor
        # prefill the braille
        # allow native braille editing
        # browse/insert symbols / templates
        # export to clipboard
        # announce expression
        # not sure if we can replace expression under cursor without going through clipboard
        # send to keymaths for graphing
        #
