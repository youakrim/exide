#!/usr/bin/python
#-*- coding: utf-8 -*-

from exipe.odp_element_parsers.TextParser import TextParser
from exipe.odp_element_parsers.utils import namespace


class SlideParser(object):

    TABLE_OF_CONTENTS_STRINGS = ("plan", "sommaire", "table des matières")
    CONCLUSION_STRINGS = ("conclu", "synthese", "resum")
    INTRODUCTION_STRINGS = ("intro", "présentation", "préambule")
    EXAMPLE_STRINGS = ("ex ", "ex.", "ex:", "exem", "examp", "eg ", "e. g.", "e.g.")
    REFERENCES_STRINGS = ("references", "biblio", "références", "refs", "sources", "liens")
    DEFINITION_STRINGS = ("def", "déf")

    def __init__(self, XMLSlideObject, number, presentationParser):
        self.bodyText = self.parseText(XMLSlideObject)
        self.title = self.parseTitle(XMLSlideObject)
        self.presentation = presentationParser
        self.number = number

    def parseText(self, XMLSlideObject):
        text = []
        # On récupère d'abord les paragraphes dont la classe de l'élément draw parent est outline
        for frame in XMLSlideObject.findall(".//draw:frame", XMLSlideObject.nsmap):
            for textF in frame.findall(".//text:p", XMLSlideObject.nsmap):
                style = ""
                if textF.get(namespace(textF)+"style-name") is not None:
                    style = textF.get(namespace(textF)+"style-name")

                if textF.text is not None:
                    text.append(TextParser(textF, "outline", style, self))

            for textF in frame.findall(".//text:span", XMLSlideObject.nsmap):
                style = ""
                if textF.get(namespace(textF)+"style-name") is not None:
                    style = textF.get(namespace(textF)+"style-name")

                if textF.text is not None:
                    text.append(TextParser(textF, "outline", style, self))

            for textF in frame.findall(".//text:text", XMLSlideObject.nsmap):
                style = ""
                if textF.get(namespace(textF)+"style-name") is not None:
                    style = textF.get(namespace(textF)+"style-name")

                if textF.text is not None:
                    text.append(TextParser(textF, "outline", style, self))

        return text

    def parseTitle(self, XMLSlideObject):
        title = []
        # On cheche la zone de texte correspondant au titre de la diapositive
        titleFrame = XMLSlideObject.find(".//draw:frame[@presentation:class='title']", XMLSlideObject.nsmap)
        if titleFrame is not None:
            # On cherche le paragraphe qui contiendrait le titre
            for textF in titleFrame.findall(".//text:p", XMLSlideObject.nsmap):
                style = ""
                if textF.get(namespace(textF)+"style-name") is not None:
                    style = textF.get(namespace(textF)+"style-name")
                if textF.text is not None:
                    title.append(TextParser(textF, "title", style, self))
            # On cherche le span qui contiendrait le titre
            for textF in titleFrame.findall(".//text:span", XMLSlideObject.nsmap):
                style = ""
                if textF.get(namespace(textF)+"style-name") is not None:
                    style = textF.get(namespace(textF)+"style-name")
                if textF.text is not None:
                    title.append(TextParser(textF, "title", style, self))
        return title

    # On cherche à extraire les textes d'un certain style
    def getTextsByStyleId(self, styleID):
        texts = []
        # On parcourt les textes et pour chaque texte, on vérifie si il a le style recherché
        for text in self.text:
            if text.style_id == styleID:
                texts.append(text)
        return texts

    def mergeSameLineTexts(self):
        input_texts = self.text
        output_text=[]
        for text in input_texts:
            input_texts.remove(text)
            for text2 in input_texts:
                if text.top == text2.top and text.style_id == text2.style_id:
                    input_texts.remove(text2)
                    text.content+=text2.content
            output_text.append(text)
        return output_text

    @property
    def text(self):
        text=""
        for tp in self.bodyText:
            text+="\n"+tp.content
        return text

    @property
    def title_text(self):
        text=""
        for tp in self.title:
            text+=tp.content
        return text
