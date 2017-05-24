#-*- coding: utf-8 -*-
from exipe.datatypes.Presentation import Presentation
from exipe.datatypes.Section import Section
from exipe.datatypes.Slide import Slide
from exipe.datatypes.types import Types
import pptx,re, os
from nltk import ne_chunk, pos_tag, word_tokenize, sent_tokenize, ne_chunk_sents, tag
from nltk.tree import Tree

def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
            else:
                continue
    return continuous_chunk

def get_text_statistics(list_of_runs):
    # On initialise les varaiables statistiques
    # We set the statistics variables
    font_list = {"default": 0}
    color_list = {"default": 0}
    font_size_list = {"default": 0} # [(62550,12)]
    boldness_list = {"bold": 0, "default": 0}
    underlined_list = {"underlined": 0, "default": 0}
    text_case_list = {"uppercase": 0, "default": 0}

    for run in list_of_runs:
        # Removing the tiny strings: ? , ; : /...
        if len(run.text)>2:
            # On récupère le nom de la police
            # We extract the font name
            if get_font_name(run) not in font_list:
                font_list[get_font_name(run)] = 1
            else:
                font_list[get_font_name(run)] += 1

            # We extract the text color
            if get_color(run) not in color_list:
                color_list[get_color(run)] = 1
            else:
                color_list[get_color(run)] += 1

            # We extract the font size
            if get_font_size(run) not in font_size_list:
                font_size_list[get_font_size(run)] = 1
            else:
                font_size_list[get_font_size(run)] += 1

            # We extract the text boldness
            if run.font.bold:
                boldness_list["bold"] += 1
            else:
                boldness_list["default"] += 1

            # We extract underlining
            if run.font.underline:
                underlined_list["underlined"] += 1
            else:
                underlined_list["default"] += 1

            # We extract text case (by word)
            for word in run.text.split(" "):
                if len(word) > 2:
                    if word.isupper():
                        text_case_list["uppercase"] += 1
                    else:
                        text_case_list["default"] += 1

    return {"fonts":font_list, "colors":color_list, "boldness":boldness_list, "underlining":underlined_list, "font-size": font_size_list, "text-case": text_case_list}

def statistics_noise_reduction(statistics):
    #TODO
    fonts_to_check = statistics["fonts"][:]
    font_groups = []
    while len(fonts_to_check) > 0:
        font_A = fonts_to_check[0]
        font_group = [font_A]
        fonts_to_check.remove(font_A)
        while len(fonts_to_check) > 0:
            if relative_uncertainty(font_A, fonts_to_check[0])<5:
                font_group.append(fonts_to_check[0])
                fonts_to_check.remove(fonts_to_check[0])
            else:
                break
        font_groups.append(font_group)
    return False

def relative_uncertainty(a,b):
    return (abs(a-b)/(a))*100

# Pré-condition : le run doit faire partie du corpus d'apprentissage des statistiques et les statistiques doivent avoir un format valides
def matches_statistics(run, statistics):
    # On considère qu'un run correspond aux statistiques si il est conforme à plus de la moitié de la mise en forme
    underlining_ratio = float(statistics["underlining"]["underlined"])/float(statistics["underlining"]["default"]+statistics["underlining"]["underlined"])
    if run.font.underline and underlining_ratio < 0.5:
        return False

    boldness_ratio = float(statistics["boldness"]["bold"])/float(statistics["boldness"]["bold"]+statistics["boldness"]["default"])
    if run.font.bold and boldness_ratio < 0.5:
        return False

    run_font_ratio = float(statistics["fonts"][get_font_name(run)])/float(total_run_count(statistics["fonts"]))
    if run_font_ratio < 0.5:
        return False

    color_ratio = float(statistics["colors"][get_color(run)])/float(total_run_count(statistics["colors"]))
    if color_ratio < 0.5:
        return False

    font_size_ratio = float(statistics["font-size"][get_font_size(run)])/float(total_run_count(statistics["font-size"]))
    if font_size_ratio < 0.5:
        return False
    return True

