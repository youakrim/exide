#!/usr/bin/python
#-*- coding: utf-8 -*-
import getopt
import os

import sys

import beamer_parser
import odp_parser


# On cherche à récuperer les noms des fichiers d'entrée et de sortie
import pptx_parser


def main(argv):
    # We try to get the input and output files names
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
        '''print("Opts : ")
        print(opts)
        print("Args : ")
        print(args)'''
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    # On récupère les noms de fichiers et extensions
    # We extract the filename and extension of both files
    inputfile_name, inputfile_extension = os.path.splitext(inputfile)
    # On vérifie que l'extension du fichier d'entrée (inputfile) est connue
    # We check if the inputfile extension is recognized
    extensions_connues = [".odp", ".pptx", ".tex"]

    if inputfile_extension not in extensions_connues:
        sys.exit("Erreur : Type de fichier non supporté \n \t Les extensions supportées sont "+ str(extensions_connues))

    # Si odp alors on entre dans l'archive
    # If the input file extension is ".odp", we unzip the archive
    if inputfile_extension == ".odp":
        pres = odp_parser.parse_odp(inputfile)
        print pres.root_section.outline.encode('utf-8')
    elif inputfile_extension == ".pptx":
        pres = pptx_parser.parse_pptx(inputfile)
        print pres.root_section.outline.encode('utf-8')
        #print pres.export_to_json()
    elif inputfile_extension == ".tex":
        pres = beamer_parser.parse_beamer(inputfile)
        print pres.root_section.outline.encode('utf-8')


if __name__ == "__main__":
    main(sys.argv[1:])
