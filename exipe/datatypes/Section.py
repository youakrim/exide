#!/usr/bin/python
# -*- coding: utf-8 -*-
from Slide import Slide


class Section:
    def __init__(self):
        self.subelements = []
        self.level = 0
        self.toc_slide_id = None
        self.type="section"
    @property
    def title(self):
        return self.subelements[0].title

    @property
    def emphasized_text(self, ):
        emphasized_texts = []
        for element in self.subelements:
            emphasized_texts+=element.emphasized_text
        return emphasized_texts

    @property
    def named_entities(self, ):
        ne = []
        for element in self.subelements:
            ne+=element.named_entities
        return ne

    @property
    def text(self, ):
        text = ""
        for element in self.subelements:
            text+=element.text
        return text

    @property
    def urls(self, ):
        urls = []
        for element in self.subelements:
            urls+=element.urls
        return urls

    @property
    def slides(self):
        slides = []
        for element in self.subelements:
            if isinstance(element, Slide):
                slides.append(element)
        return slides

    @property
    def sections(self):
        sections = []
        for element in self.subelements:
            if isinstance(element, Section):
                sections.append(element)
        return sections

    @property
    def outline(self):
        outline = "- "+self.title.replace('\n', ' ').replace('\r', '').replace('\t', '')+"\n"
        for element in self.subelements:
            if isinstance(element, Section):
                for line in element.outline.split("\n"):
                    outline += "\t"+line+"\n"
            else:
                outline+="\t* "+element.title.replace('\n', ' ').replace('\r', '').replace('\t', '')+" [sl. "+str(element.id)+"]\n"
        return outline

    @property
    def id(self):
        return self.subelements[0].id

    def get_slides_of_type(self, type):
        pass

    def get_slides_by_keyword(self, keyword):
        pass

    def get_slides_by_title(self, title):
        pass

