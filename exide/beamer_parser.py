#!/usr/bin/python
#-*- coding: utf-8 -*-
import re, os

from datatypes.Section import Section
from datatypes.Slide import Slide
from datatypes.Presentation import Presentation
from parser_utils import get_named_entities, get_urls, get_slide_type


def parse_beamer(path):
    """
    Transform a beamer tex file into a |Presentation| object

    :param path: Path of the beamer file
    :type path: string
    :return: |Presentation|
    """
    with open(path, 'r') as content_file:
        content = content_file.read()

    if len(re.compile(r'\\begin{frame}').split(content)) == 0:
        raise Exception("Invalid LaTeX Beamer file. No frame found.")

    if len(re.findall(r'\\title\[?.*\]?[\n]?\{(.*)\}', content, re.M)) > 0:
        title = re.findall(r'\\title\[?.*\]?[\n]?\{(.*)\}', content, re.M)[0]
    else:
        title = "Untitled"

    if len(re.compile(r'\\begin{frame}').split(content)) == 0:
        raise Exception("Invalid LaTeX Beamer file. No frame found.")

    if len(re.findall(r'\\author\[?.*\]?[\n]?\{(.*)\}', content, re.M)) > 0:
        author = detex(re.findall(r'\\author\[?.*\]?[\n]?\{(.*)\}', content, re.M)[0])
    else:
        author = "Untitled"

    pres = Presentation()
    pres.title = title
    pres.author = author
    pres.root_section = Section(title)

    title_slide = Slide()
    title_slide.title = title
    title_slide.type = "sectionheader"
    title_slide.id = 1
    pres.root_section.subelements.append(title_slide)

    pres.root_section.subelements += parse_sections(content, 2)
    return pres


def parse_slides(latex, starting_index=1):
    """
    Extract slides from tex file.

    :param latex:
    :param starting_index:
    :return:
    """
    index = starting_index
    slides = []
    slides_contents = re.compile(r'\\begin{frame}').split(latex)
    for i in range(1, len(slides_contents)):
        if len(re.findall(r'\\titlepage', slides_contents[i])) == 0:
            current_slide = Slide()
            current_slide.title = get_frame_title(slides_contents[i])
            current_slide.text = detex(slides_contents[i])
            current_slide.id = index
            current_slide.urls = get_urls(current_slide.text)
            current_slide.type = get_slide_type(current_slide)
            current_slide.named_entities = get_named_entities(current_slide.text.decode('ascii', "ignore"))
            current_slide.emphasized_text = get_emphasized_terms(slides_contents[i])
            index+=1
            slides.append(current_slide)
    return slides


def get_frame_title(latex):
    """
    Extract the title from slide tex source.

    :param latex: string
    :return: String
    """
    if re.match(r'^{.*}', latex):
        return re.findall(r'\{(.*?)\}', latex, re.S)[0]
    elif len(re.findall(r'\\frametitle{(.*?)}', latex, re.S)) > 0:
        return re.findall(r'\\frametitle{(.*?)}', latex, re.S)[0]
    return "Untitled"


def parse_subsections(latex, starting_index=1):
    """
    Parse subsections.

    :param latex:
    :param starting_index:
    :return: list of |Section| objects
    """
    index = starting_index
    subsections = []
    subsections_titles = re.findall(r'\\subsection{(.*?)\}', latex, re.S)
    subsections_contents = re.compile(r'\\subsection{.*}').split(latex)
    subsections += parse_slides(subsections_contents[0], index)
    index += len(subsections)
    for i in range(1, len(subsections_contents)):
        current_section = Section(subsections_titles[i-1])
        current_section.subelements += parse_slides(subsections_contents[i], index)
        index += len(current_section.subelements)
        subsections.append(current_section)
    return subsections


