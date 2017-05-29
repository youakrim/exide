#!/usr/bin/python
#-*- coding: utf-8 -*-

class TextParser(object):

    def __init__(self, PPTXTextObject, slide):
        self.pptx_objet = PPTXTextObject
        self.slide = slide

    @property
    def text(self):
        if self.pptx_objet.text is not None:
            return self.pptx_objet.text
        else:
            return ""

    @property
    def font_weight(self):
        if self.pptx_objet.font.bold:
            return "bold"
        else:
            return "default"
        pass

    @property
    def underlined(self):
        return self.pptx_objet.font.underline

    @property
    def font_family(self):
        if self.pptx_objet.font.name is not None:
            return self.pptx_objet.font.name
        return "default"

    @property
    def font_size(self):
        if self.pptx_objet.font.size is not None:
            return self.pptx_objet.font.size
        return "default"

    @property
    def color(self):
        if self.pptx_objet.font.color.type is not None:
            # print run.font.color.type
            if "RGB" in str(self.pptx_objet.font.color.type):
                return self.pptx_objet.font.color.rgb
            elif "SCHEME" in str(self.pptx_objet.font.color.type):
                return "default"
        return "default"
