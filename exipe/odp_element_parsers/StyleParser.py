#!/usr/bin/python
#-*- coding: utf-8 -*-


class StyleParser(object):

    def __init__(self, XMLStyleObject, presentation):
        self.id = XMLStyleObject.attrib["id"]
        self.font_size = int(XMLStyleObject.attrib["size"])
        self.font_family = XMLStyleObject.attrib["family"]
        self.font_color = XMLStyleObject.attrib["color"]
        self.presentation = presentation