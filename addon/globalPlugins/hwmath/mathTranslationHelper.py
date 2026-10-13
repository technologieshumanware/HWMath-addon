# BrailleNoteEvolve add-on
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# Copyright (C) 2026 Technologies Humanware

#store pairs of mathml / brl strings

from logHandler import log


class MathTranslationHelper:

    mTranslations : dict
       
    #private final Map<String,String> mTranslations; //MathMl , Braille

    def __init__(self):
        self.mTranslations = dict()
        log.warning("MathTranslationHelper init")

 
    def add( self, mathml, braille):
        self.mTranslations[mathml] = braille
        print(self.mTranslations.values)
        
    def get(self, mathml):
        log.info("checking translation for %s", mathml)
        return self.mTranslations.get(mathml)




