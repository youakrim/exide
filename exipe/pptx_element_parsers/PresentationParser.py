#!/usr/bin/python
#-*- coding: utf-8 -*-

from .SlideParser import SlideParser


class PresentationParser(object):

    def __init__(self, pythonPPTXPresentationObject):
        self.initial_format = "pptx"
        self.title = pythonPPTXPresentationObject.core_properties.title
        self.author = pythonPPTXPresentationObject.core_properties.author
        self.category = pythonPPTXPresentationObject.core_properties.category
        self.comments = pythonPPTXPresentationObject.core_properties.comments
        self.keywords = pythonPPTXPresentationObject.core_properties.keywords
        self.language = pythonPPTXPresentationObject.core_properties.language
        self.created = pythonPPTXPresentationObject.core_properties.created
        self.last_modified = pythonPPTXPresentationObject.core_properties.modified
        self.subject = pythonPPTXPresentationObject.core_properties.subject
        self.pptx_object = pythonPPTXPresentationObject
        self.slides = self.parse_slides(pythonPPTXPresentationObject)

    def parse_slides(self, pythonPPTXPresentationObject):
        slides = []
        slide_count = 0
        for slide in pythonPPTXPresentationObject.slides:
            slides.append(SlideParser(slide, slide_count, self))
            slide_count += 1
        return slides
