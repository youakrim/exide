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
        for frame in XMLSlideObject.findall(".//draw:frame[@presentation:class='outline']", XMLSlideObject.nsmap):
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
        # On récupère ensuite les paragraphes dont l'éléments draw frame parent est de classe notes
        for frame in XMLSlideObject.findall(".//draw:frame[@presentation:class='notes']", XMLSlideObject.nsmap):
            for textF in frame.findall(".//text:p", XMLSlideObject.nsmap):
                style = ""
                if textF.get(namespace(textF)+"style-name") is not None:
                    style = textF.get(namespace(textF)+"style-name")

                if textF.text is not None:
                    text.append(TextParser(textF, "notes", style, self))

            for textF in frame.findall(".//text:span", XMLSlideObject.nsmap):
                style = ""
                if textF.get(namespace(textF)+"style-name") is not None:
                    style = textF.get(namespace(textF)+"style-name")

                if textF.text is not None:
                    text.append(TextParser(textF, "notes", style, self))

            for textF in frame.findall(".//text:text", XMLSlideObject.nsmap):
                style = ""
                if textF.get(namespace(textF)+"style-name") is not None:
                    style = textF.get(namespace(textF)+"style-name")

                if textF.text is not None:
                    text.append(TextParser(textF, "notes", style, self))

        for frame in XMLSlideObject.findall(".//draw:frame[@presentation:class='text']", XMLSlideObject.nsmap):
            for textF in frame.findall(".//text:p", XMLSlideObject.nsmap):
                style = ""
                if textF.get(namespace(textF)+"style-name") is not None:
                    style = textF.get(namespace(textF)+"style-name")

                if textF.text is not None:
                    text.append(TextParser(textF, "text", style, self))

            for textF in frame.findall(".//text:span", XMLSlideObject.nsmap):
                style = ""
                if textF.get(namespace(textF)+"style-name") is not None:
                    style = textF.get(namespace(textF)+"style-name")

                if textF.text is not None:
                    text.append(TextParser(textF, "text", style, self))

            for textF in frame.findall(".//text:text", XMLSlideObject.nsmap):
                style = ""
                if textF.get(namespace(textF)+"style-name") is not None:
                    style = textF.get(namespace(textF)+"style-name")

                if textF.text is not None:
                    text.append(TextParser(textF, "text", style, self))
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

    def isAnExample(self):
        if len(self.title) >0:
            for p in self.title:
                if p.isAnExample() or any(word in p.content.lower() for word in self.EXAMPLE_STRINGS):
                    return True
            return False
        else:
            for text in self.bodyText:
                if text.isAnExample():
                    return True
        return False

    def isAToC(self):
        if len(self.title) >0:
            for p in self.title:
                if any(word in p.content.lower() for word in self.TABLE_OF_CONTENTS_STRINGS):
                    return True
            return False
        else:
            for text in self.bodyText:
                return any(word in text.content.lower() for word in self.TABLE_OF_CONTENTS_STRINGS)
        return False

    def isAConclusion(self):
        if len(self.title) >0:
            for p in self.title:
                if any(word in p.content.lower() for word in self.CONCLUSION_STRINGS):
                    return True
            return False
        else:
            for text in self.bodyText:
                return any(word in text.content.lower() for word in self.CONCLUSION_STRINGS)
        return False

    def isAnIntroduction(self):
        if len(self.title) >0:
            for p in self.title:
                if any(word in p.content.lower() for word in self.INTRODUCTION_STRINGS):
                    return True
            return False
        else:
            for text in self.bodyText:
                return any(word in text.content.lower() for word in self.INTRODUCTION_STRINGS)
        return False

    def isReferences(self):
        if len(self.title) >0:
            for p in self.title:
                if any(word in p.content.lower() for word in self.REFERENCES_STRINGS):
                    return True
            return False
        else:
            for text in self.bodyText:
                return any(word in text.content.lower() for word in self.REFERENCES_STRINGS)
        return False

    def isADefinition(self):
        if len(self.title) >0:
            for p in self.title:
                if any(word in p.content.lower() for word in self.DEFINITION_STRINGS):
                    return True
            return False
        else:
            for text in self.bodyText:
                return any(word in text.content.lower() for word in self.DEFINITION_STRINGS)
        return False

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
