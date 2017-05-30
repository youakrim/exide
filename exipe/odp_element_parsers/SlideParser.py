#!/usr/bin/python
#-*- coding: utf-8 -*-

from exipe.odp_element_parsers.TextParser import TextParser
from exipe.odp_element_parsers.utils import namespace


class SlideParser(object):

    def __init__(self, XMLSlideObject, number, presentationParser):
        self.presentation = presentationParser
        self.text_parsers = self.parseText(XMLSlideObject)
        self.title_parsers = self.parseTitle(XMLSlideObject)
        self.number = number

    def get_style_by_id(self, style_id):
        return self.presentation.get_style_by_id(style_id)

    def parseText(self, XMLSlideObject):
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
        texts = []
        # On parcourt les textes et pour chaque texte, on vérifie si il a le style recherché
        for text in self.text_parsers:
            if text.style_id == styleID:
                texts.append(text)
        return texts

    def mergeSameLineTexts(self):
        input_texts = self.text_parsers
        output_text=[]
        for text in input_texts:
            input_texts.remove(text)
            for text2 in input_texts:
                if text.top == text2.top and text.style_id == text2.style_id:
                    input_texts.remove(text2)
                    text.text+=text2.text
            output_text.append(text)
        return output_text

    @property
    def text(self):
        text=""
        for tp in self.text_parsers:
            text+="\n"+tp.text
        return text

    @property
    def title(self):
        text=""
        for tp in self.title_parsers:
            text+=tp.text
        return text
