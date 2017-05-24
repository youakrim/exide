#!/usr/bin/python
#-*- coding: utf-8 -*-

from exipe.odp_element_parsers.ElementParser import ElementParser
from exipe.odp_element_parsers.StyleGroup import StyleGroup
from exipe.odp_element_parsers.StyleParser import StyleParser


class ElementGroup(object):

    def __init__(self, presentation):
        self.elements=[]
        self.presentation = presentation
        #self.styles = self.parseStyles(XMLPresentationObject)
        #self.styleGroups = self.mergeSimilarStyles()

    def getConclusionElements(self):
        toc_elements = []
        for element in self.elements:
            if element.isAConclusion():
                toc_elements.append(element)
        return toc_elements
    
    def getDefinitionElements(self):
        toc_elements = []
        for element in self.elements:
            if element.isADefinition():
                toc_elements.append(element)
        return toc_elements
    
    def getExampleElements(self):
        ex_elements = []
        for element in self.elements:
            if element.isAnExample():
                ex_elements.append(element)
        return ex_elements
    
    def getIntroductionElements(self):
        toc_elements = []
        for element in self.elements:
            if element.isAnIntroduction():
                toc_elements.append(element)
        return toc_elements

    def getReferencesElements(self):
        toc_elements = []
        for element in self.elements:
            if element.isReferences():
                toc_elements.append(element)
        return toc_elements

    def getToCElements(self):
        toc_elements = []
        for element in self.elements:
            if element.isAToC():
                toc_elements.append(element)
        return toc_elements

    def isAConclusion(self):
        #TODO
        return False

    def isADefinition(self):
        #TODO
        return False

    def isAnExample(self):
        #TODO
        return False

    def isAnIntroduction(self):
        #TODO
        return False

    def isReferences(self):
        #TODO
        return False

    def isAToC(self):
        #TODO
        return False

