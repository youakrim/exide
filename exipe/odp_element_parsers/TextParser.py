#!/usr/bin/python
#-*- coding: utf-8 -*-

class TextParser(object):
    """docstring for TextParser"""
    EXAMPLE_STRINGS = ("ex ", "ex.", "ex:", "exemple", "eg ", "e. g.", "e.g.")

    def __init__(self, XMLTextObject, pseudoType, style_id, slide):
        self.content = self.getContent(XMLTextObject)
        self.slide = slide
        self.style_id = style_id
        self.pseudoType = pseudoType

    def getContent(self, XMLTextObject):
        if XMLTextObject.text is not None:
            return XMLTextObject.text
        else:
            return ""

    def isAnExample(self):
        return self.content.lower().startswith(self.EXAMPLE_STRINGS)