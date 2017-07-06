#!/usr/bin/python
# -*- coding: utf-8 -*-


class Slide:
    """
    A Slide object has the following attributes :
        - title (String) : the slide's title or "Untitled" if the slide has no title.
        - text (String) : the slide's body text
        - type (String) : the slide's type ot "notype" if the slide has no type.
        - emphasized terms (list of strings) : the slide's emphasized terms
        - urls (list of strings) : the slide's urls
        - named_entities (list of strings): the slide's named entities
        - id (int) : slide's number.
    """

    def __init__(self):
        self.title = "Untitled"
        self.text = ""
        self.type = "notype"
        self.emphasized_terms = []
        self.urls = []
        self.named_entities = []
        self.id = ""
