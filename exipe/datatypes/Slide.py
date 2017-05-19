#!/usr/bin/python
#-*- coding: utf-8 -*-

class Slide:
    #Slide
    def __init__(self):
        self.title = ""
        self.body_text = ""
        self.type = None
        self.emphasized_text = ""
        self.named_entities = []
        self.urls = []

    def get_emphasized_text(self, ):
        pass

    def get_named_entities(self, ):
        pass

    def get_urls(self, ):
        pass

    def get_text(self):
        return self.body_text
