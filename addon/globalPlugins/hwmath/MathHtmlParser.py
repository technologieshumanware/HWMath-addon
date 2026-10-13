# BrailleNoteEvolve add-on
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# Copyright (C) 2026 Technologies Humanware

import re
from logHandler import log

class MathJaxSnippetLanguage:

    @staticmethod
    def updateMathJaxSnippetContentWithLanguage(path, language):
        locale = "locale:"
        lines = MathJaxSnippetLanguage.getLinesFromHtmlFile(path)
        if lines.__len__() == 0:
            # lines is empty
            log.warning("getLinesFromHtmlFile is empty")
            return

        newLines = []

        for line in lines:
            if locale in line:
                # ex: locale: 'en'
                previousLanguage = re.findall(r'(?<=\').*?(?=\')', line)
                if previousLanguage.__len__() > 0:
                    if previousLanguage.count(language) > 0:
                        # Already the good language, we don't need to update the language
                        log.debug("already the right language %s" %language)
                        return
                    line = re.sub(previousLanguage[0], language, line)
            newLines.append(line)

        html = ''.join(newLines)
        MathJaxSnippetLanguage.writeHtmlFileFromHtmlContent(path, html)

    @staticmethod
    def getLinesFromHtmlFile(path):
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                return file.readlines()
        except IOError:
            log.error("Invalid path: %s" % path)
            return []

    @staticmethod
    def writeHtmlFileFromHtmlContent(path, htmlContent):
        with open(path, mode='w', encoding='utf-8') as file:
            file.write(htmlContent)
            log.debug("file written")

