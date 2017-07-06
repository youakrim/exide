# -*- coding: utf-8 -*-
import io
import os, copy

from nltk import ne_chunk, re
from nltk import ne_chunk, pos_tag, word_tokenize, sent_tokenize, ne_chunk_sents, tag
from nltk.tree import Tree

from datatypes.Section import Section
from datatypes.Slide import Slide
from datatypes.SlideTypes import SlideTypes
from datatypes.Presentation import Presentation


def get_continuous_chunks(text):
    """
    Return the list of proper nouns of the given string

    :param text: string
    :return: list of proper nouns
    """
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
    """
    Return a dictionary of dictionaries each corresponding to a statistic

    :param list_of_text_parsers:
    :return: a dictionary of dictionaries
    """
    # On initialise les varaiables statistiques
    # We set the statistics variables
    font_list = {"default": 0}
    color_list = {"default": 0}
    font_size_list = {"default": 0}  # [(62550,12)]
    boldness_list = {"bold": 0, "default": 0}
    underlined_list = {"default": 0}
    text_case_list = {"uppercase": 0, "default": 0}

    for tp in list_of_text_parsers:
        # Removing the tiny strings: ? , ; : /...
        if len(tp.text) > 2:
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

    return {"fonts": font_list, "colors": color_list, "boldness": boldness_list, "underlining": underlined_list,
            "font-size": font_size_list, "text-case": text_case_list}


def statistics_noise_reduction(statistics):
    """
    Return a text statistic dictionary denoised (similar characteristics has been merged) [this function doesn't work yet].

    :param statistics:
    :return: a text statistic dictionary
    """
    # TODO
    fonts_to_check = statistics["fonts"][:]
    font_groups = []
    while len(fonts_to_check) > 0:
        font_A = fonts_to_check[0]
        font_group = [font_A]
        fonts_to_check.remove(font_A)
        while len(fonts_to_check) > 0:
            if relative_uncertainty(font_A, fonts_to_check[0]) < 5:
                font_group.append(fonts_to_check[0])
                fonts_to_check.remove(fonts_to_check[0])
            else:
                break
        font_groups.append(font_group)
    return False


def relative_uncertainty(a, b):
    """
    Calculate the relative uncertainty between two numbers

    :param a:
    :param b:
    :return: relative uncertainty between a and b
    """
    return (abs(a - b) / (a)) * 100


# Pré-condition : le text_parser doit faire partie du corpus d'apprentissage des statistiques et les statistiques doivent avoir un format valides
def matches_statistics(tp, statistics, underlining_threshold=0.5, boldness_threshold=0.9, font_family_threshold=0.5, color_threshold = 0.5, font_size_threshold =0.3):
    """
    Return True if the given TextParser object matches the given text statistics or False if ut doesn't

    :param tp: TextParser
    :param statistics:
    :param underlining_threshold:
    :param boldness_threshold:
    :param font_family_threshold:
    :param color_threshold:
    :param font_size_threshold:
    :return:
    """
    # On considère qu'un text_parser correspond aux statistiques si il est conforme à plus de la moitié de la mise en forme
    tp_underlining_ratio = float(statistics["underlining"][tp.underlined]) / float(
        total_text_parser_count(statistics["underlining"]))
    if tp_underlining_ratio < underlining_threshold:
        return False

    tp_boldness_ratio = float(statistics["boldness"][tp.font_weight]) / float(
        total_text_parser_count(statistics["boldness"]))
    if tp_boldness_ratio < boldness_threshold:
        return False

    tp_font_ratio = float(statistics["fonts"][tp.font_family]) / float(total_text_parser_count(statistics["fonts"]))
    if tp_font_ratio < font_family_threshold:
        return False

    color_ratio = float(statistics["colors"][tp.color]) / float(total_text_parser_count(statistics["colors"]))
    if color_ratio < color_threshold:
        return False

    font_size_ratio = float(statistics["font-size"][tp.font_size]) / float(
        total_text_parser_count(statistics["font-size"]))
    if font_size_ratio < font_size_threshold:
        return False
    return True


# Strings with different case
def get_case_emphasized_terms(text, statistics):
    """
    Returns the words that have a different case than the average text.

    :param text:
    :param statistics:
    :return:
    """
    case_emphasized_terms = []
    for word in text.split(" "):
        if not matches_case_statistics(word, statistics):
            case_emphasized_terms.append(word)
    return case_emphasized_terms


def matches_case_statistics(word, statistics):
    """
    Return True if the given text's characteristics matches average characteristics given by the statistics.

    :param word: String
    :param statistics: Dictionary
    :return: Boolean
    """
    text_case_ratio = float(statistics["text-case"][get_case(word)]) / float(
        total_text_parser_count(statistics["text-case"]))
    if text_case_ratio < 0.0:
        return False
    return True


