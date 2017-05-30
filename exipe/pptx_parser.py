#-*- coding: utf-8 -*-
from exipe.datatypes.Presentation import Presentation
from exipe.datatypes.Section import Section
from exipe.datatypes.Slide import Slide
from exipe.datatypes.types import Types
import pptx,re, os
from nltk import ne_chunk, pos_tag, word_tokenize, sent_tokenize, ne_chunk_sents, tag
from nltk.tree import Tree
from parser_utils import *

from exipe.pptx_element_parsers.PresentationParser import PresentationParser


def parse_pptx(fileName):

    # Maintenant, nous allons pour chaque diapositive créer un objet slide

    file = open(fileName)
    prs = pptx.Presentation(file)
    pres_pars = PresentationParser(prs)

    return parse(pres_pars)


if __name__ == '__main__':
    # TESTS 2
    # Put the path of the file you want to test here
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))+"/tests/data/pptx"
    pres = parse_pptx(os.path.join(__location__, "presentation-test-odp.pptx"))

    for element in pres.root_section.subelements:
        print "\nSlide title: "+element.title+" ["+element.type+"]"
        if len(element.urls) > 0:
            print "URLs"
            print element.urls
        if len(element.named_entities):
            print "Named Entities"
            print element.named_entities
        if len(element.emphasized_text) > 0:
            print "Emphasized"
            print element.emphasized_text
        print element.text
