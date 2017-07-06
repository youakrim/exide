import os

from exide.parse import parse

if __name__ == '__main__':
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/data/pptx"
    exide_presentation = parse(os.path.join(__location__, "presentation-test-sections.pptx"))

    print(exide_presentation.outline)
