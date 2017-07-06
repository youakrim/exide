#!/usr/bin/python
#-*- coding: utf-8 -*-

from .TextParser import TextParser
from .utils import namespace


class SlideParser(object):

    def __init__(self, XMLSlideObject, number, presentationParser):
        self.presentation = presentationParser
        self.text_parsers = self.parseText(XMLSlideObject)
        self.title_parsers = self.parseTitle(XMLSlideObject)
        self.number = number
        self.layout = None

    def get_style_by_id(self, style_id):
        """
        Return a |StyleParser| matching the given id.

        :param style_id:
        :return: |StyleParser| object.
        """
        return self.presentation.get_style_by_id(style_id)

    def parseText(self, XMLSlideObject):
        """
        Create |TextParser| object for each text of the given XML slide object.

        :param XMLSlideObject: LXML slide object
        :return: List of |TextParser| object.
        """
        text = []
        for frame in XMLSlideObject.findall(".//draw:frame", XMLSlideObject.nsmap):
            if frame not in XMLSlideObject.findall(".//draw:frame[@presentation:class='title']", XMLSlideObject.nsmap):
                for textF in frame.findall(".//text:p", XMLSlideObject.nsmap):
                    style = None
                    if textF.get(namespace(textF)+"style-name") is not None:
                        style_id = textF.get(namespace(textF)+"style-name")
                        style = self.get_style_by_id(style_id)

                    if textF.text is not None:
                        text.append(TextParser(textF, style, self))

                for textF in frame.findall(".//text:span", XMLSlideObject.nsmap):
                    style = None
                    if textF.get(namespace(textF)+"style-name") is not None:
                        style_id = textF.get(namespace(textF)+"style-name")
                        style = self.get_style_by_id(style_id)

                    if textF.text is not None:
                        text.append(TextParser(textF, style, self))

                for textF in frame.findall(".//text:text", XMLSlideObject.nsmap):
                    style = None
                    if textF.get(namespace(textF)+"style-name") is not None:
                        style_id = textF.get(namespace(textF)+"style-name")
                        style = self.get_style_by_id(style_id)

                    if textF.text is not None:
                        text.append(TextParser(textF, style, self))

        return text

    def parseTitle(self, XMLSlideObject):
        """
        Look up for the XML title object within the given XML Slide Object and creates a list of |TextParser| objects for each text within the title.

        :param XMLSlideObject:
        :return:
        """
        title = []
        # On cheche la zone de texte correspondant au titre de la diapositive
        titleFrame = XMLSlideObject.find(".//draw:frame[@presentation:class='title']", XMLSlideObject.nsmap)
        if titleFrame is not None:
            # On cherche le paragraphe qui contiendrait le titre
            for textF in titleFrame.findall(".//text:p", XMLSlideObject.nsmap):
                style = None
                if textF.get(namespace(textF) + "style-name") is not None:
                    style_id = textF.get(namespace(textF) + "style-name")
                    style = self.get_style_by_id(style_id)

                if textF.text is not None:
                    title.append(TextParser(textF, style, self))
            # On cherche le span qui contiendrait le titre
            for textF in titleFrame.findall(".//text:span", XMLSlideObject.nsmap):
                style = None
                if textF.get(namespace(textF)+"style-name") is not None:
                    style_id = textF.get(namespace(textF)+"style-name")
                    style = self.get_style_by_id(style_id)
                if textF.text is not None:
                    title.append(TextParser(textF, style, self))
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
        for text in self.text_parsers:
            if text.style_id == styleID:
                texts.append(text)
        return texts

    @property
    def text(self):
        """
        Return a string containing all the body text of the slide.

        :return: Strinf
        """
        text=""
        for tp in self.text_parsers:
            text+="\n"+tp.text
        return text

    @property
    def title(self):
        """
        Retrun a string containing the title of the slide.

        :return: String
        """
        if len(self.title_parsers) > 0:
            text=""
            for tp in self.title_parsers:
                text+=tp.text
            return text