def parse_sections(latex, starting_index=1):
    """
    Parse sections.

    :param latex: string
    :param starting_index: int
    :return: list of |Section| objects
    """
    index = starting_index
    sections = []
    sections_titles = re.findall(r'\\section{(.*?)\}', latex, re.S)
    sections_contents = re.compile(r'\\section{.*}').split(latex)
    sections += parse_subsections(sections_contents[0], index)
    index += len(sections)
    for i in range(1, len(sections_contents)):
        current_section = Section(sections_titles[i-1])
        current_section.subelements += parse_subsections(sections_contents[i], index)
        index += len(current_section.subelements)
        sections.append(current_section)
    return sections

def get_emphasized_terms(latex):
    """
    Return emphasized terms of the given latex string.

    :param latex: String
    :return: list of Strings
    """
    return re.findall(r'\\emph{(.*?)\}', latex, re.S)

def applyRegexps(text, listRegExp):
    """ Applies successively many regexps to a text"""
    # apply all the rules in the ruleset
    for element in listRegExp:
        left = element['left']
        right = element['right']
        r = re.compile(left)
        text = r.sub(right, text)
    return text

def detex(latexText):
    """
        Transform a latex text into a simple text
        Credits : Gilles Bertrand http://www.gilles-bertrand.com/2012/11/a-simple-detex-function-in-python.html
    """
    # initialization
    regexps = []
    text = latexText
    # remove all the contents of the header, ie everything before the first occurence of "\begin{document}"
    text = re.sub(r"(?s).*?(\\begin\{document\})", "", text, 1)

    # remove comments
    regexps.append({r'left': r'([^\\])%.*', 'right': r'\1'})
    text = applyRegexps(text, regexps)
    regexps = []

    # - replace some LaTeX commands by the contents inside curly rackets
    to_reduce = [r'\\emph', r'\\textbf', r'\\textit', r'\\text', r'\\IEEEauthorblockA', r'\\IEEEauthorblockN',
                 r'\\author', r'\\caption', r'\\author', r'\\thanks']
    for tag in to_reduce:
        regexps.append({'left': tag + r'\{([^\}\{]*)\}', 'right': r'\1'})
    text = applyRegexps(text, regexps)
    regexps = []
    """
     _     _       _ _       _     _   
    | |__ (_) __ _| (_) __ _| |__ | |_ 
    | '_ \| |/ _` | | |/ _` | '_ \| __|
    | | | | | (_| | | | (_| | | | | |_ 
    |_| |_|_|\__, |_|_|\__, |_| |_|\__|
             |___/     |___/           
    """
    # - replace some LaTeX commands by the contents inside curly brackets and highlight these contents
    to_highlight = [r'\\part[\*]*', r'\\chapter[\*]*', r'\\section[\*]*', r'\\subsection[\*]*', r'\\subsubsection[\*]*',
                    r'\\paragraph[\*]*'];
    # highlightment pattern: #--content--#
    for tag in to_highlight:
        regexps.append({'left': tag + r'\{([^\}\{]*)\}', 'right': r'\n#--\1--#\n'})
    # highlightment pattern: [content]
    to_highlight = [r'\\title', r'\\author', r'\\thanks', r'\\cite', r'\\ref'];
    for tag in to_highlight:
        regexps.append({'left': tag + r'\{([^\}\{]*)\}', 'right': r'[\1]'})
    text = applyRegexps(text, regexps)
    regexps = []

    """
     _ __ ___ _ __ ___   _____   _____ 
    | '__/ _ \ '_ ` _ \ / _ \ \ / / _ \
    | | |  __/ | | | | | (_) \ V /  __/
    |_|  \___|_| |_| |_|\___/ \_/ \___|

    """
    # remove LaTeX tags
    # - remove completely some LaTeX commands that take arguments
    to_remove = [r'\\maketitle', r'\\footnote', r'\\centering', r'\\IEEEpeerreviewmaketitle', r'\\includegraphics',
                 r'\\IEEEauthorrefmark', r'\\label', r'\\begin', r'\\end', r'\\big', r'\\right', r'\\left',
                 r'\\documentclass', r'\\usepackage', r'\\bibliographystyle', r'\\bibliography', r'\\cline',
                 r'\\multicolumn', r'\\pause']

    # replace tag with options and argument by a single space
    for tag in to_remove:
        regexps.append({'left': tag + r'(\[[^\]]*\])*(\{[^\}\{]*\})*', 'right': r' '})
        # regexps.append({'left':tag+r'\{[^\}\{]*\}\[[^\]\[]*\]', 'right':r' '})
    text = applyRegexps(text, regexps)
    regexps = []

    """
                    _                
     _ __ ___ _ __ | | __ _  ___ ___ 
    | '__/ _ \ '_ \| |/ _` |/ __/ _ \
    | | |  __/ |_) | | (_| | (_|  __/
    |_|  \___| .__/|_|\__,_|\___\___|
             |_|                     
    """

    # - replace some LaTeX commands by the contents inside curly rackets
    # replace some symbols by their ascii equivalent
    # - common symbols
    regexps.append({'left': r'\\eg(\{\})* *', 'right': r'e.g., '})
    regexps.append({'left': r'\\ldots', 'right': r'...'})
    regexps.append({'left': r'\\Rightarrow', 'right': r'=>'})
    regexps.append({'left': r'\\rightarrow', 'right': r'->'})
    regexps.append({'left': r'\\le', 'right': r'<='})
    regexps.append({'left': r'\\ge', 'right': r'>'})
    regexps.append({'left': r'\\_', 'right': r'_'})
    regexps.append({'left': r'\\\\', 'right': r'\n'})
    regexps.append({'left': r'~', 'right': r' '})
    regexps.append({'left': r'\\&', 'right': r'&'})
    regexps.append({'left': r'\\%', 'right': r'%'})
    regexps.append({'left': r'([^\\])&', 'right': r'\1\t'})
    regexps.append({'left': r'\\item', 'right': r'\t- '})
    regexps.append({'left': r'\\\hline[ \t]*\\hline', 'right': r'============================================='})
    regexps.append({'left': r'[ \t]*\\hline', 'right': r'_____________________________________________'})
    # - special letters
    regexps.append({'left': r'\\\'{?\{e\}}?', 'right': r'é'})
    regexps.append({'left': r'\\`{?\{a\}}?', 'right': r'à'})
    regexps.append({'left': r'\\\'{?\{o\}}?', 'right': r'ó'})
    regexps.append({'left': r'\\\'{?\{a\}}?', 'right': r'á'})
    # keep untouched the contents of the equations
    regexps.append({'left': r'\$(.)\$', 'right': r'\1'})
    regexps.append({'left': r'\$([^\$]*)\$', 'right': r'\1'})
    # remove the equation symbols ($)
    regexps.append({'left': r'([^\\])\$', 'right': r'\1'})
    # correct spacing problems
    regexps.append({'left': r' +,', 'right': r','})
    regexps.append({'left': r' +', 'right': r' '})
    regexps.append({'left': r' +\)', 'right': r'\)'})
    regexps.append({'left': r'\( +', 'right': r'\('})
    regexps.append({'left': r' +\.', 'right': r'\.'})
    # remove lonely curly brackets
    regexps.append({'left': r'^([^\{]*)\}', 'right': r'\1'})
    regexps.append({'left': r'([^\\])\{([^\}]*)\}', 'right': r'\1\2'})
    regexps.append({'left': r'\\\{', 'right': r'\{'})
    regexps.append({'left': r'\\\}', 'right': r'\}'})
    # strip white space characters at end of line
    regexps.append({'left': r'[ \t]*\n', 'right': r'\n'})
    # remove consecutive blank lines
    regexps.append({'left': r'([ \t]*\n){3,}', 'right': r'\n'})
    # apply all those regexps
    text = applyRegexps(text, regexps)
    regexps = []
    # return the modified text
    return text


if __name__ == '__main__':

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))+"/tests/data/beamer"
    pres = parse_beamer(os.path.join(__location__, "simple_beamer"))
    print pres.title
    print pres.author
    print pres.root_section.outline
