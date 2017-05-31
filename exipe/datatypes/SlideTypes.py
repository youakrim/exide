#-*- coding: utf-8 -*-
import os,io


class SlideTypes:
    LIST = dict()

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    file = io.open(os.path.join(__location__, "types_dict"), 'r', encoding='utf-8')
    file_content = file.read()
    lines = file_content.split("\n")
    while len(lines)>0:
        # si la ligne est d un nouveau type alors on créer un indice dans le dict
        if lines[0].startswith("###") and lines[0].endswith("###"):
            # On récupère la clé
            words = lines[0].split("###")
            # On initialise la LISTe de mots
            if words[1] not in LIST:
                LIST[words[1]] = []
            # On retire la ligne de type de la LISTe des lignes
            lines.remove(lines[0])
            # On ajoute les lignes suivantes tant que l'on ne rencontre pas une ligne qui commence par ###
            while len(lines)>0:
                if lines[0].startswith("###") and lines[0].endswith("###"):
                    break
                else:
                    LIST[words[1]].append(lines[0])
                    lines.remove(lines[0])


if __name__ == '__main__':
    # TESTS
    for words in Types.LIST:
        print words
        for word in Types.LIST[words]:
            print "\t"+word