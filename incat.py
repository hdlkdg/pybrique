# Ceci est un petit script pour vérifier si une manifestation est dans le catalogue local

import sys, os, csv
from pymarc import MARCReader

# Uniformiser les noms que les gens écrivent n'importe comment et sans aucune discipline. C'est affreux.
def autoCorrect(name):
    string = str(name)
    if "," in string:
        better = string.split(", ")[1] + " " + string.split(", ")[0]
        return better.replace(".","")
    else:
        return string
"""
# Est-ce qu'un document est dans le catalogue local ?
# Cette fonction aligne une entrée existante sur la BnF par date, titre et auteur ; ne fonctionne pas très bien.
def sortInCat(l):
    final_result = []
    with open('catalogue.mrc', 'rb') as file:
        reader = MARCReader(file)
        for record in reader:
            if record['245']['b']:
                titlemrc = str(record['245']['a']) + " : " + str(record['245']['b'])
            else:
                titlemrc = str(record['245']['a'])
            try:
                if record['100']:
                    authormrc = autoCorrect(str(record['100']['a']))
                else:
                    authormrc = str(record['110']['a'])
            except:
                pass
            try:
                maybe = str(record['008'])
                datemrc1 = maybe.split('\\')[0][-4:]            
                if maybe.split('\\')[0][-5] == 's':
                    datemrc2 = ''
                else:
                    datemrc2 = maybe.split('\\')[0][-8:-4]
            except:
                pass
            for d in l:
                if (d['Titre'].lower() in titlemrc.lower() or titlemrc.lower() in d['Titre'].lower()) and (d['Auteur'] in authormrc or authormrc in d['Auteur']) and (d['Date'] in datemrc1 or d['Date'] in datemrc2):
                    final_result.append(d)

        return final_result
"""
# Est-ce qu'une oeuvre est dans le catalogue local ? Cette fonction se contente de récupérer toutes les oeuvres du même auteur
def sortInCat(name):
    final_result = []
    with open('catalogue.mrc', 'rb') as file:
        reader = MARCReader(file)
        for record in reader:
            try:
                if record['100']:
                    authormrc = autoCorrect(str(record['100']['a']))
                else:
                    authormrc = str(record['110']['a'])
            except:
                authormrc = record['700']['a']
            if name.lower() in authormrc.lower() or authormrc.lower() in name.lower():
                titre = record['245']['a']
                try:
                    ed = record['260']['a'] + " " + record['260']['b'] + " " + record['260']['c']
                except:
                    ed = ""
                try:
                    type_doc = record['300']['a']
                except:
                    type_doc = ""
                try:
                    maybe = str(record['008'])
                    date = maybe.split('\\')[0][-4:]
                except:
                    date = ""
                d = {
                        'Titre':titre,
                        'Edition':ed,
                        'Format':type_doc,
                        'Date':date
                        }
                final_result.append(d)
    return final_result

# Quels sont les oeuvres au sujet de l'auteur (BnF) qui existent dans le catalogue local ?
def aboutInCat(l):
    final_result = []
    with open('catalogue.mrc', 'rb') as file:
        reader = MARCReader(file)
        for record in reader:
            try:
                author = autoCorrect(str(record['100']['a']))
                if record['245']['b']:
                    title = record['245']['a'] + " " + record['245']['b'].strip('/=') + "!"
                else:
                    title = record['245']['a'].strip('/=')
                for work in l:
                    if (title.lower() in work['Titre'].lower() or work['Titre'].lower() in title.lower()) and (work['Auteur'].lower() in author.lower()):
                        final_result.append(work)
            except:
                pass
    return final_result


            

# Est-ce qu'une partition est dans le catalogue ?
# Pour plus tard : il n'y a pas besoin de deux extraits .mrc différents, car le champ 245$h permet d'identifier les partitions
def partInCat(name):
    final_result = []
    with open('catalogue.mrc', 'rb') as file:
        reader = MARCReader(file)
        for record in reader:
            if '[mus.]' in str(record['245']['h']):
                try:
                    if record['100']:
                        authormrc = autoCorrect(str(record['100']['a']))
                    else:
                        authormrc = str(record['110']['a'])
                    if name.lower() in authormrc.lower() or authormrc.lower() in name.lower():
                        titre = record['245']['a']
                        final_result.append(titre)
                except:
                    pass
    return final_result

# Est-ce qu'il y a une chronique Bibliozik qui parle de cet auteur ?
def inBibliozik(ark):
    final_result = []
    with open('bibliozik.csv') as file:
        readable = csv.DictReader(file)
        for row in readable:
            if row['Sujet'] == ark:
                entry = {
                        'Titre':row['Titre'],
                        'URL':row['URL'],
                        'Date':row['Date']
                        }
                final_result.append(entry)
    return final_result
