#-*- coding: utf-8 -*-
import io
import os, copy

from nltk import ne_chunk, re
from nltk import ne_chunk, pos_tag, word_tokenize, sent_tokenize, ne_chunk_sents, tag
from nltk.tree import Tree

from exipe.datatypes.Section import Section
from exipe.datatypes.Slide import Slide
from exipe.datatypes.types import Types
from exipe.datatypes.Presentation import Presentation


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

def get_text_statistics(list_of_text_parsers):
    # On initialise les varaiables statistiques
    # We set the statistics variables
    font_list = {"default": 0}
    color_list = {"default": 0}
    font_size_list = {"default": 0} # [(62550,12)]
    boldness_list = {"bold": 0, "default": 0}
    underlined_list = {"default": 0}
    text_case_list = {"uppercase": 0, "default": 0}

    for tp in list_of_text_parsers:
        # Removing the tiny strings: ? , ; : /...
        if len(tp.text)>2:
            # On récupère le nom de la police
            # We extract the font name
            if tp.font_family not in font_list:
                font_list[tp.font_family] = 1
            else:
                font_list[tp.font_family] += 1

            # We extract the text color
            if tp.color not in color_list:
                color_list[tp.color] = 1
            else:
                color_list[tp.color] += 1

            # We extract the font size
            if tp.font_size not in font_size_list:
                font_size_list[tp.font_size] = 1
            else:
                font_size_list[tp.font_size] += 1

            # We extract the font_weight
            if tp.font_weight not in boldness_list:
                boldness_list[tp.font_weight] = 1
            else:
                boldness_list[tp.font_weight] += 1

            # We extract underlining
            if tp.underlined not in underlined_list:
                underlined_list[tp.underlined] = 1
            else:
                underlined_list[tp.underlined] += 1

            # We extract text case (by word)
            for word in tp.text.split(" "):
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

# Pré-condition : le text_parser doit faire partie du corpus d'apprentissage des statistiques et les statistiques doivent avoir un format valides
def matches_statistics(tp, statistics):
    # On considère qu'un text_parser correspond aux statistiques si il est conforme à plus de la moitié de la mise en forme
    tp_underlining_ratio = float(statistics["underlining"][tp.underlined])/float(total_text_parser_count(statistics["underlining"]))
    if tp_underlining_ratio < 0.5:
        return False

    tp_boldness_ratio = float(statistics["boldness"][tp.font_weight])/float(total_text_parser_count(statistics["boldness"]))
    if tp_boldness_ratio < 0.5:
        return False

    tp_font_ratio = float(statistics["fonts"][tp.font_family])/float(total_text_parser_count(statistics["fonts"]))
    if tp_font_ratio < 0.5:
        return False

    color_ratio = float(statistics["colors"][tp.color])/float(total_text_parser_count(statistics["colors"]))
    if color_ratio < 0.5:
        return False

    font_size_ratio = float(statistics["font-size"][tp.font_size])/float(total_text_parser_count(statistics["font-size"]))
    if font_size_ratio < 0.3:
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
    text_case_ratio = float(statistics["text-case"][get_case(word)]) / float(total_text_parser_count(statistics["text-case"]))
    if text_case_ratio < 0.5:
        return False
    return True


def get_case(word):
    if word.isupper():
        return "uppercase"
    return "default"


def total_text_parser_count(statistic):
    count = 0
    for value in statistic:
        count+=statistic[value]
    return count


def get_emphasized_terms(list_of_text_parsers):
    statistics = get_text_statistics(list_of_text_parsers)
    emphasized_terms = []
    for tp in list_of_text_parsers:
        if not matches_statistics(tp, statistics):
            emphasized_terms.append(tp.text)
        emphasized_terms += get_case_emphasized_terms(tp.text, statistics)
    return emphasized_terms


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
    text = ""
    for shape in slide.shapes.placeholders:
        if slide.shapes.title is not None:
            if slide.shapes.title.shape_id != shape.shape_id:
                if not shape.has_text_frame:
                    continue
                for paragraph in shape.text_frame.paragraphs:
                    text += "\n" + (paragraph.level * "\t") + paragraph.text
        else:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                text += "\n" + (paragraph.level * "\t") + paragraph.text

    return text


