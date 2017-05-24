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

    '''def fastSorting(tab, left, right):
        if right > left:
            pivot = (left+right)/2
            tmp = tab[left]
            tab[left] = tab[pivot]
            tab[pivot] = tmp
            pivot = left
            for i in range(left+1, right):
                if tab[i]["occurences"] < tab[left]["occurences"]:
                    pivot+=1
                    tmp = tab[i]
                    tab[i] = tab[pivot]
                    tab[pivot] = tmp
                    tri_rapide(tab, left, pivot-1)
                    tri_rapide(tab, pivot+1, right)
    '''

    def parseSlides(self, XMLPresentationObject):
        slides = []
        slideCount=0
        for slide in XMLPresentationObject.findall(".//draw:page", XMLPresentationObject.nsmap):
            slides.append(SlideParser(slide, slideCount, self))
            slideCount+=1
        return slides


    def getExampleSlides(self):
        ex_slides = []
        for slide in self.slides:
            if slide.isAnExample():
                ex_slides.append(slide)
        return ex_slides

    def getToCSlides(self):
        toc_slides = []
        for slide in self.slides:
            if slide.isAToC():
                toc_slides.append(slide)
        return toc_slides

    def getConclusionSlides(self):
        toc_slides = []
        for slide in self.slides:
            if slide.isAConclusion():
                toc_slides.append(slide)
        return toc_slides

    def getIntroductionSlides(self):
        toc_slides = []
        for slide in self.slides:
            if slide.isAnIntroduction():
                toc_slides.append(slide)
        return toc_slides

    def getReferencesSlides(self):
        toc_slides = []
        for slide in self.slides:
            if slide.isReferences():
                toc_slides.append(slide)
        return toc_slides

    def getDefinitionSlides(self):
        toc_slides = []
        for slide in self.slides:
            if slide.isADefinition():
                toc_slides.append(slide)
        return toc_slides

    def parseStyles(self, XMLPresentationObject):
        #TODO
        styles = []
        for style in XMLPresentationObject.findall(".//fontspec", XMLPresentationObject.nsmap):
            nouveau_style = StyleParser(style, self)
            if nouveau_style.countOccurences() > 0:
                styles.append(nouveau_style)
        return styles

    def mergeSimilarStyles(self):
        #TODO
        input_styles = self.styles[:]
        output_style_groups = []
        # Pour chaque style on cherche si il existe des styles similaires
        for style in input_styles:
            # On retire l'élément de la liste pour ne pas qu'il soit comparé plusieurs fois
            input_styles.remove(style)
            style_group = StyleGroup(self)
            style_group.styles.append(style)
            for style2 in input_styles:
                if style2.isSimilarTo(style):
                    # On retire l'élément de la liste pour ne pas qu'il soit comparé plusieurs fois
                    input_styles.remove(style2)
                    # On l'ajoute au groupe de style
                    style_group.styles.append(style2)
            output_style_groups.append(style_group)
        return output_style_groups