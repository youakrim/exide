#!/usr/bin/python
#-*- coding: utf-8 -*-

from exipe.odp_element_parsers.SlideParser import SlideParser
from exipe.odp_element_parsers.StyleGroup import StyleGroup
from exipe.odp_element_parsers.StyleParser import StyleParser


class PresentationParser(object):

    def __init__(self, XMLPresentationObject):
        self.slides = self.parseSlides(XMLPresentationObject)
        #self.styles = self.parseStyles(XMLPresentationObject)
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
            nouveau_style = StyleParser(style, self)
            if nouveau_style.countOccurences() > 0:
                styles.append(nouveau_style)
        return styles

    def get_style_by_id(self, style_id):
        for style in self.styles:
            if style.id == style_id:
                return style
        return None