def get_case(word):
    """
    Gives the case of the given word.

    :param word: String
    :return: String
    """
    if word.isupper():
        return "uppercase"
    return "default"


def total_text_parser_count(statistic):
    """
    Count the |TextParser| object included in the given statistics.

    :param statistic: dictionary
    :return: int
    """
    count = 0
    for value in statistic:
        count += statistic[value]
    return count


def get_emphasized_terms(list_of_text_parsers):
    """
    Return a list of emphasized terms within the given |TextParser| objects.

    :param list_of_text_parsers:
    :return: list of Strings.
    """
    statistics = get_text_statistics(list_of_text_parsers)
    emphasized_terms = []
    for tp in list_of_text_parsers:
        if len(tp.text) > 3:
            if not matches_statistics(tp, statistics):
                emphasized_terms.append(tp.text)
            emphasized_terms += get_case_emphasized_terms(tp.text, statistics)
    return emphasized_terms


def get_urls(text):
    """
    Return a list of the urls of the given text.

    :param text: String
    :return: String
    """
    return re.findall('[http[s]?://]?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)


def get_slide_parser_type(slide):
    """
    Returns a string with the matching slide type for the given |SlideParser| or "notype" if no type was found.

    :param slide: |SlideParser|
    :return: String
    """
    if get_title(slide) == "Untitled":
        return "graphic"
    if slide.layout is not None and slide.layout == slide.presentation.pptx_object.slide_layouts[2]:
        return "sectionheader"
    for type in SlideTypes.LIST:
        if any(word in get_title(slide).lower() for word in SlideTypes.LIST[type]):
            return type
    return "notype"


def get_slide_type(slide):
    """
    Returns a string with the matching slide type for the given slide or "notype" if no type was found.

    :param slide:
    :return: String
    """
    if slide.title == "Untitled":
        return "graphic"
    for type in SlideTypes.LIST:
        if any(word in slide.title.decode("utf8").lower() for word in SlideTypes.LIST[type]):
            return type
    return "notype"


def get_named_entities(text):
    """
    Return the list af the named entities of the given text.

    :param text: string
    :return: list of strings
    """
    return get_continuous_chunks(text.encode('ascii', 'ignore'))


def get_title(slide):
    """
    Return the title of a given slide, return "Untitled" if no title was found.

    :param slide:
    :return: String
    """
    if slide.title is not None:
        return slide.title
    elif len(slide.text.split("\n")) > 0:
        for line in slide.text.split("\n"):
            if len(line) > 2 and len(slide.text.split(" ")) > 0:
                return line.replace('\t', '')
    return "Untitled"

"""
def group_slides_by_title(section):
    # We start by regrouping slides with similar titles
    current_section = None
    new_tree = Section(section.title)
    for i in range(1, len(section.slides)):
        if current_section is not None and title_similarity(get_title(section.slides[i - 1]), get_title(section.slides[i])) > 0.7:
            current_section.subelements.append(section.slides[i])
        elif current_section is None and title_similarity(get_title(section.slides[i - 1]), get_title(section.slides[i])) > 0.7:
            current_section = Section(section.slides[i - 1].title)
            current_section.subelements.append(section.slides[i - 1])
            current_section.subelements.append(section.slides[i])
        elif current_section is not None:
            new_tree.subelements.append(copy.copy(current_section))
            current_section = None
        else:
            new_tree.subelements.append(section.slides[i - 1])
    if current_section is not None:
        new_tree.subelements.append(copy.copy(current_section))
    else:
        new_tree.subelements.append(section.slides[len(section.slides) - 1])
    return new_tree
"""

def structure_extraction(section, presentation_parser):
    """
    Return a structured |Section| object.

    :param section:
    :param presentation_parser:
    :return: |Sectionbject|
    """
    slide_parser_list = presentation_parser.slides
    if len(section.subelements) > 0:
        output_section = Section(section.subelements[0].title)
    else:
        output_section = Section("Untitled")
    element_list = section.subelements
    output_section.subelements.append(element_list[0])
    # On retire la premier element de liste_elem qui correspond au titre de la section
    element_list.remove(element_list[0])
    # Tant que la pile n’est pas vide
    while len(element_list) > 0:
        # Si l’élément courant est une section
        if isinstance(element_list[0], Section):
            # On l'ajoute directement à la section de sortie
            output_section.subelements.append(element_list[0])
            element_list.remove(element_list[0])
        # Si l’élément courant est une en-tête de section suivie par au moins une diapo de niveau inférieur:
        elif is_section_header(element_list[0]) and len(element_list) > 1:
            # Alors on créer une section
            current_section = Section(element_list[0].title)
            # On ajoute l’élément dans la section
            current_section.subelements.append(element_list[0])
            # On retire l’élément de la pile

            element_list.remove(element_list[0])
            # On ajoute tout les éléments suivants jusqu’à ce qu’il y a une autre en-t^te de section de même niveau suivie par au moins une diapo de niveau inférieur
            while len(element_list) > 0 and not(is_section_header(element_list[0]) and section_level(slide_parser_list[element_list[0].id - 1]) >= section_level(slide_parser_list[current_section.subelements[0].id - 1])):
                current_section.subelements.append(element_list[0])
                element_list.remove(element_list[0])
            # On structure la section créee
            structured_section = structure_extraction(current_section, presentation_parser)
            # On ajoute la section créée à la section de sortie
            output_section.subelements.append(copy.copy(structured_section))
        # Sinon, on l’ajoute à la section de sortie
        else:
            output_section.subelements.append(element_list[0])
            element_list.remove(element_list[0])
    return output_section


def title_similarity(title_1, title_2):
    """
    Return a similarity index between two strings.

    :param title_1:
    :param title_2:
    :return:
    """
    str1 = stopwords_removal(title_1, "fr").lower().split()
    str2 = stopwords_removal(title_2, "fr").lower().split()
    if max(len(str1), len(str2)) == 0:
        return 0
    return float(sum(levenshtein(word2, word1) == 0 or (
    (float(max(len(word1), len(word2)) - levenshtein(word2, word1)) / max(len(word1), len(word2))) > 0.7) for word2 in
                     str1 for word1 in str2)) / max(len(str1), len(str2))


def is_section_header(slide):
    """
    Return True if the given side is a section header and false if it isn't.

    :param slide:
    :return: Boolean
    """
    return slide.type == "sectionheader" or (len(slide.text.split(" ")) < 30 and slide.type != "graphic")


def section_level(slide_parser):
    """
    Return a string corresponding to the indentation level of the slide

    :param slide_parser:
    :return:
    """
    if len(slide_parser.title_parsers) > 0:
        return slide_parser.title_parsers[0].font_size
    return 0


def levenshtein(s1, s2):
    """
    Return the levensthein distance between two strings

    :param s1:
    :param s2:
    :return: int
    """
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
    """
    Removes the stopwords of the string of the given language. If no stopwords dictionary exist for the given language, the function raises an exception.

    :param string:
    :param language: language of the given string
    :return: String
    """
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/dict/"
    path = os.path.join(__location__, "sw_" + language+".txt");

    string_without_numbers = ''.join([i for i in string if i.isalpha()])
    result = ""
    try:
        file = io.open(path, 'r', encoding='utf-8')
        file_content = file.read()
        stopwords = file_content.split("\n")
        stringwords = string_without_numbers.split()
        resultwords = [word for word in stringwords if word.lower() not in stopwords]
        result = ' '.join(resultwords)
    except:
        print "Error : missing stopword file for " + language + " in" + __location__

    return result


def parse(presentation_parser):
    """
    Parse a |PresentationParser| object into a |Presentation| object.

    :param presentation_parser: |PresentationParser| object
    :return: |Presentation| object
    """
    # On créé la section racine qui va contenir tout les éléments : diapositives, autres sections
    presentation_title = get_title(presentation_parser.slides[0])
    root_section = Section()
    # On peut maintenant créer la présentation
    presentation = Presentation(root_section)

    presentation.initial_format = presentation_parser.initial_format
    presentation.title = presentation_parser.title
    presentation.author = presentation_parser.author
    presentation.category = presentation_parser.category
    presentation.comments = presentation_parser.comments
    presentation.keywords = presentation_parser.keywords
    presentation.language = presentation_parser.language
    presentation.created = presentation_parser.created
    presentation.last_modified = presentation_parser.last_modified
    presentation.subject = presentation_parser.subject
    current_id = 1
    for slide_parser in presentation_parser.slides:
        new_slide = Slide()
        new_slide.id = current_id
        current_id += 1
        new_slide.title = get_title(slide_parser)

        # On récupère le texte du corps de la diapositive
        new_slide.text = slide_parser.text

        new_slide.emphasized_terms = get_emphasized_terms(slide_parser.text_parsers)

        # On cherche à typer la diapositive en fonction de son titre
        new_slide.type = get_slide_parser_type(slide_parser)

        # On cherche à récupérer les URLs
        new_slide.urls = get_urls(new_slide.text)
        presentation.root_section.subelements.append(new_slide)
        if presentation.root_section.title is None:
            presentation.root_section.title == new_slide.title

        # On cherche à récupérer les entités nommées
        new_slide.named_entities = get_named_entities(new_slide.title)
        new_slide.named_entities += get_named_entities(new_slide.text)
    presentation.root_section = group_slides_by_title(presentation.root_section)
    presentation.root_section = structure_extraction(presentation.root_section, presentation_parser)
    return presentation