def structure_extraction(section):
    # We start by regrouping slides with similar titles
    current_section = None
    new_tree = Section(section.title)
    for i in range(1,len(section.slides)):
        if current_section is not None and title_similarity(section.slides[i-1].title, section.slides[i].title) > 0.7:
            current_section.subelements.append(section.slides[i])
        elif current_section is None and title_similarity(section.slides[i-1].title, section.slides[i].title) > 0.7:
            current_section = Section(section.slides[i-1].title)
            current_section.subelements.append(section.slides[i - 1])
            current_section.subelements.append(section.slides[i])
        elif current_section is not None:
            new_tree.subelements.append(copy.copy(current_section))
            current_section = None
        else:
            new_tree.subelements.append(section.slides[i-1])
    if current_section is not None:
        new_tree.subelements.append(copy.copy(current_section))
    else:
        new_tree.subelements.append(section.slides[len(section.slides)-1])
    # We then try to recognize section headers and create new section
    new_new_tree = Section(new_tree.title)
    element_list = new_tree.subelements[:]
    i = 0
    while len(element_list) > 0:
        if is_section_header(element_list[0]):
            current_section = Section(element_list[i].title)
            element_list.remove(element_list[0])
            while len(element_list) > 0:
                if is_section_header(element_list[0]):
                    break
                else:
                    current_section.subelements.append(element_list[0])
                    element_list.remove(element_list[0])
            new_new_tree.subelements.append(copy.copy(current_section))
        else:
            new_new_tree.subelements.append(element_list[0])
            element_list.remove(element_list[0])



    return new_new_tree



def title_similarity(title_1, title_2):
    str1 = stopwords_removal(title_1, "fr").lower().split()
    str2 = stopwords_removal(title_2, "fr").lower().split()
    return float(sum(levenshtein(word2, word1) == 0 or ((float(max(len(word1), len(word2))-levenshtein(word2, word1))/max(len(word1), len(word2))) > 0.7) for word2 in str1 for word1 in str2))/max(len(str1), len(str2))

def is_section_header(slide):
    return get_slide_type(slide) == "sectionheader"

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def stopwords_removal(string, language):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))+"/dict/"
    path = os.path.join(__location__, "sw_"+language);

    string_without_numbers = ''.join([i for i in string if i.isalpha()])
    try:
        file = io.open(path, 'r', encoding='utf-8')
    except:
        print "Error : missing stopword file for "+language+" in"+__location__
    file_content = file.read()
    stopwords = file_content.split("\n")
    stringwords = string_without_numbers.split()
    resultwords = [word for word in stringwords if word.lower() not in stopwords]
    result = ' '.join(resultwords)

    return result


def parse(presentation_parser):
    # On créé la section racine qui va contenir tout les éléments : diapositives, autres sections
    presentation_title = presentation_parser.slides[0].title
    root_section = Section(presentation_title)
    # On peut maintenant créer la présentation
    presentation = Presentation(root_section)
    for slide_parser in presentation_parser.slides:

        new_slide = Slide()
        new_slide.title = slide_parser.title

        # On récupère le texte du corps de la diapositive
        new_slide.text = slide_parser.text

        new_slide.emphasized_text = get_emphasized_terms(slide_parser.text_parsers)

        # On cherche à typer la diapositive en fonction de son titre
        new_slide.type = get_slide_type(new_slide)

        # On cherche à récupérer les URLs
        new_slide.urls = get_urls(new_slide.text)
        root_section.subelements.append(new_slide)

        # On cherche à récupérer les entités nommées
        new_slide.named_entities = get_named_entities(new_slide.title)
        new_slide.named_entities += get_named_entities(new_slide.text)

        named_entities = []

    presentation.root_section = structure_extraction(root_section)
    return presentation
