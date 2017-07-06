import os

from exide.parse import parse

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/data/pptx"
exide_presentation = parse(os.path.join(__location__, "presentation-test-sections.pptx"))

for slide in exide_presentation.root_section.slides:
    print(slide.title)

