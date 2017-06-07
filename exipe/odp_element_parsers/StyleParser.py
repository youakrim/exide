#!/usr/bin/python
#-*- coding: utf-8 -*-
from .utils import namespace


class StyleParser(object):
    NS = "{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}"

    def __init__(self, id, type, XMLStyleObject, presentation):
        self.xml_style = XMLStyleObject
        self.type = type
        self.id = id
        self.presentation = presentation

    @property
    def font_family(self):
        if self.type == "fontspec":
            if "family" in self.xml_style.attrib:
                return self.xml_style.attrib["family"]
            else:
                return ""
        elif self.type == "text-properties":
            if namespace(self.xml_style)+"font-name" in  self.xml_style.attrib:
                return self.xml_style.attrib[namespace(self.xml_style)+"font-name"]
            else:
                return ""
        return ""

    @property
    def font_size(self):
        if self.type == "fontspec":
            if "size" in self.xml_style.attrib:
                return self.xml_style.attrib["size"]
            else:
                return ""
        elif self.type == "text-properties":
            if StyleParser.NS+"font-size" in  self.xml_style.attrib:
                return self.xml_style.attrib[StyleParser.NS+"font-size"]
            else:
                return ""
        return ""

    @property
    def font_color(self):
        if self.type == "fontspec":
            if "color" in self.xml_style.attrib:
                return self.xml_style.attrib["color"]
            else:
                return ""
        elif self.type == "text-properties":
            if StyleParser.NS+"color" in self.xml_style.attrib:
                return self.xml_style.attrib[StyleParser.NS+"color"]
            else:
                return ""
        return ""

    @property
    def font_weight(self):
        if self.type == "fontspec":
            if "weight" in self.xml_style.attrib:
                return self.xml_style.attrib["weight"]
            else:
                return ""
        elif self.type == "text-properties":
            if StyleParser.NS + "font-weight" in self.xml_style.attrib:
                return self.xml_style.attrib[StyleParser.NS + "font-weight"]
            else:
                return ""
        return ""

    @property
    def underlined(self):
        if self.type == "fontspec":
            if "underline" in self.xml_style.attrib:
                return self.xml_style.attrib["underline"]
            else:
                return "default"
        elif self.type == "text-properties":
            if namespace(self.xml_style)+"text-underline-style" in  self.xml_style.attrib:
                return self.xml_style.attrib[namespace(self.xml_style)+"text-underline-style"]
            else:
                return "default"
        return ""
