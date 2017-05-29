#!/usr/bin/python
#-*- coding: utf-8 -*-

class TextParser(object):

    def __init__(self, XMLTextObject, pseudoType, style, slide):
        self.xml_object = XMLTextObject
        self.slide = slide
        self.style = style
        self.pseudoType = pseudoType

    @property
    def text(self):
        if self.xml_object.text is not None:
            return self.xml_object.text
        else:
            return ""

    @property
    def font_weight(self):
        if self.style is not None:
            return self.style.font_weight
        else:
            return "default"

    @property
    def underlined(self):
        #TODO
        pass

    @property
    def font_family(self):
        #TODO
        pass

    @property
    def font_size(self):
        #TODO
        pass

    @property
    def color(self):
        #TODO
        pass