#Strings with different case
def get_case_emphasized_terms(text, statistics):
    case_emphasized_terms = []
    for word in text.split(" "):
        if not matches_case_statistics(word, statistics):
            case_emphasized_terms.append(word)
    return case_emphasized_terms

def matches_case_statistics(word, statistics):
    text_case_ratio = float(statistics["text-case"][get_case(word)]) / float(total_run_count(statistics["text-case"]))
    if text_case_ratio < 0.5:
        return False
    return True

def get_font_size(run):
    if run.font.size is not None:
        return run.font.size
    return "default"

def get_font_name(run):
    if run.font.name is not None:
        return run.font.name
    return "default"

def get_case(word):
    if word.isupper():
        return "uppercase"
    return "default"

def get_color(run):
    if run.font.color.type is not None:
        # print run.font.color.type
        if "RGB" in str(run.font.color.type):
                return run.font.color.rgb
        elif "SCHEME" in str(run.font.color.type):
            return "default"
    return "default"

def total_run_count(statistic):
    count = 0
    for value in statistic:
        count+=statistic[value]
    return count

def get_emphasized_terms(list_of_runs):
    statistics = get_text_statistics(list_of_runs)
    emphasized_terms = []
    for run in list_of_runs:
        if not matches_statistics(run, statistics):
            emphasized_terms.append(run.text)
        emphasized_terms += get_case_emphasized_terms(run.text, statistics)
    return emphasized_terms


def parse_pptx(fileName):
    # On créé la section racine qui va contenir tout les éléments : diapositives, autres sections
    presentation_title = "Root section"
    root_section = Section(presentation_title)
    # On peut maintenant créer la présentation
    presentation = Presentation(root_section)

    # Maintenant, nous allons pour chaque diapositive créer un objet slide

    file = open(fileName)
    prs = pptx.Presentation(file)

    for slide in prs.slides:

        new_slide = Slide()
        new_slide.title = get_title(slide)

        # On récupère le texte du corps de la diapositive
        new_slide.text = get_text(slide)

        new_slide.emphasized_text = get_emphasized_terms(get_runs(slide))

        # On cherche à typer la diapositive en fonction de son titre
        new_slide.type = get_slide_type(new_slide)

        # On cherche à récupérer les URLs
        new_slide.urls = get_urls(new_slide.text)
        root_section.subelements.append(new_slide)

        # On cherche à récupérer les entités nommées
        new_slide.named_entities = get_named_entities(new_slide.title)
        new_slide.named_entities += get_named_entities(new_slide.text)

        my_sent = "My name is Jack Tester."
        parse_tree = ne_chunk(tag.pos_tag(word_tokenize(my_sent)), binary=True)  # POS tagging before chunking!
        # print parse_tree
        named_entities = []

        for t in parse_tree.subtrees():
            #print t
            if t.label() == 'NE':
                #print t
                named_entities.append(t)
                # named_entities.append(list(t))  # if you want to save a list of tagged words instead of a tree
        # print named_entities
    return presentation

def get_urls(text):
   return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

def get_slide_type(slide):
    for type in Types.LIST:
        if any(word in slide.title.lower() for word in Types.LIST[type]):
            return type
    return "notype"

def get_named_entities(text):
    return get_continuous_chunks(text.encode('ascii', 'ignore'))

def get_title(slide):
    if slide.shapes.title is not None:
        return slide.shapes.title.text
    return "Untitled"

def get_text(slide):
    text=""
    for shape in slide.shapes.placeholders:
        if slide.shapes.title is not None and slide.shapes.title.shape_id != shape.shape_id:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                text += "\n" + (paragraph.level * "\t") + paragraph.text
    return text

def get_runs(slide):
    run_list = []
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for paragraph in shape.text_frame.paragraphs:
            run_list += paragraph.runs
    return run_list

def structure_extraction(section):
    #TODO

    pass

if __name__ == '__main__':
    # TESTS 2
    # Put the path of the file you want to test here
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))+"/tests/data/pptx"
    pres = parse_pptx(os.path.join(__location__, "presentation-test.pptx"))

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
