#!/usr/bin/python
# -*- coding: utf-8 -*-
from Slide import Slide


class Section:
    """
    A Section object has the following attributes :
        - subelements (list of Slide and Section objects): list of the element within the Section
        - level (int) : depth of the Section in the presentation element tree
        - toc_slide_id (int) : id of the table of content slide of the Section
        - title (string): title of the Section
    """
    def __init__(self, title=None):
        self.subelements = []
        self.level = 0
        self.toc_slide_id = None
        self.type = "section"
        self.title = title

    def first_slide_title(self):
        """
            Title of the fist slide of the section, returns None if the Section has no slide
        """
        if len(self.subelements) > 0:
            return self.subelements[0].title
        return "Untitled"

    @property
    def emphasized_terms(self, ):
        """
            List of the emphasized terms of the Section's slides
        """
        emphasized_termss = []
        for element in self.subelements:
            emphasized_termss += element.emphasized_terms
        return emphasized_termss

    @property
    def named_entities(self, ):
        """
            List of the named entities of the Section's slides
        """
        ne = []
        for element in self.subelements:
            ne += element.named_entities
        return ne

    @property
    def text(self, ):
        """
            String of the body text of all slides without the slide titles
        """
        text = ""
        for element in self.subelements:
            text += element.text
        return text

    @property
    def urls(self, ):
        """
            List of the URLs of the Section's slides
        """
        urls = []
        for element in self.subelements:
            urls += element.urls
        return urls

    @property
    def slides(self):
        """
            List of the Section's Slide objects
        """
        slides = []
        for element in self.subelements:
            if isinstance(element, Slide):
                slides.append(element)
        return slides

    @property
    def sections(self):
        """
            List of the Section's subsections
        """
        sections = []
        for element in self.subelements:
            if isinstance(element, Section):
                sections.append(element)
        return sections

    @property
    def outline(self):
        """
            Return a list style string with the section outline
        """
        if self.title is not None:
            outline = "- " + self.title.replace('\n', ' ').replace('\r', '').replace('\t', '') + "\n"
        else:
            outline = "- Untitled \n"
        for element in self.subelements:
            if isinstance(element, Section):
                for line in element.outline.split("\n"):
                    outline += "\t" + line + "\n"
            else:
                outline += "\t* " + element.title.replace('\n', ' ').replace('\r', '').replace('\t',
                                                                                               '') + " [sl. " + str(
                    element.id) + "]\n"
        return outline

    @property
    def id(self):
        """
        Return the |id| of the first |Slide| of the |Section|
        """
        if len(self.subelements) >0:
            return self.subelements[0].id
        else:
            return 1

    def get_slides_of_type(self, type):
        """
        Returns the list of the |Slide| objects of the given type

        :param type: str. -- type of slides
        :return: list of |Slide| objects
        """
        slides = []
        for slide in self.subelements:
            if slide.type == type:
                slides.append(slide)
        return slides

    def get_slides_by_keyword(self, keyword, search_title=True, search_body_text=False):
        """
        Returns the list of |Slide| objects that contain a given keyword

        :param keyword: The word or string to look for.
        :param search_title: Indicates if the search should consider the title string or not
        :param search_body_text: Indicates if the search should consider the body text string or not
        :return: list of |Slide| objects
        """
        slides = []
        for slide in self.slides:
            if search_title:
                if keyword in slide.title:
                    slide.append(slide)
            if search_bodytext:
                if keyword in slide.text:
                    slides.append()
        return slides

    def get_slides_by_title(self, title):
        """
        Returns the list of the slides whose title matches the given title

        :param title: The title string to look for
        :return: list of |Slide| objects
        """
        slides = []
        for slide in self.slides:
            if slide.title == title:
                slides.append(slide)
        return slides
