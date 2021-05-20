# pybrique

_pybrique_ (**py** pour Python et **brique** pour brique, sans raison, c'est comme ça) est un nom que j'ai donné à l'application créée dans le
cadre de mon stage au Pôle Musique de la Médiathèque José Cabanis de
Toulouse (mars-mai 2021). Elle est écrite en Python, ne pèse pas grand-chose et est publiée sous [GPLv3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html).

### Table de matières
- [Que fait _pybrique_ ?](https://github.com/hdlkdg/pybrique#que-fait-pybrique-)
- [Les usages possibles]
- [Où est-ce que ça boîte ?]
- [La structure](#structure)
- [Comment l'utiliser ?](#utiliser)
	* [Préparation](#preparation)
	* [Installation et lancement](#installation)
	* [Utilisation](#utilisation)
- [Bibliographie](#bibliographie)
- [Contact](#contact)

## Que fait _pybrique_ ?
* Il utilise le langage de requête SPARQL (**S**PARQL **P**rotocol
  **a**nd **R**DF **Q**uery **L**anguage) pour accéder aux données ouvertes de la [Bibliothèque
nationale de France](https://data.bnf.fr) et de la [DBpédia](http://fr.dbpedia.org).
* Il en extrait des données intéressantes sur un auteur : image,
  biographie, œuvres, ouvrages dont il ou elle fait objet, etc.
* Il aligne ces informations entre le catalogue local et les informations trouvées sur le Web : les résultats des requêtes SPARQL mais aussi les liens sur [Gallica](https://gallica.bnf.fr), sur [IMSLP](https://imslp.org/wiki/Main_Page) et, qui sait, possiblement autre chose aussi.
* Il permet d'exécuter des requêtes choisies sur le programme via son API et assembler les informations récueillies comme on veut.

## Que permet _pybrique_ ?
* Enrichissement automatisé des contenus produits par des vrais humains (ex.
  bibliothécaires)
* Médiation centré sur le _contenu_ par opposition au _support_.
* Utilisation de quelques avancées de la [transition
  bibliographique](https://www.transition-bibliographique.fr/) (TB) sans s'y lancer
  entièrement. 

## Où boîte _pybrique_ ?{#problemes}
_pybrique_ est avant tout une application de _recherche_ pour ouvrir des pistes pour
l'exploitation des données du Web sémantique dans un cadre documentaire comme
celui des bibliothèques. Ça veut dire que les questions de sa déployabilité
ont été sécondaires dans sa création. Cela pose quelques
limites :

- Les requêtes SPARQL se font sur les endpoints distants, ce qui ralentit
  considérablement le chargement. 
  Les données de la BnF peuvent être récupérées [ici](https://api.bnf.fr/dumps-de-databnffr) pour être interrogées localement avec une plus grande vitesse. Cela impliquerait quelques
  modifications mineures du code, notamment du fichier `requetes.py`.
- L'identification des auteurs se fait via l'identifiant
  pérenne
  [ARK](https://www.transition-bibliographique.fr/17-10-10-numero-frbnf-identifiant-ark/) qu'il faut aller chercher manuellement sur [_data.bnf.fr_](https://data.bnf.fr). L'alignement entre les œuvres trouvées sur la base de données de la BnF et le catalogue local se fait à travers plusieurs éléments plus ou moins sûrs : le titre, l'auteur, la date, etc. Lorsque les identifiants ARK seront intégrés aux notices du catalogue local dans le cadre de la TB, les contenus entre différentes bases de données seront récupérables beaucoup plus facilement, sans travail supplémentaire d'alignement. Pour l'instant, _pybrique_ le fait à sa manière, donc avec une certaine marge d'erreur.

## De quoi est fait _pybrique_ ?
_pybrique_ est fait de deux « composantes ».

1. Le fichier `requetes.py` contient une classe de requêtes `Artiste`. Après l'importation de la classe, il suffit de l'initier en attribuant l'identifiant ARK :

		mahler = Artiste('ark:/12148/cb13896959d')

	Les méthodes de la classe ne sont rien d'autre que des requêtes SPARQL sur les bases de données de type RDF. Par exemple, la méthode suivante envoie une requête SPARQL pour obtenir la biographie de Mahler depuis DBpedia : 
		
		mahler.bio()

	De manière générale, `requetes.py` contient un code assez propre et bien commenté, donc facile à prendre en main à condition de connaître les rudiments de Python.

2. L'API (interface de programmation) qui permet à une plateforme de votre choix de communiquer avec le programme principal en lui envoyant des requêtes.

## Comment utiliser _pybrique_ ?

### Préparation

Pour que _pybique_ fonctionne correctement, il faut qu'il puisse acceder aux fichiers suivants :

- `bibliozik.csv` est un catalogue des chroniques à 4 colonnes (_Titre_, _URL_, _ARK_ et _Date_) qui doit être placé dans le dossier principal de l'application ;
- `catalogue.mrc` est un extrait du catalogue en format _Marc21_ qui doit lui aussi être placé dans le dossier principal de l'application.

### Installation et lancement

La meilleure manière d'installer les dépendances de _pybrique_ est en passant par le gestionnaire de paquets Python [pip](https://pypi.org/project/pip/). Pour ce faire, il faut suivre les étapes suivantes :

- Installer [Python3](https://www.python.org/downloads/) s'il n'est pas encore installé
- Installer [pip](https://pypi.org/project/pip/)
- Ouvrir l'interface en ligne de commande dans le dossier _pybrique_ et exécuter la commande suivante :

		$ pip install -r requirements.txt

Cela va installer les dépendances suivantes :

- Flask==2.0.0
- Flask\_RESTful==0.3.8
- pymarc==4.1.0
- marshmallow==3.12.1
- dicttoxml==1.7.4
- SPARQLWrapper==1.8.5

Une fois les dépendaces installées, lancer l'application en exécutant

		$ python app.py

### Utilisation

Une fois l'application démarrée, les requêtes sur l'API se construisent de manière suivante :
		
		http://<URL>/artist?ark=<identifiant ark>&info=<type d'info>

Par exemple, si l'application est lancée sur `http://127.0.0.1:5000/` et l'on veut récupérer la biographie de Gustav Mahler dont on connaît l'identifiant ARK (`ark:/12148/cb13896959d`), la requête sera la suivante :

		http://127.0.0.1:5000/artist?ark=ark:/12148/cb13896959d&info=bio

qui donnera la réponse sérialisée en XML :

		<root>
		<response type="str">
		Gustav Mahler (prononcé [ˈɡʊstaf ˈmaːlɐ] en allemand), né à Kaliště dans l'Empire d'Autriche (aujourd'hui en République tchèque), le 7 juillet 1860 et mort à Vienne le 18 mai 1911, est un compositeur, pianiste et chef d'orchestre autrichien. Plus célèbre en son temps comme chef d'orchestre, son nom reste attaché aujourd’hui à son œuvre de compositeur dont la dimension orchestrale et l'originalité musicale jettent un pont entre la fin du XIXe siècle et la période moderne. Il est l'auteur de dix symphonies (la réduction d’orchestre (en) de la dernière est complète, mais son orchestration est inachevée) et plusieurs cycles de lieder.
		</response>
		</root>

Les méthodes correspondant aux types d'information a récupérer sont les suivantes :

- `name` - le nom de l'artiste
- `bio` - la biographie de l'artiste
- `img` - une image de l'artite (URL)
- `caption` - la légende associée à l'image
- `partitions` - la liste des partitions de l'auteur sur le catalogue de la médiathèque
- `imslp` - le lien vers les partitions de l'auteur sur [IMSLP](https://imslp.org/wiki/Main_Page)
- `works` - la liste de _toutes_ les œuvres de l'auteur connues de la BnF 
- `worksincat` - la liste des œuvres de l'auteur sur le catalogue de la médiathèque
- `gallica` - la liste des réproductions numériques des œuvres de l'auteur sur [Gallica](https://gallica.bnf.fr)
- `about` - la liste de _toutes_ les œuvres traitant de l'auteur connues de la BnF
- `aboutincat` - la liste des œuvres traitant de l'auteur sur le catalogue de la médiathèque
- `bibliozik` - les chroniques [Bibliozik](https://www.bibliotheque.toulouse.fr/sites-thematiques/bibliozik/chronique-musique/) traitant de l'auteur
- `wikipedia` - le lien Wikipédia de l'auteur
- `musicbrainz` - le lien MusicBrainz de l'auteur
- `site` - le site de l'auteur

Si l'on préfère les réponses sérialisées en JSON plutôt que XML, cela devrait se faire facilement en modifiant `app.py`

## Bibliographie

Pour comprendre un peu plus les enjeux de la TB et de l'usage des technologies du web sémantique dans un contexte documentaire, la bibliographie ci-dessous propose quelques pistes de lecture et d'exploration autour du sujet.

### Ouvrages
- BERMES, Emmanuelle, ISAAC, Antoine et POUPEAU, Gautier, 2013. _Le web sémantique en bibliothèque_. Paris : Ed. du Cercle de la librairie, 2013. 176 p.
- BERMES, Emmanuelle (dir.), 2016. _Vers de nouveaux catalogues_. Paris : Ed. du Cercle de la librairie. 171 p. 
- DELESTRE, Nicolas et MALANDAIN, Nicolas, 2017. _Du web des documents au web sémantique_. Bois-Guillaume : Klog. 199 p.
- MESGUICH Véronique, 2017. 4. Rendre les catalogues de bibliothèques plus visibles sur le Web. In : MESGUICH, Véronique (dir.). _Bibliothèques : le Web est à vous_. Paris, Éd. du Cercle de la Librairie, p. 77-103.
- TOUSSAINT, Claire, LERESCHE, Françoise, PUYRENIER, Frédéric et al. (dir.), 2018. _Cataloguer aujourd'hui : identifier les œuvres, les expressions, les personnes selon RDA-FR_. Paris : Ed. du Cercle de la librairie. 199 p.

### Articles
- ADBS (éd.), 2016. Web de données et création de valeurs : le champ des possibles. _I2D - Information, données & documents. 2016. Vol. 53, N° 2.
- AIOUTZ, Renaud, 2018. Alignements des données : s’habituer à finir plus… sans finir. _Arabesques_. N° 89, pp. 20-21. [Consulté le 14/05/2021]. Disponible sur : <https://publications-prairial.fr/arabesques/index.php?id=248>
- ANGJELI, Anila, 2011. La normalisation en bibliothèque à l'heure du web sémantique. _Documentaliste - Sciences de l'Information_. Vol. 48, n° 4. [Consulté le 14/05/2021]. Disponible sur : <https://hal.archives-ouvertes.fr/hal-00875829>
- BERMES, Emmanuelle, 2016. Web de données et bibliothèques : l’évolution du modèle d’agrégation des données. _I2D - Information, données & documents_. Vol. 53, N° 2, p. 37-37.
- BOURNERIE, Pierre, 2020. Le petit laboratoire sémantique : expérimentation à la BM de Fresnes. _Site de la Transition Bibliographique_ [en ligne]. Mis à jour le 12/05/2020. [Consulté le 14/05/2021]. Disponible sur : <https://www.transition-bibliographique.fr/2018-04-09-petit-laboratoire-semantique-experimentation-bm-fresnes/>
- CAVALIE, Etienne et GEOFFROY, Géraldine, 2015. Transformer les collections en information grâce aux technologies du web sémantique. _Arabesques_. N° 80, pp. 19-20. [Consulté le 14/05/2021]. Disponible sur : <https://hal.archives-ouvertes.fr/hal-01179423>
- JACQUOT, Olivier, 2017. _data.bnf.fr_ pour les nuls. _Carnet de recherche à la Bibliothèque nationale de France_ [en ligne]. Mis en ligne le 21/11/2017. [Consulté le 14/05/2021]. Disponible sur : <https://bnf.hypotheses.org/2181>
- KEMBELLEC, Gérald, 2016. Le web de données en contexte bibliothécaire. _I2D - Information, données & documents_. Vol. 53, N° 2, p. 30-31.
- MENON, Bruno, 2016. Comprendre les standards du web de données. _I2D - Information, données & documents_. Vol. 53, N° 2, p. 32-34. 

### Conférences
- AZOUZ, Kaouther, 2014. Le web sémantique, média de valorisation des pratiques professionnelles en bibliothèques. In : _9ème Journée Jeunes Chercheurs du laboratoire GERiiCO de Université Lille 3_. Villeneuve d’Ascq, France, 2014. [Consulté le 14/05/2021]. Disponible sur : <https://hal.archives-ouvertes.fr/hal-01637615>
- BERMES, Emmanuelle, BOULET, Vincent et LECLAIRE, Céline, 2016. Améliorer l’accès aux données des bibliothèques sur le web : l’exemple de data.bnf.fr. In : National Libraries, International Federation of Library Associations and Institutions (IFLA). _IFLA WLIC 2016 – Columbus, OH – Connections. Collaboration. Community in Session 201._ Columbus, États-Unis, 2016. [Consulté le 14/05/2021]. Disponible sur : <https://hal.archives-ouvertes.fr/hal-01393255>

### Ressources en ligne
- Bibliothèque municipale de Fresnes, 2020. Pétit laboratoire sémantique. _Site de de la Transition Bibliographique_ [en ligne]. [Consulté le 14/05/2021]. Disponible sur : <http://bm.fresnes94.fr/semlab/>
- Bibliothèque nationale de France, 2021. Web sémantique et modèle de données. _data.bnf.fr_ [en ligne]. Mis à jour le 14/01/2021. [Consulté le 14/05/2021]. Disponible sur : <https://data.bnf.fr/fr/semanticweb>
- Bibliothèque nationale de France, 2020. SPARQL endpoint de data.bnf.fr. _data.bnf.fr_ [en ligne]. [Consulté le 14/05/2021]. Disponible sur : <https://api.bnf.fr/fr/sparql-endpoint-de-databnffr>
- World Wide Web Consortium, 2013. SPARQL 1.1 Query Language. _W3C_ [en ligne]. Mis à jour le 21/03/2013. [Consulté le 14/05/2021]. Disponible sur : <https://www.w3.org/TR/sparql11-protocol/>

## Contact

Voilà tout. Si vous voulez me contacter, vous pouvez vous adresser à _lukk.plt_ [bzgt] _gmail.com_ et je vous répondrai si je peux.
