#!/usr/bin/python
#-*- coding: utf-8 -*-


class StyleParser(object):

    def __init__(self, XMLStyleObject, presentation):
        self.id = XMLStyleObject.attrib["id"]
        self.font_size = int(XMLStyleObject.attrib["size"])
        self.font_family = XMLStyleObject.attrib["family"]
        self.font_color = XMLStyleObject.attrib["color"]
        self.presentation = presentation

    def getOccurences(self):
        return self.presentation.getTextsByStyleId(self.id)

    def countOccurences(self):
        return len(self.getOccurences())

    def isSimilarTo(self, styleParser):
        similarity_index = 0
        # On regarde si les polices sont différentes
        if styleParser.font_family == self.font_family:
            similarity_index += 100
        # On compare les tailles de police
        similarity_index+=100*(1-2*(abs(self.font_size - styleParser.font_size)/self.font_size))
        if styleParser.font_color == self.font_color:
            # Si la couleur des styles est noir
            if self.font_color == "#000000":
                # Alors on ne prends pas en compte la couleur
                return similarity_index > 190
            else:
                similarity_index+=100
        return similarity_index > 290

    # Plus l'indice calculé est grand, plus le style a de chance de correspondre à un style de titre
    def headingIndex(self):
        return self.font_size