#!/usr/bin/python
#-*- coding: utf-8 -*-

import math


class StyleGroup(object):

    def __init__(self, presentation):
        self.styles = []
        self.presentation = presentation

    def getOccurences(self):
        occurences = set()
        for style in self.styles:
            for occurence in style.getOccurences():
                occurences.add(occurence)
        return occurences

    def formatsText(self, textParser):
        return textParser in self.getOccurences()

    def headingIndex(self):
        index = 0
        for style in self.styles:
            index+=style.headingIndex()
        return math.ceil(index/len(self.styles))
