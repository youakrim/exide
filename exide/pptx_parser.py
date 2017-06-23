#-*- coding: utf-8 -*-

import pptx
from .parser_utils import *

from .pptx_element_parsers.PresentationParser import PresentationParser


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
    pres = parse_pptx(os.path.join(__location__, "presentation-test-sections.pptx"))

    print pres.root_section.outline
