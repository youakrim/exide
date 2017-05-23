#-*- coding: utf-8 -*-
from exipe.datatypes.Presentation import Presentation
from exipe.datatypes.Section import Section
from exipe.datatypes.Slide import Slide
from exipe.datatypes.types import Types
import pptx,re
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
    font_size_list = {"default": 0}
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
        if slide.shapes.title is not None:
            new_slide.title = slide.shapes.title.text
        else:
            new_slide.title = "Untitled"

        run_list = []
        # On récupère le texte du corps de la diapositive
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                new_slide.body_text += "\n" + (paragraph.level * "\t") + paragraph.text
                run_list+=paragraph.runs

        new_slide.emphasized_text = get_emphasized_terms(run_list)

        # On cherche à typer la diapositive en fonction de son titre
        for type in Types.LIST:
            if any(word in new_slide.title.lower() for word in Types.LIST[type]):
                new_slide.type = type

        # On cherche à récupérer les URLs
        new_slide.urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', new_slide.body_text)
        root_section.subelements.append(new_slide)

        # On cherche à récupérer les entités nommées
        new_slide.named_entities = get_continuous_chunks(new_slide.title.encode('ascii', 'ignore'))
        new_slide.named_entities += get_continuous_chunks(new_slide.body_text.encode('ascii', 'ignore'))

        my_sent = "My name is Jacob Perkins."
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

if __name__ == '__main__':
    # TESTS 2
    # Put the path of the file you want to test here
    pres = parse_pptx("/media/sf_Documents/fichiers_test2/presentation-test.pptx")

    for element in pres.root_section.subelements:
        if element.type is not None:
            print "\n<"+element.type+">"+element.title+"</"+element.type+">"
        else:
            print "\n<notype>"+element.title+"</notype>"
        if len(element.urls) > 0:
            print "URL"
            print element.urls
        if len(element.named_entities):
            print "NE"
            print element.named_entities
        if len(element.emphasized_text) >0:
            print "Emph"
            print element.emphasized_text
    # print pres.root_section.get_text()