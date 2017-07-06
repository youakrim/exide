#!/usr/bin/python
#-*- coding: utf-8 -*-

from .TextParser import TextParser
from .ShapeParser import ShapeParser

class SlideParser(object):

    def __init__(self, PPTXSlideObject, number, presentationParser):
        self.presentation = presentationParser
        self.text_parsers = self.parseText(PPTXSlideObject)
        self.title_parsers = self.parseTitle(PPTXSlideObject)
        self.number = number
        self.pptx_object = PPTXSlideObject
        self.layout = PPTXSlideObject.slide_layout


    def parseText(self, PPTXSlideObject):
        """
        Create |TextParser| object for each text of the given XML slide object.

        :param XMLSlideObject: LXML slide object
        :return: List of |TextParser| object.
        """
        text = []
        for shape in PPTXSlideObject.shapes:
            if hasattr(shape, "text") and shape.text is not None and shape not in PPTXSlideObject.shapes.placeholders:
                text.append(ShapeParser(shape, self))
        for shape in PPTXSlideObject.shapes.placeholders:
            if PPTXSlideObject.shapes.title is not None:
                if PPTXSlideObject.shapes.title.shape_id != shape.shape_id:
                    if not shape.has_text_frame:
                        continue
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            text.append(TextParser(run, self))
            else:
                if not shape.has_text_frame:
                    continue
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        text.append(TextParser(run, self))
        return text

    def parseTitle(self, PPTXSlideObject):
        """
        Look up for the XML title object within the given XML Slide Object and creates a list of |TextParser| objects for each text within the title.

        :param XMLSlideObject:
        :return:
        """
        title = []
        for shape in PPTXSlideObject.shapes.placeholders:
            if PPTXSlideObject.shapes.title is not None:
                if PPTXSlideObject.shapes.title.shape_id == shape.shape_id:
                    if not shape.has_text_frame:
                        continue
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            title.append(TextParser(run, self))
        return title

    # On cherche à extraire les textes d'un certain style
    def getTextsByStyleId(self, styleID):
        """
        Return a list of |TextParser| objects whose style matches the given style ID.

        :param styleID: ID of a |StyleParser|
        :return: List of |TextParser| objects.
        """
        texts = []
        # On parcourt les textes et pour chaque texte, on vérifie si il a le style recherché
        for text in self.text:
            if text.style_id == styleID:
                texts.append(text)
        return texts

    @property
    def text(self):
        """
        Return a string containing all the body text of the slide.

        :return: String
        """
        text=""
        for tp in self.text_parsers:
            text+="\n"+tp.text
        return text

    @property
    def title(self):
        """
        Return a string containing the title of the slide.

        :return: String
        """
        if self.pptx_object.shapes.title is not None:
            return self.pptx_object.shapes.title.text
        return None
