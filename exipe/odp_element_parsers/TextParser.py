#!/usr/bin/python
#-*- coding: utf-8 -*-

class TextParser(object):
    """docstring for TextParser"""
    EXAMPLE_STRINGS = ("ex ", "ex.", "ex:", "exemple", "eg ", "e. g.", "e.g.")

    def __init__(self, XMLTextObject, pseudoType, style, slide):
        self.content = self.getContent(XMLTextObject)
        self.slide = slide
        self.style = style
        self.pseudoType = pseudoType
        if style is not None:
            print style.font_color
            print style.font_family
            print style.font_weight
        else:
            print None

    def getContent(self, XMLTextObject):
        if XMLTextObject.text is not None:
            return XMLTextObject.text
        else:
            return ""

    @property
    def bold(self):
        pass

    @property
    def underlined(self):
        pass

    @property
    def font_family(self):
        pass

    @property
    def font_size(self):
        pass

    @property
    def color(self):
        pass
