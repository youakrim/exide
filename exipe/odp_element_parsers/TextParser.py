#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
            print style.font_color
            print style.font_family
            print style.font_weight
            print style.font_size'''


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
        return ""

    @property
    def font_family(self):
        if self.style is not None:
            return self.style.font_family
        else:
            return "default"
        pass

    @property
    def font_size(self):
        if self.style is not None:
            return self.style.font_size
        else:
            return "default"

    @property
    def color(self):
        if self.style is not None:
            return self.style.font_color
        else:
            return "default"
        pass
