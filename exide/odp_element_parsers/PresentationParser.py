#!/usr/bin/python
#-*- coding: utf-8 -*-

from .SlideParser import SlideParser
from .StyleParser import StyleParser
from .utils import namespace


class PresentationParser(object):

    def __init__(self, XMLPresentationObject, XMLMeta):
        self.initial_format = "odp"
        self.xml_meta = XMLMeta
        self.styles = self.parseStyles(XMLPresentationObject)
        self.slides = self.parseSlides(XMLPresentationObject)
        self.category = ""
        self.comments = ""
        self.keywords = ""
        self.language = ""
        self.subject = ""

    @property
    def title(self):
        """
        Title of the presentation
        :return: String containing the title of the presentation or None if no title was found
        """
        if self.xml_meta.find(".//dc:title", self.xml_meta.nsmap):
            return self.xml_meta.find(".//dc:title", self.xml_meta.nsmap).text
        return None

    @property
    def author(self):
        """
        Author of the presentation
        :return: String containing the author name of the presentation or None if no author name was found
        """
        if self.xml_meta.find(".//meta:initial-creator", self.xml_meta.nsmap):
            return self.xml_meta.find(".//meta:initial-creator", self.xml_meta.nsmap).text
        return None

    @property
    def last_modifier(self):
        """
        Name of the last person who edited the presentation
        :return: String containing the last editor's name or None if no name was found
        """
        if self.xml_meta.find(".//dc:creator", self.xml_meta.nsmap):
            return self.xml_meta.find(".//dc:creator", self.xml_meta.nsmap).text
        return None

    @property
    def last_modified(self):
        """
        Date of the last edit of the presentation
        :return: String containing the last edition date or None if no date was found
        """
        if self.xml_meta.find(".//dc:date", self.xml_meta.nsmap):
            return self.xml_meta.find(".//dc:date", self.xml_meta.nsmap).text
        return None

    @property
    def created(self):
        """
        Date of creation of the presentation
        :return: String containing the date of creation or None if no date was found
        """
        if self.xml_meta.find(".//meta:creation-date", self.xml_meta.nsmap):
            return self.xml_meta.find(".//meta:creation-date", self.xml_meta.nsmap).text
        return None

    # On cherche à extraire les texte d'un certain style
    def getTextsByStyleId(self, styleID):
        """
        Get all |TextParser| of a given style.
        :param styleID: Id of the style
        :return: A list of |TextParser|
        """
        #TODO
        texts = []
        # On parcourt les slides et pour chaque slide, on récupère le nombre de textes ayant le style
        for slide in self.slides:
            for text in slide.getTextsByStyleId(styleID):
                texts.append(text)
        return texts

    def parseSlides(self, XMLPresentationObject):
        """
        Create |SlideParser| object of each slide of the presentation

        :param XMLPresentationObject:
        :return:
        """
        slides = []
        slideCount=0
        for slide in XMLPresentationObject.findall(".//draw:page", XMLPresentationObject.nsmap):
            slides.append(SlideParser(slide, slideCount, self))
            slideCount+=1
        return slides

    def parseStyles(self, XMLPresentationObject):
        """
        Create a |StyleParser| object of each style of the presentation.

        :param XMLPresentationObject: LXML presentation object
        :return: list of |StyleParser| objects
        """
        styles = []
        for style in XMLPresentationObject.findall(".//fontspec", XMLPresentationObject.nsmap):
            type="fontspec"
            nouveau_style = StyleParser(style.attrib["id"], type, style, self)
            if nouveau_style.countOccurences() > 0:
                styles.append(nouveau_style)
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
        """
        Return a |StyleParser| object matching the given ID.

        :param style_id:
        :return: |StyleParser| object or None if no matching style was found.
        """
        for style in self.styles:
            if style.id == style_id:
                return style
        return None