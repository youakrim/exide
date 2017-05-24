#!/usr/bin/python
#-*- coding: utf-8 -*-

from exipe.odp_element_parsers.SlideParser import SlideParser
from exipe.odp_element_parsers.StyleGroup import StyleGroup
from exipe.odp_element_parsers.StyleParser import StyleParser
from exipe.odp_element_parsers.utils import namespace


class PresentationParser(object):

    def __init__(self, XMLPresentationObject):
        self.styles = self.parseStyles(XMLPresentationObject)
        print self.styles
        self.slides = self.parseSlides(XMLPresentationObject)
        #self.styleGroups = self.mergeSimilarStyles()

    # On cherche à extraire les texte d'un certain style
    def getTextsByStyleId(self, styleID):
        #TODO
        texts = []
        # On parcourt les slides et pour chaque slide, on récupère le nombre de textes ayant le style
        for slide in self.slides:
            for text in slide.getTextsByStyleId(styleID):
                texts.append(text)
        return texts

    def parseSlides(self, XMLPresentationObject):
        slides = []
        slideCount=0
        for slide in XMLPresentationObject.findall(".//draw:page", XMLPresentationObject.nsmap):
            slides.append(SlideParser(slide, slideCount, self))
            slideCount+=1
        return slides

    def parseStyles(self, XMLPresentationObject):
        styles = []
        for style in XMLPresentationObject.findall(".//fontspec", XMLPresentationObject.nsmap):
            type="fontspec"
            nouveau_style = StyleParser(style.attrib["id"], type, style, self)
            if nouveau_style.countOccurences() > 0:
                styles.append(nouveau_style)
        print "text-properties"
        for XMLStyle in XMLPresentationObject.findall(".//style:style", XMLPresentationObject.nsmap):
            if namespace(XMLStyle)+"name" in XMLStyle.attrib:
                id = XMLStyle.attrib[namespace(XMLStyle)+"name"]
            else:
                id=""
            for textProperties in XMLStyle.findall(".//style:text-properties", XMLPresentationObject.nsmap):
                type = "text-properties"
                nouveau_style = StyleParser(id, type, textProperties, self)
                styles.append(nouveau_style)
        return styles

    def get_style_by_id(self, style_id):
        for style in self.styles:
            if style.id == style_id:
                return style
        return None