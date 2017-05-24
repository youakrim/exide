#-*- coding: utf-8 -*-

import getopt
import os
import sys
import uuid

import shutil, zipfile
from lxml import etree

from exipe.datatypes.Section import Section
from exipe.datatypes.Presentation import Presentation
from exipe.datatypes.Slide import Slide
from exipe.odp_element_parsers.PresentationParser import PresentationParser



def parse_odp(file_path):
    inputfile_name, inputfile_extension = os.path.splitext(file_path)
    inputfile_name = os.path.basename(file_path)
    inputfile_directory = os.path.dirname(file_path)

    unique_id = uuid.uuid4()
    # On décompresse l'archive
    # We unzipp the archive
    path_to_unzipped = inputfile_directory + "/unzipped_" + str(unique_id)
    zip_ref = zipfile.ZipFile(file_path, 'r')
    zip_ref.extractall(path_to_unzipped)
    zip_ref.close()
    # On récupère le contenu du fichier content.xml
    # We extract the content from the "content.xml" file
    with open(path_to_unzipped + "/content.xml", 'r') as content_file:
        content = content_file.read()
    # On parse le contenu en xml
    # We parse the content as an xml file
    tree = etree.parse(path_to_unzipped + "/content.xml")
    root = tree.getroot()
    # On supprime l'archive décompressée
    shutil.rmtree(path_to_unzipped)

    presPars = PresentationParser(root)

    # On créé une section racine
    root_section = Section("Root section")

    # On ajoute des slides à cette section
    for slideParser in presPars.slides:
        slideTmp = Slide()
        slideTmp.title = slideParser.title_text
        slideTmp.text = slideParser.text
        root_section.subelements.append(slideTmp)
    # On créé une présentation à partir de la section racine
    pres = Presentation(root_section)

    return pres

if __name__ == '__main__':
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))+"/tests/data/odp"
    pres = parse_odp(os.path.join(__location__, "presentation-test-pptx.odp"))

    for element in pres.root_section.subelements:
        print "\nSlide title: " + element.title + " [" + element.type + "]"
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