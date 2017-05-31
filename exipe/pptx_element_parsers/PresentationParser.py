#!/usr/bin/python
#-*- coding: utf-8 -*-

from exipe.pptx_element_parsers.SlideParser import SlideParser


class PresentationParser(object):

    def __init__(self, pythonPPTXPresentationObject):
        self.pptx_object = pythonPPTXPresentationObject
        self.slides = self.parseSlides(pythonPPTXPresentationObject)
        #self.styleGroups = self.mergeSimilarStyles()

    def parseSlides(self, pythonPPTXPresentationObject):
        slides = []
        slide_count = 0
        for slide in pythonPPTXPresentationObject.slides:
            slides.append(SlideParser(slide, slide_count, self))
            slide_count += 1
        return slides