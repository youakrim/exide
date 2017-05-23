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
        # On récupère le texte du corps de la diapositive
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                new_slide.body_text += "\n" + (paragraph.level * "\t") + paragraph.text
                # On parcours les run à la recherche de texte en emphase
                for run in paragraph.runs:
                    if run.font.bold or run.font.underline or run.text.isupper():
                        new_slide.emphasized_text.append(run.text)

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
        print parse_tree
        named_entities = []

        for t in parse_tree.subtrees():
            print t
            if t.label() == 'NE':
                print t
                named_entities.append(t)
                # named_entities.append(list(t))  # if you want to save a list of tagged words instead of a tree
        print named_entities
    return presentation

if __name__ == '__main__':
    # TESTS 2
    # Put the path of the file you want to test here
    pres = parse_pptx("/media/sf_Documents/fichiers_test2/cours-cartes_conceptuelles.pptx")

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