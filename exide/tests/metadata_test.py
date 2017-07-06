import os

from exide.parse import parse

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/data/pptx"
exide_presentation = parse(os.path.join(__location__, "presentation-test-sections.pptx"))

print("The presentation \""+exide_presentation.title+"\" was created by "+exide_presentation.author+" on "+str(exide_presentation.created))

