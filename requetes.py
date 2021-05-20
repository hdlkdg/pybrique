#!/usr/bin/python3

"""
Ce ficher contient une liste de requêtes qui interrogent les BD relationnelles de la BnF et DBpedia pour obtenir des infos diverses et variées ! Les requêtes sont divisées en deux classes Python : une pour l'artiste, l'autre pour l'oeuvre.

L'usage :
    import requetes
    nomDUnArtiste = requetes.Artiste("identifiant_ark")
    biographie = nomDUnArtiste.bio()
    photo = nomDUnArtiste.img()
    etc.

"""

import sys, os, json
from incat import sortInCat, aboutInCat, partInCat, inBibliozik
from SPARQLWrapper import SPARQLWrapper, JSON

class Artiste:

    def __init__(self, ark):
        self.ark = ark

    # Récupérer les données de la BnF
    def BNF(self):

        ark = self.ark
        final_result = {} # Le résultat sera un dictionnaire

        # BnF pour endpoint
        sparql = SPARQLWrapper("https://data.bnf.fr/sparql")
        
        # La requête elle-même
        queryString = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX schemaorg: <http://schema.org/>
        SELECT DISTINCT ?name ?man ?about ?dbpedia ?imslp
        WHERE {
        <http://data.bnf.fr/""" + str(ark) + """> skos:prefLabel ?name .
        <http://data.bnf.fr/""" + str(ark) + """> foaf:focus ?uri_auteur .
        OPTIONAL { ?uri_auteur owl:sameAs ?dbpedia .
        FILTER (regex(?dbpedia, 'dbpedia')) }
        OPTIONAL { <http://data.bnf.fr/""" + str(ark) + """> schemaorg:sameAs ?imslp .
        FILTER (regex(?imslp, 'imslp')) }
        }
        """
        sparql.setQuery(queryString)

        # Convertir en JSON
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        # Les valeurs des resultats
        name = result['results']['bindings'][0]['name']['value']
        try:
            dbpedia = result['results']['bindings'][0]['dbpedia']['value']
        except:
            dbpedia = ""
        try:
            imslp = result['results']['bindings'][0]['imslp']['value']
        except:
            imslp = ""

        # Organiser les valeurs en dictionnaire
        final_result['Nom'] = name
        # Exception pour quelques auteurs francisés :
        exceptions = { 'Johann Sebastian Bach (1685-1750)':'http://fr.dbpedia.org/resource/Johann_Sebastian_Bach' }
        if name in exceptions:
            final_result['DBpedia'] = exceptions[name]
        else:
            final_result['DBpedia'] = dbpedia
        final_result['Imslp'] = imslp

        return final_result

    # Obtenir les oeuvres d'un auteur - séparement pour rapidité
    def BNFWorks(self):
        
        ark = self.ark
        final_result = [] # Le résultat sera une liste

        # BnF pour endpoint
        sparql = SPARQLWrapper("https://data.bnf.fr/sparql")
        
        # La requête elle-même
        queryString = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdarelationships: <http://rdvocab.info/RDARelationshipsWEMI/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT DISTINCT ?man ?title ?date ?name
        WHERE {
        <http://data.bnf.fr/""" + str(ark) + """> foaf:focus ?uri_auteur ;
        skos:prefLabel ?name .
        ?exp dcterms:contributor ?uri_auteur .
        ?man rdarelationships:expressionManifested ?exp ;
        dcterms:title ?title ;
        dcterms:date ?date ;
        dcterms:description ?description .
        OPTIONAL { FILTER (xsd:integer (?date) > '1980'^^xsd:integer) }
        FILTER CONTAINS (?description, "disque") .
        }
        """
        sparql.setQuery(queryString)

        # Convertir en JSON
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        try:
            for i in result['results']['bindings']:
                d = {
                        'Titre':i['title']['value'],
                        'ARK':i['man']['value'],
                        'Date':i['date']['value'],
                        'Auteur':i['name']['value']
                        }
                final_result.append(d)
        except:
            pass

        return final_result

    # Obtenir les oeuvres disponibles sur Gallica
    def WorksGallica(self):

        ark = self.ark
        final_result = []

        # BnF pour endpoint
        sparql = SPARQLWrapper("https://data.bnf.fr/sparql")

        # La requête
        queryString = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX rdarelationships: <http://rdvocab.info/RDARelationshipsWEMI/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT DISTINCT ?gallica ?titre ?date ?name
        WHERE { 
        <http://data.bnf.fr/""" + str(ark) + """> foaf:focus ?uri_auteur ;
        skos:prefLabel ?name .
        ?oeuvre dcterms:creator ?uri_auteur .
        ?manifestation rdarelationships:workManifested ?oeuvre ;
        rdarelationships:electronicReproduction ?gallica ;
        dcterms:title ?titre ;
        dcterms:date ?date .
        }
        """
        sparql.setQuery(queryString)

        # Convertir en JSON
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        # Organiser en dictionnaire
        try:
            for i in result['results']['bindings']:
                d = {
                        'Gallica':i['gallica']['value'],
                        'Titre':i['titre']['value'],
                        'Date':i['date']['value'],
                        'Auteur':i['name']['value']
                        }
                final_result.append(d)
        except:
            pass
        
        return final_result

    # Obtenir les oeuvres sur un auteur - séparement pour rapidité
    def BNFAbout(self):
        
        ark = self.ark
        final_result = [] # Le résultat sera une liste

        # BnF pour endpoint
        sparql = SPARQLWrapper("https://data.bnf.fr/sparql")
        
        # La requête elle-même
        queryString = """
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX rdarelationships: <http://rdvocab.info/RDARelationshipsWEMI/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT DISTINCT ?about ?title ?date ?name
        WHERE {
        ?about dcterms:subject <http://data.bnf.fr/""" + str(ark) + """#about> ;
        dcterms:title ?title ;
        dcterms:date ?date ;
        rdarelationships:expressionManifested ?expr .
        ?expr <http://id.loc.gov/vocabulary/relators/aut> ?uri_aut .
        ?aut foaf:focus ?uri_aut ;
        skos:prefLabel ?name .
        }
        """
        sparql.setQuery(queryString)

        # Convertir en JSON
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        # Organiser en liste
        for i in result['results']['bindings']:
            try:
                d = {
                        'ARK':i['about']['value'],
                        'Titre':i['title']['value'],
                        'Date':i['date']['value'],
                        'Auteur':i['name']['value']
                        }
                final_result.append(d)
            except:
                pass

        return final_result

    # Obtenir les données de DBpedia
    def DBpedia(self):
        
        # DBpedia pour endpoint
        sparql = SPARQLWrapper("http://fr.dbpedia.org/sparql")
        
        final_result = {}

        if self.BNF()['DBpedia'] == "":
            url = "http://fr.dbpedia.org/resource/" + self.BNF()['Nom'].replace(" ","_") # Bon, ça commence à être freestyle
        else:
            url = self.BNF()['DBpedia']


        # La requête SPARQL
        queryString = """
            PREFIX dbpedia: <http://dbpedia.org/ontology>
            SELECT ?bio ?img ?caption
            WHERE { 
            <""" + str(url) + """> dbpedia-owl:abstract ?bio ;
            dbpedia-owl:thumbnail ?img .
            OPTIONAL { <""" + str(url) + """> dbpedia-owl:thumbnailCaption ?caption . }
            FILTER langMatches(lang(?bio),"fr")
            }"""
        sparql.setQuery(queryString)
        
        # Convertir en JSON
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        try: 
            bio = result['results']['bindings'][0]['bio']['value']
        except:
            bio = "Nous n'avons pas réussi à trouver la biographie de cet auteur"
        try:
            img = result['results']['bindings'][0]['img']['value']
            caption = result['results']['bindings'][0]['caption']['value']
        except:
            img = ""
            caption = ""

        # Organiser en dictionnaire
        final_result['Bio'] = bio
        final_result['Image'] = img
        final_result['Caption'] = caption

        return final_result

    # Récupérer des liens pertinents de la BnF s'il y en a (MusicBrainz et Wikipedia)
    def BNFLiens(self):
        
        ark = self.ark
        final_result = {} # Le résultat sera un dictionnaire

        # BnF pour endpoint
        sparql = SPARQLWrapper("https://data.bnf.fr/sparql")
        
        # La requête elle-même
        queryString = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?wkpd ?musicbrainz 
        WHERE {
         OPTIONAL {
            <http://data.bnf.fr/""" + str(ark) + """> skos:exactMatch ?wkpd ;
                                                      skos:exactMatch ?musicbrainz .
        FILTER regex(?wkpd, "wikipedia") .
        FILTER regex(?musicbrainz, "musicbrainz") .
            }
        }
        """
        sparql.setQuery(queryString)

        # Convertir en JSON
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        # Attribuer les valeurs
        for i in result['results']['bindings']:
            try:
                wkpd = result['results']['bindings'][0]['wkpd']['value']
            except:
                wkpd = ""
            try:
                musicbrainz = result['results']['bindings'][0]['musicbrainz']['value']
            except:
                musicbrainz = ""

        # Organiser en dictionnaire
        final_result['Wikipedia'] = wkpd
        final_result['MusicBrainz'] = musicbrainz

        return final_result
    
    # Récupérer le site web s'il y en a un
    def BNFSite(self):
        
        ark = self.ark

        # BnF pour endpoint
        sparql = SPARQLWrapper("https://data.bnf.fr/sparql")
        
        # La requête elle-même
        queryString = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?site
        WHERE {
        OPTIONAL { <http://data.bnf.fr/""" + str(ark) + """#about> foaf:homepage ?site }
        }
        """
        sparql.setQuery(queryString)

        # Convertir en JSON
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        try:
            url = result['results']['bindings'][0]['site']['value']
        except:
            url = ""

        return url

    # Une liste de fonctions pour simplifier la syntaxe

    def name(self):
        return self.BNF()['Nom']

    def bio(self):
        return self.DBpedia()['Bio']

    def img(self):
        return self.DBpedia()['Image']

    def caption(self):
        return self.DBpedia()['Caption']

    def partitions(self):
        name = self.BNF()['Nom']
        return partInCat(name)

    def imslp(self):
        return self.BNF()['Imslp']
    
    def works(self):
        return self.BNFWorks()

    def worksincat(self):
        local = sortInCat(self.BNF()['Nom'])
        return local

    def gallica(self):
        return self.WorksGallica()

    def about(self):
        return self.BNFAbout()

    def aboutincat(self):
        local = aboutInCat(self.BNFAbout())
        return local

    def bibliozik(self):
        ark = self.ark
        return inBibliozik(ark)

    def wikipedia(self):
        return self.BNFLiens()['Wikipedia']
    
    def musicbrainz(self):
        return self.BNFLiens()['MusicBrainz']

    def site(self):
        return self.BNFSite()
