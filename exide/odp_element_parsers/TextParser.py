#!/usr/bin/python
#-*- coding: utf-8 -*-


class TextParser(object):

    def __init__(self, XMLTextObject, style, slide):
        self.xml_object = XMLTextObject
        self.slide = slide
        self.style = style

    @property
    def text(self):
        if self.xml_object.text is not None:
            return self.xml_object.text
        return ""

    @property
    def font_weight(self):
        if self.style is not None:
            return self.style.font_weight
        else:
            return "default"

    @property
    def underlined(self):
        if self.style is not None:
            return self.style.underlined
        return "default"

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
        return "default"

    @property
    def color(self):
        if self.style is not None:
            return self.style.font_color
        return "default"

