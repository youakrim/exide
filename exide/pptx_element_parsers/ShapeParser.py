#!/usr/bin/python
#-*- coding: utf-8 -*-


class ShapeParser(object):

    def __init__(self, PPTXShapeObject, slide):
        self.pptx_objet = PPTXShapeObject
        self.slide = slide

    @property
    def text(self):
        if hasattr(self.pptx_objet, "text") and self.pptx_objet.text is not None:
            return self.pptx_objet.text
        return ""

    @property
    def font_weight(self):
        return "default"

    @property
    def underlined(self):
        return "default"

    @property
    def font_family(self):
        return "default"

    @property
    def font_size(self):
        return "default"

    @property
    def color(self):
        return "default"
