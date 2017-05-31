#!/usr/bin/python
#-*- coding: utf-8 -*-

from exipe.pptx_element_parsers.TextParser import TextParser

class SlideParser(object):

    def __init__(self, PPTXSlideObject, number, presentationParser):
        self.presentation = presentationParser
        self.text_parsers = self.parseText(PPTXSlideObject)
        self.title_parsers = []
        self.number = number
        self.pptx_object = PPTXSlideObject
        self.layout = PPTXSlideObject.slide_layout


    def parseText(self, PPTXSlideObject):
        text = []
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
        for tp in self.text_parsers:
            text+="\n"+tp.text
        return text

    @property
    def title(self):
        text = ""
        if self.pptx_object.shapes.title is not None:
            return self.pptx_object.shapes.title.text
        return "Untitled"
