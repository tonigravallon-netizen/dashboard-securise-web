"""
seed_routes.py - Routes de peuplement de la base ARCANA WIKI
Cree 10 articles detailles sur les theories du complot dans Firestore.
"""

from flask import Blueprint, redirect, url_for, flash
from flask_login import current_user, login_required
from .helpers import get_firebase, render_markdown, slugify, truncate_text
from datetime import datetime, timezone, timedelta
import random

seed_bp = Blueprint("seed", __name__)


@seed_bp.route("/admin/seed-wiki")
@login_required
def seed_wiki():
    fb = get_firebase()

    # Verifier si des articles existent deja
    existing = fb.list_articles(status="published", limit=1)
    if existing:
        flash("Les archives sont deja remplies!", "info")
        return redirect(url_for("wiki.home"))

    # Generer des timestamps repartis sur les 30 derniers jours
    base_date = datetime.now(timezone.utc)
    timestamps = []
    for i in range(10):
        offset_days = random.randint(1, 30)
        offset_hours = random.randint(0, 23)
        offset_minutes = random.randint(0, 59)
        ts = base_date - timedelta(days=offset_days, hours=offset_hours, minutes=offset_minutes)
        timestamps.append(ts.isoformat())
    timestamps.sort()

    author_username = current_user.username or current_user.display_name or "ARCANA"

    # =========================================================================
    # ARTICLE 1 : La Terre Plate et le Mur de Glace Antarctique
    # =========================================================================
    content_1 = """### Introduction

La theorie de la Terre plate connait un regain de popularite spectaculaire depuis les annees 2010, portee par les reseaux sociaux et une mefiance croissante envers les institutions scientifiques. Selon ses partisans, notre planete ne serait pas une sphere tournant dans le vide spatial, mais un **disque plat** entoure par un immense **mur de glace** que nous appelons l'Antarctique.

### Le Modele de la Terre Plate

Dans le modele le plus repandu, la Terre serait un disque avec le **Pole Nord au centre** et l'Antarctique formant une barriere circulaire sur les bords. Le Soleil et la Lune seraient des objets relativement petits, situes a quelques milliers de kilometres au-dessus du disque, tournant en cercle au-dessus de sa surface. Ce modele expliquerait, selon ses defenseurs, pourquoi le soleil semble se lever et se coucher : il s'eloignerait simplement au-dela de la portee de notre vision.

Le mur de glace antarctique atteindrait une hauteur estimee entre **60 et 150 metres**, s'etendant sur des milliers de kilometres. Au-dela de ce mur, certains theoriciens evoquent d'**autres terres inconnues**, voire d'autres civilisations cachees au monde.

### Le Traite de l'Antarctique (1959)

L'un des arguments les plus frequemment cites par les partisans de la Terre plate est le **Traite de l'Antarctique**, signe le 1er decembre 1959 par 12 nations en pleine Guerre froide. Ce traite interdit toute exploitation militaire et miniere du continent et restreint severement l'acces aux civils. Pour les theoriciens, ce traite serait la preuve que les gouvernements du monde entier **conspirent pour empecher quiconque de decouvrir la verite** sur le bord du monde.

Pourquoi les Etats-Unis et l'URSS, en plein conflit ideologique, se seraient-ils mis d'accord sur un point aussi precis ? C'est la question que posent invariablement les flat-earthers.

### L'Operation Highjump (1947)

L'**amiral Richard E. Byrd** mena en 1946-1947 une expedition militaire massive en Antarctique baptisee *Operation Highjump*. Avec **4 700 hommes, 13 navires et 33 avions**, cette operation etait disproportionnee pour une simple mission scientifique. Byrd aurait declare dans une interview au journal chilien *El Mercurio* qu'il existait au-dela du Pole Sud *"un nouveau territoire aussi grand que les Etats-Unis"*.

Les sceptiques affirment que ces propos ont ete **deformes et sortis de leur contexte**, et que l'operation avait des objectifs militaires classiques lies a la Guerre froide, notamment l'entrainement au combat en conditions polaires.

### La Conspiration de la NASA

Pour les tenants de la Terre plate, la **NASA** (National Aeronautics and Space Administration) est l'architecte principal de la tromperie. Les images satellites de la Terre seraient des **composites numeriques** (ce que la NASA admet partiellement, les images etant assemblees a partir de multiples cliches). Les missions Apollo seraient des mises en scene filmees, et l'ensemble du programme spatial serait un gigantesque detournement de fonds publics.

La theorie du **dome** ou *firmament* complete ce tableau : une structure solide et transparente recouvrirait le disque terrestre, empechant toute sortie vers l'espace. Les fusees ne feraient que longer cette paroi avant de retomber dans l'ocean.

### Le Dome et le Firmament

La notion de *firmament* trouve ses racines dans les textes bibliques, notamment la **Genese**, ou Dieu cree un *"firmament au milieu des eaux"*. Pour certains partisans de la Terre plate, cette reference scripturaire constitue une preuve supplementaire. Le dome serait compose d'un materiau inconnu, possiblement de l'eau a l'etat solide, expliquant la couleur bleue du ciel.

### Arguments et Contre-Arguments

Les flat-earthers citent l'**absence de courbure visible** a l'oeil nu, le fait que l'eau *"cherche toujours son niveau"*, et l'impossibilite ressentie de se tenir *"a l'envers"* sur une sphere. Les scientifiques repondent par la **gravite**, les photographies depuis l'espace, la navigation maritime, les fuseaux horaires et les observations astronomiques reproductibles.

La communaute scientifique considere unanimement la Terre plate comme une **pseudo-science** contredite par des siecles d'observations. Mais pour ses adeptes, cette unanimite meme est suspecte et constitue la preuve d'un **consensus fabrique**.

### Conclusion

Qu'elle soit prise au serieux ou consideree comme un phenomene sociologique fascinant, la theorie de la Terre plate revele une **crise de confiance profonde** envers les institutions scientifiques et gouvernementales. Elle nous rappelle que dans l'ere de l'information, la verite est souvent une question de perspective, au sens propre comme au figure."""

    slug_1 = slugify("La Terre Plate et le Mur de Glace Antarctique")
    article_1 = {
        "title": "La Terre Plate et le Mur de Glace Antarctique",
        "title_lower": "la terre plate et le mur de glace antarctique",
        "slug": slug_1,
        "summary": truncate_text("Exploration de la theorie de la Terre plate, du mur de glace antarctique, du Traite de 1959, de l'Operation Highjump et de la conspiration NASA.", 200),
        "content": content_1,
        "content_html": render_markdown(content_1),
        "category": "science",
        "tags": ["terre-plate", "antarctique", "mur-de-glace", "flat-earth", "nasa"],
        "sources": [
            {"title": "The Flat Earth Society", "url": "https://www.tfes.org/", "type": "archive"},
            {"title": "Traite de l'Antarctique (1959)", "url": "https://www.ats.aq/", "type": "officiel"},
        ],
        "related_articles": [],
        "author_uid": current_user.uid,
        "author_username": author_username,
        "generated_by_ai": False,
        "ai_model": "",
        "status": "published",
        "credibility": "speculatif",
        "classification": "confidentiel",
        "views": random.randint(50, 5000),
        "upvotes": random.randint(5, 500),
        "downvotes": random.randint(0, 50),
        "comment_count": 0,
        "created_at": timestamps[0],
        "updated_at": timestamps[0],
        "featured": True,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Orlando-Ferguson-flat-earth-map_edit.jpg/640px-Orlando-Ferguson-flat-earth-map_edit.jpg",
    }

    # =========================================================================
    # ARTICLE 2 : L'Affaire Jeffrey Epstein - Le Reseau des Puissants
    # =========================================================================
    content_2 = """### Introduction

L'affaire Jeffrey Epstein est sans doute le **plus grand scandale de pedocriminalite** impliquant les elites mondiales de l'histoire moderne. Financier americain, condamne une premiere fois en 2008 dans des conditions scandaleusement clemente, Epstein a ete retrouve mort dans sa cellule le **10 aout 2019** dans des circonstances que beaucoup jugent impossibles. Son reseau de trafic sexuel impliquant des mineures met en lumiere un systeme de corruption et de protection au plus haut niveau du pouvoir.

### Le Reseau Epstein

Jeffrey Epstein, ne en 1953 a Brooklyn, a bati une fortune dont l'origine reste **largement inexpliquee**. Ancien professeur de mathematiques a la Dalton School de New York, il est devenu gestionnaire de fortune pour les ultra-riches, notamment le milliardaire **Leslie Wexner**, fondateur de L Brands (Victoria's Secret), qui lui a cede une propriete a Manhattan estimee a **77 millions de dollars**.

Epstein possedait un veritable **empire immobilier** : un hotel particulier a New York (East 71st Street), un ranch au Nouveau-Mexique (Zorro Ranch), un appartement a Paris, et surtout deux iles privees dans les Iles Vierges americaines, dont la tristement celebre **Little Saint James**, surnommee *"Pedophile Island"* ou *"Orgy Island"*.

### Little Saint James et le Temple Mysterieux

L'ile de Little Saint James, d'une superficie d'environ **28 hectares**, abritait des infrastructures troublantes. Les images satellites revelent un **temple bleu et blanc** de style oriental dont la fonction n'a jamais ete clairement etablie. Des temoignages de victimes evoquent des **abus systematiques** sur l'ile, ou des mineures etaient amenees regulierement.

Des **cameras de surveillance** etaient dissimulees dans toutes les pieces, suggerant qu'Epstein enregistrait ses invites dans des situations compromettantes a des fins de **chantage** potentiel. Cette hypothese est soutenue par plusieurs enqueteurs et victimes.

### Le Lolita Express

L'avion prive d'Epstein, un **Boeing 727** surnomme le *"Lolita Express"*, a effectue des centaines de vols entre 1997 et 2005 selon les **registres de vol** rendus publics. Parmi les passagers frequents figurent des noms retentissants :

- **Bill Clinton** : au moins **26 vols** documentes, dont plusieurs sans son detail de Secret Service
- **Prince Andrew** (duc d'York) : photographie a plusieurs reprises avec Epstein et accuse formellement par **Virginia Giuffre**
- **Bill Gates** : plusieurs rencontres documentees avec Epstein **apres** sa premiere condamnation de 2008
- **Donald Trump** : cite comme ami d'Epstein dans les annees 1990, declare en 2002 qu'Epstein aimait les femmes *"du cote jeune"*
- **Alan Dershowitz** : avocat celebre, accuse par des victimes

### La Mort Suspecte au MCC de Manhattan

Le 10 aout 2019, Jeffrey Epstein est retrouve mort dans sa cellule du **Metropolitan Correctional Center** (MCC) de Manhattan. Le verdict officiel : **suicide par pendaison**. Mais les circonstances sont extraordinairement suspectes :

- Epstein avait ete retire de la **surveillance anti-suicide** seulement 12 jours apres une premiere tentative
- Les **deux gardiens** assignes a sa surveillance se sont endormis et ont **falsifie les registres**
- Les **cameras de securite** devant sa cellule ont *"dysfonctionne"* exactement cette nuit-la
- Le medecin legiste prive engage par la famille, **Dr. Michael Baden**, a constate des fractures de l'os hyoide plus compatibles avec un **stranglement** qu'un suicide
- Son codtenu avait ete **transfere** la veille, le laissant seul en cellule

L'expression **"Epstein didn't kill himself"** est devenue un phenomene culturel mondial, exprimant le scepticisme generalise face a la version officielle.

### Ghislaine Maxwell et le Role de Recruteuse

**Ghislaine Maxwell**, fille du magnat de la presse **Robert Maxwell** (lui-meme mort dans des circonstances mysterieuses en 1991, soupconnees de liens avec le **Mossad**, le MI6 et le KGB), a ete la **principale recruteuse** du reseau Epstein. Condamnee en juin 2022 a **20 ans de prison**, elle a ete reconnue coupable de trafic sexuel de mineures.

Les liens entre Robert Maxwell et les services de renseignement israeliens alimentent la theorie selon laquelle Epstein aurait ete un **agent d'influence** utilisant le chantage sexuel comme outil de controle politique pour le compte du **Mossad** ou de la **CIA**.

### Le Carnet Noir

Le *"petit carnet noir"* d'Epstein, obtenu par son ancien majordome **Alfredo Rodriguez** (qui a tente de le vendre 50 000 dollars), contient les coordonnees de plus de **1 500 personnalites** : chefs d'Etat, PDG, artistes, scientifiques. La possession de ces contacts ne signifie pas necessairement une implication dans les crimes d'Epstein, mais l'ampleur du reseau est vertigineuse.

### Les Zones d'Ombre Persistantes

Plusieurs questions restent sans reponse :

- **D'ou venait reellement la fortune d'Epstein ?** Aucun client n'a jamais confirme publiquement lui avoir confie de l'argent en dehors de Wexner.
- **Qui a commande son elimination ?** Si c'en etait une.
- **Pourquoi les enquetes ont-elles ete si lentes et indulgentes pendant des decennies ?**
- **Combien de victimes au total ?** Les estimations vont de dizaines a des centaines.

### Conclusion

L'affaire Epstein est un cas d'ecole ou les **faits documentes** sont deja si graves qu'ils depassent la plupart des theories du complot. Les documents judiciaires, les temoignages des victimes et les preuves materielles dessinent le portrait d'un systeme de predation protege par les plus hautes spheres du pouvoir. La question n'est plus de savoir *si* un reseau existait, mais *jusqu'ou* il s'etendait et *qui* le protegeait reellement."""

    slug_2 = slugify("L'Affaire Jeffrey Epstein - Le Reseau des Puissants")
    article_2 = {
        "title": "L'Affaire Jeffrey Epstein - Le Reseau des Puissants",
        "title_lower": "l'affaire jeffrey epstein - le reseau des puissants",
        "slug": slug_2,
        "summary": truncate_text("Enquete sur le reseau de Jeffrey Epstein, le Lolita Express, l'ile Little Saint James, sa mort suspecte et les liens avec les elites mondiales.", 200),
        "content": content_2,
        "content_html": render_markdown(content_2),
        "category": "politique",
        "tags": ["epstein", "trafic", "elite", "lolita-express", "pedocriminalite"],
        "sources": [
            {"title": "Acte d'accusation SDNY 2019", "url": "https://www.justice.gov/usao-sdny/pr/jeffrey-epstein-charged-manhattan-federal-court-sex-trafficking-minors", "type": "officiel"},
            {"title": "Documents judiciaires - Ghislaine Maxwell", "url": "https://www.courtlistener.com/docket/4355835/giuffre-v-maxwell/", "type": "document"},
            {"title": "Flight logs Lolita Express", "url": "https://www.documentcloud.org/documents/1507315-epstein-flight-manifests.html", "type": "document"},
        ],
        "related_articles": [],
        "author_uid": current_user.uid,
        "author_username": author_username,
        "generated_by_ai": False,
        "ai_model": "",
        "status": "published",
        "credibility": "documente",
        "classification": "top-secret",
        "views": random.randint(50, 5000),
        "upvotes": random.randint(5, 500),
        "downvotes": random.randint(0, 50),
        "comment_count": 0,
        "created_at": timestamps[1],
        "updated_at": timestamps[1],
        "featured": True,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Aerial_image_of_Little_Saint_James_Island.jpg/640px-Aerial_image_of_Little_Saint_James_Island.jpg",
    }

    # =========================================================================
    # ARTICLE 3 : Les Emails et Documents Epstein Declassifies
    # =========================================================================
    content_3 = """### Introduction

En janvier 2024, une decision judiciaire historique a ordonne la **declassification de centaines de documents** lies a l'affaire Jeffrey Epstein, issus principalement du proces **Giuffre contre Maxwell**. Ces documents, longtemps scelles, ont revele des noms, des temoignages et des details que le public attendait depuis des annees. Mais la realite des revelations a ete plus nuancee que ce que beaucoup esperaient.

### La Declassification de 2024

Le juge **Loretta Preska** du tribunal federal du district sud de New York a ordonne la publication echelonnee de plus de **900 pages** de documents precedemment scelles. Cette decision faisait suite a des annees de batailles juridiques menees par le **Miami Herald** et d'autres medias invoquant le droit du public a l'information.

Les documents comprenaient des **depositions**, des **emails**, des **notes internes** et des **temoignages sous serment** provenant principalement du proces civil intente par Virginia Giuffre contre Ghislaine Maxwell en 2015.

### Les Noms Reveles

Plus de **150 personnes** sont mentionnees dans les documents declassifies, mais il est crucial de comprendre que **etre nomme ne signifie pas etre accuse**. Parmi les noms les plus mediatises :

- **Prince Andrew** : les depositions detaillent des rencontres avec Virginia Giuffre, confirmant des temoignages anterieurs
- **Bill Clinton** : mentionne a plusieurs reprises, notamment dans des temoignages de victimes placant sa presence sur l'ile
- **Alan Dershowitz** : nomme directement dans des accusations de contacts sexuels avec des mineures, qu'il nie categoriement
- **Jean-Luc Brunel** : le mannequin-scout francais retrouve mort dans sa cellule a Paris en **fevrier 2022**, un autre *"suicide"* controversé
- **Stephen Hawking** : mentionne dans un contexte non accusatoire, provoquant neanmoins un emoi mediatique

### La Controverse de la "Liste Epstein"

L'expression **"liste Epstein"** est devenue virale sur les reseaux sociaux, creant l'attente d'un document unique revelant tous les complices. En realite, une telle liste **n'existe pas** sous cette forme. Les documents declassifies sont un ensemble heterogene de pieces judiciaires ou des noms apparaissent dans des contextes tres differents : certains comme **temoins**, d'autres comme **accuses**, d'autres encore simplement **mentionnes** dans des conversations.

Cette confusion a ete exploitee pour des **campagnes de desinformation** et des reglement de comptes politiques, chaque camp designant les adversaires de l'autre comme *"sur la liste"*.

### Les Depositions des Victimes

Les temoignages les plus poignants des documents sont ceux des **victimes**. Johanna Sjoberg, Virginia Giuffre et d'autres femmes decrivent avec des details precis le **systeme de recrutement** mis en place par Maxwell et Epstein :

- Approche de jeunes filles vulnerables (souvent issues de milieux defavorises)
- Promesses de **carriere dans le mannequinat** ou d'aide financiere
- Premiers *"massages"* evoluant vers des **abus sexuels**
- Pressions psychologiques et **recompenses financieres** pour recruter d'autres victimes
- Menaces et intimidation pour maintenir le **silence**

### Les Accords de Non-Divulgation (NDA)

Les documents revelent l'existence de nombreux **NDA** (Non-Disclosure Agreements) signes entre les victimes et Epstein dans le cadre d'accords financiers. Ces accords, assortis de **compensations allant de 100 000 a plusieurs millions de dollars**, interdisaient aux victimes de parler publiquement de leurs experiences.

L'accord le plus scandaleux reste le **Non-Prosecution Agreement** de 2008 negocie par l'avocat **Alexander Acosta** (futur secretaire au Travail de Trump), qui a accorde a Epstein et a ses **co-conspirateurs nommes et non nommes** une immunite federale en echange d'un plaidoyer de culpabilite sur des charges mineures de l'Etat de Floride.

### Ce que les Documents Montrent vs les Attentes

Le public esperait des **revelations explosives** nommant des dizaines de complices celebres. La realite fut plus complexe :

**Ce qui a ete confirme :**
- L'ampleur du reseau de recrutement
- L'implication directe de Maxwell dans les abus
- Les liens documentees entre Epstein et de nombreuses personnalites
- Le caractere systematique et organise du trafic

**Ce qui reste flou :**
- Le role exact de chaque personnalite nommee
- L'etendue reelle du reseau de chantage
- Les liens avec les services de renseignement
- L'origine de la fortune d'Epstein

### Conclusion

La declassification des documents Epstein a constitue une etape importante pour la **transparence judiciaire**, mais n'a pas apporte le *"grand devoilement"* espere par beaucoup. Les documents confirment l'existence d'un **reseau criminel sophistique** protege par l'argent et le pouvoir, tout en laissant de nombreuses questions sans reponse. La verite complete sur l'affaire Epstein reste, pour l'heure, **enfouie sous des couches de secret, de pouvoir et de silence**."""

    slug_3 = slugify("Les Emails et Documents Epstein Declassifies")
    article_3 = {
        "title": "Les Emails et Documents Epstein Declassifies",
        "title_lower": "les emails et documents epstein declassifies",
        "slug": slug_3,
        "summary": truncate_text("Analyse des documents Epstein declassifies en 2024 : noms reveles, depositions des victimes, la controverse de la 'liste Epstein' et les NDA.", 200),
        "content": content_3,
        "content_html": render_markdown(content_3),
        "category": "politique",
        "tags": ["epstein", "emails", "documents", "declassification", "victimes"],
        "sources": [
            {"title": "PACER - US Court Records", "url": "https://www.pacer.gov/", "type": "officiel"},
            {"title": "Unsealed Epstein documents 2024", "url": "https://storage.courtlistener.com/recap/gov.uscourts.nysd.447706/", "type": "document"},
        ],
        "related_articles": [],
        "author_uid": current_user.uid,
        "author_username": author_username,
        "generated_by_ai": False,
        "ai_model": "",
        "status": "published",
        "credibility": "documente",
        "classification": "secret",
        "views": random.randint(50, 5000),
        "upvotes": random.randint(5, 500),
        "downvotes": random.randint(0, 50),
        "comment_count": 0,
        "created_at": timestamps[2],
        "updated_at": timestamps[2],
        "featured": True,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Handwritten_document.jpg/480px-Handwritten_document.jpg",
    }

    # =========================================================================
    # ARTICLE 4 : La Franc-Maconnerie - Les Architectes de l'Ombre
    # =========================================================================
    content_4 = """### Introduction

La **franc-maconnerie** est sans doute la **societe secrete la plus ancienne et la plus influente** encore en activite aujourd'hui. Avec une histoire remontant aux **guildes de batisseurs de cathedrales** du Moyen Age, elle a evolue en un reseau mondial de loges et d'obediences dont l'influence sur la politique, la culture et la finance est alternativement niee, minimisee ou exageree.

### Des Batisseurs de Cathedrales aux Loges Modernes

Les origines de la franc-maconnerie sont enveloppees de mystere. La version historique consensuelle la fait remonter aux **guildes de macons operatifs** du Moyen Age, ces artisans specialises dans la construction des cathedrales gothiques. Ces guildes possedaient des **secrets de metier** (techniques de taille de pierre, calculs architecturaux) qu'elles transmettaient par des rituels d'initiation.

La transition vers la maconnerie **speculative** (philosophique et non plus operationnelle) s'est faite progressivement aux XVIIe et XVIIIe siecles. La fondation de la **Grande Loge de Londres** en **1717** est generalement consideree comme l'acte de naissance de la franc-maconnerie moderne. La **Constitution d'Anderson** de 1723 a codifie les principes fondamentaux : tolerance, fraternite, progres moral et recherche de la verite.

### La Hierarchie et les Degres

La franc-maconnerie est organisee en **degres d'initiation** :

**Les 3 degres fondamentaux (Rite Bleu) :**
- **Apprenti** : le neophyte, qui apprend les rudiments du symbolisme
- **Compagnon** : l'initie qui approfondit sa quete
- **Maitre** : le grade culminant, associe a la legende d'**Hiram Abiff**, l'architecte du Temple de Salomon

**Les hauts grades :**
- Le **Rite Ecossais Ancien et Accepte** comporte **33 degres**, dont le 33e est un grade honorifique reserve a une elite
- Le **Rite de York** propose une voie alternative avec ses propres degres
- Chaque degre est associe a des **rituels specifiques**, des mots de passe et des signes de reconnaissance

### Membres Celebres

La liste des francs-macons celebres est vertigineuse :

- **Voltaire** : initie a la loge *Les Neuf Soeurs* a Paris en 1778, peu avant sa mort
- **George Washington** : premier president des Etats-Unis, maitre de sa loge en Virginie
- **Benjamin Franklin** : Grand Maitre de la loge de Pennsylvanie et membre des *Neuf Soeurs* a Paris
- **Wolfgang Amadeus Mozart** : membre de la loge *Zur Wohlthatigkeit* a Vienne, *La Flute enchantee* est remplie de symbolisme maconnique
- **Napoleon Bonaparte** : bien que son statut de franc-macon soit debattu, ses freres Joseph et Jerome l'etaient certainement
- **Winston Churchill** : initie en 1901 a la loge *Studholme Alliance*

### Les Symboles

Le **symbolisme maconnique** est omnipresent et souvent mal interprete :

- **L'equerre et le compas** : les outils du macon, representant la **matiere et l'esprit**, la rectitude morale et les limites que l'on s'impose
- **L'Oeil de la Providence** (Oeil qui voit tout) : symbole de la conscience divine, present sur le billet d'un dollar americain
- **La pyramide tronquee** : symbolisant le travail inacheve de l'humanite vers la perfection
- **Le pavage mosaique** (damier noir et blanc) : la dualite du monde, bien et mal, lumiere et tenebres
- **La lettre G** : diversement interpretee comme God (Dieu), Geometrie ou Gnose

### Le Grand Orient de France et la Politique

En France, le **Grand Orient de France** (GODF), fonde en 1773, est la plus grande obedience maconnique. Contrairement a la maconnerie anglo-saxonne, le GODF est **adogmatique** : il n'exige pas la croyance en un Etre Supreme.

Son influence sur la politique francaise est **documentee et considerable** :
- La loi de **separation de l'Eglise et de l'Etat** (1905) a ete largement preparee dans les loges
- L'**affaire des fiches** (1904) a revele que le GODF surveillait les opinions religieuses des officiers de l'armee
- De nombreux presidents de la Republique etaient francs-macons, ainsi que des dizaines de ministres et parlementaires
- La **laicite** a la francaise est en grande partie une creation maconnique

### Le Scandale de la Loge P2

En Italie, la **Propaganda Due** (P2), dirigee par **Licio Gelli**, a ete au coeur de l'un des plus grands scandales de l'apres-guerre. Decouverte en 1981, cette loge clandestine comptait parmi ses membres des **ministres, generaux, chefs des services secrets, banquiers** (dont Roberto Calvi, retrouve pendu sous le pont de Blackfriars a Londres) et meme **Silvio Berlusconi**. La P2 etait impliquee dans des tentatives de **coup d'Etat** et des liens avec la **mafia** et l'**Operation Gladio** de l'OTAN.

### Theories et Realite

Les theories du complot attribuent aux francs-macons un **controle mondial** coordonne. La realite est plus nuancee : la franc-maconnerie est un **reseau d'influence** puissant mais fragmentee, divise en obediences souvent rivales. Son influence est reelle dans certains secteurs (justice, politique, affaires), mais l'idee d'un **gouvernement maconnique mondial unifie** releve davantage du mythe que de la realite documentee.

### Conclusion

La franc-maconnerie reste une institution fascinante a la frontiere entre le **secret et le pouvoir**, la **philosophie et la politique**. Son influence historique est indeniable, son fonctionnement actuel plus prosaic que ne le suggerent les theories du complot. Mais tant qu'elle conservera ses rituels et son gout du secret, elle continuera d'alimenter les fantasmes les plus elabores."""

    slug_4 = slugify("La Franc-Maconnerie - Les Architectes de l'Ombre")
    article_4 = {
        "title": "La Franc-Maconnerie - Les Architectes de l'Ombre",
        "title_lower": "la franc-maconnerie - les architectes de l'ombre",
        "slug": slug_4,
        "summary": truncate_text("Histoire de la franc-maconnerie, des guildes medievales aux loges modernes : hierarchie, symboles, membres celebres, influence politique et scandales.", 200),
        "content": content_4,
        "content_html": render_markdown(content_4),
        "category": "occultisme",
        "tags": ["franc-maconnerie", "illuminati", "loge", "grand-orient", "symboles"],
        "sources": [
            {"title": "Grand Orient de France - Site officiel", "url": "https://www.godf.org/", "type": "officiel"},
            {"title": "Constitution d'Anderson (1723)", "url": "https://freemasonry.bcy.ca/texts/anderson1723.html", "type": "archive"},
        ],
        "related_articles": [],
        "author_uid": current_user.uid,
        "author_username": author_username,
        "generated_by_ai": False,
        "ai_model": "",
        "status": "published",
        "credibility": "documente",
        "classification": "confidentiel",
        "views": random.randint(50, 5000),
        "upvotes": random.randint(5, 500),
        "downvotes": random.randint(0, 50),
        "comment_count": 0,
        "created_at": timestamps[3],
        "updated_at": timestamps[3],
        "featured": True,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Masonic_SquareCompassesG.svg/480px-Masonic_SquareCompassesG.svg.png",
    }

    # =========================================================================
    # ARTICLE 5 : Les Illuminati de Baviere - Du Mythe a la Realite
    # =========================================================================
    content_5 = """### Introduction

Aucun nom n'evoque autant le **complot mondial** que celui des *Illuminati*. De Jay-Z formant un triangle avec ses mains a l'oeil sur le billet d'un dollar, les references aux Illuminati sont omnipresntes dans la culture populaire. Mais qui etaient reellement les Illuminati, et comment un ordre secret bavarois du XVIIIe siecle est-il devenu le symbole ultime de la **conspiration mondiale** ?

### Adam Weishaupt et la Fondation de l'Ordre

Le **1er mai 1776** (date qui alimente a elle seule d'innombrables theories), le professeur de droit canonique **Adam Weishaupt** fonde l'**Ordre des Illumines de Baviere** (*Illuminatenorden*) a l'universite d'Ingolstadt. Weishaupt, decu par l'obscurantisme religieux des Jesuites qui dominaient l'education bavaroise, cree un ordre voue a des ideaux **rationalistes et progressistes** :

- Opposition a la **superstition** et au dogmatisme religieux
- Lutte contre l'**abus de pouvoir** de l'Etat et de l'Eglise
- Promotion de l'**education** et de la raison
- Egalite entre les classes sociales

L'ordre comptait au sommet de son influence environ **2 000 membres** dans toute l'Europe, dont des aristocrates, des intellectuels et des fonctionnaires. Le baron **Adolph von Knigge** fut l'un de ses recruteurs les plus efficaces.

### Infiltration des Loges Maconniques

La strategie des Illuminati fut d'**infiltrer les loges franc-maconnes** existantes pour diffuser leurs idees. Cette tactique fonctionna remarquablement bien, au point que de nombreux macons ignoraient qu'ils avaient ete recrutes par les Illuminati. Cette fusion explique en partie pourquoi les deux organisations sont si souvent confondues dans les theories du complot contemporaines.

### L'Interdiction de 1785 et la Dispersion

En 1784-1785, le duc-electeur de Baviere **Charles Theodore** interdit toutes les societes secretes, dont les Illuminati. Des documents internes sont saisis et publies, revelant les rituels et les objectifs de l'ordre. Weishaupt fuit en exil. Officiellement, l'ordre des Illuminati **cesse d'exister**.

Mais pour les theoriciens du complot, cette dissolution n'etait qu'une **facade**. L'ordre aurait simplement plonge dans une clandestinite plus profonde, continuant son action a travers d'autres organisations.

### L'Oeil de la Providence et le Dollar Americain

L'element le plus cite comme *"preuve"* de l'existence actuelle des Illuminati est l'**Oeil de la Providence** surmontant une pyramide tronquee au verso du billet d'un dollar americain. Ce symbole, integre au **Grand Sceau des Etats-Unis** en 1782, est accompagne de la devise latine **"Novus Ordo Seclorum"** (*Nouvel Ordre des Siecles*), que les conspirationnistes traduisent par *"Nouvel Ordre Mondial"*.

Les historiens notent que :
- L'Oeil de la Providence est un **symbole chretien** ancien, representant Dieu veillant sur l'humanite
- La pyramide symbolise la **force et la duree**
- Les 13 etages representent les **13 colonies originelles**
- La devise est tiree des *Bucoliques* de **Virgile** et fait reference a un nouvel age, pas a un gouvernement mondial
- Le symbole a ete adopte **avant** que les Illuminati ne soient connus aux Etats-Unis

### Les Theories Modernes

Au XXe et XXIe siecles, les Illuminati sont devenus un **concept fourre-tout** englobant toute forme de conspiration elitiste :

**L'industrie musicale :** Des artistes comme **Jay-Z**, **Beyonce**, **Rihanna** et **Lady Gaga** sont regulierement accuses d'etre des *"pantins des Illuminati"* en raison de leur utilisation de symboles (triangles, oeil unique, pyramides) dans leurs clips et performances. Le signe du triangle forme par les mains (le *"Roc Sign"* de Jay-Z, en realite le logo de son label Roc-A-Fella Records) est devenu **le** geste illuminati par excellence.

**Les rituels de celebritees :** Les ceremonies des Grammy Awards, du Super Bowl ou des Jeux Olympiques sont decortiquees image par image a la recherche de **symbolisme occulte** cache. Certains y voient des **rituels sataniques** deguises en divertissement de masse.

**Le Bohemian Grove :** Ce club prive californien ou se reunissent chaque ete les hommes les plus puissants d'Amerique (presidents, PDG, banquiers) pour un rituel nocturne appele la **"Cremation of Care"** devant une statue de hibou geant est souvent lie aux Illuminati.

### Faits et Fantasmes

La frontiere entre realite historique et fantasme est ici particulierement floue :

**Ce qui est historiquement vrai :**
- Les Illuminati de Baviere ont existe de 1776 a 1785
- Ils ont reellement cherche a influencer la politique par l'infiltration
- Leurs objectifs etaient progressistes et anticléricaux

**Ce qui est speculatif :**
- Leur survie apres 1785
- Leur role dans la Revolution francaise
- L'existence d'un ordre illuminati contemporain

**Ce qui releve du mythe :**
- Le controle de l'industrie musicale
- Les rituels sataniques televises
- Un gouvernement mondial secret

### Conclusion

Les Illuminati de Baviere furent un **phenomene historique reel mais ephemere**. Leur transformation en mythe conspirrationniste mondial temoigne de notre besoin profond de donner un **visage et un nom** aux forces qui semblent gouverner le monde dans l'ombre. Que l'on y croie ou non, le simple fait que le mot *"Illuminati"* provoque encore autant de fascination, **240 ans** apres leur dissolution, est en soi un phenomene remarquable."""

    slug_5 = slugify("Les Illuminati de Baviere - Du Mythe a la Realite")
    article_5 = {
        "title": "Les Illuminati de Baviere - Du Mythe a la Realite",
        "title_lower": "les illuminati de baviere - du mythe a la realite",
        "slug": slug_5,
        "summary": truncate_text("Des Illumines de Baviere d'Adam Weishaupt en 1776 au mythe mondial : l'Oeil de la Providence, le dollar, l'industrie musicale et le Bohemian Grove.", 200),
        "content": content_5,
        "content_html": render_markdown(content_5),
        "category": "occultisme",
        "tags": ["illuminati", "baviere", "weishaupt", "nouvel-ordre-mondial", "oeil"],
        "sources": [
            {"title": "Adam Weishaupt et les Illumines de Baviere", "url": "https://www.britannica.com/topic/Illuminati", "type": "archive"},
            {"title": "Novus Ordo Seclorum - Billet d'un dollar", "url": "https://www.treasury.gov/", "type": "officiel"},
        ],
        "related_articles": [],
        "author_uid": current_user.uid,
        "author_username": author_username,
        "generated_by_ai": False,
        "ai_model": "",
        "status": "published",
        "credibility": "speculatif",
        "classification": "secret",
        "views": random.randint(50, 5000),
        "upvotes": random.randint(5, 500),
        "downvotes": random.randint(0, 50),
        "comment_count": 0,
        "created_at": timestamps[4],
        "updated_at": timestamps[4],
        "featured": True,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Eye_of_Providence.svg/480px-Eye_of_Providence.svg.png",
    }

    # =========================================================================
    # ARTICLE 6 : La Dynastie Rothschild - L'Empire Financier Invisible
    # =========================================================================
    content_6 = """### Introduction

Le nom **Rothschild** est synonyme de **richesse et de pouvoir** depuis plus de deux siecles. Cette dynastie bancaire, fondee dans le ghetto juif de Francfort au XVIIIe siecle, a bati un empire financier qui a **finance des guerres, cree des nations et influence le cours de l'histoire**. Pour les theoriciens du complot, les Rothschild incarnent l'archetype de l'**elite financiere invisible** qui tire les ficelles du monde.

### Mayer Amschel Rothschild et les Cinq Fils

L'histoire commence avec **Mayer Amschel Rothschild** (1744-1812), cambiste et marchand de pieces dans la *Judengasse* (ruelle des Juifs) de Francfort. Son genie fut de placer ses **cinq fils** dans les cinq plus grandes capitales financieres d'Europe, creant le premier **reseau bancaire international** de l'histoire :

- **Amschel Mayer** a **Francfort**
- **Salomon** a **Vienne**
- **Nathan Mayer** a **Londres** (la branche la plus puissante)
- **Carl** a **Naples**
- **James** a **Paris**

Ce reseau familial permettait des transferts de fonds et d'informations a une vitesse **inegalee pour l'epoque**, grace a un systeme de **courriers prives** et de messages codes. Cette avance informationnelle etait leur arme secrete.

### La Legende de Waterloo

L'episode le plus celebre et le plus conteste de l'histoire Rothschild concerne la **bataille de Waterloo** en 1815. Selon la legende, **Nathan Mayer Rothschild** a Londres aurait appris la defaite de Napoleon **un jour avant** le gouvernement britannique grace a son reseau de courriers. Il aurait alors **vendu massivement** ses titres a la Bourse de Londres, provoquant une panique. Les autres investisseurs, croyant que Napoleon avait gagne, auraient vendu dans la panique. Les agents de Rothschild auraient alors **rachete a prix derisoire** avant que la nouvelle de la victoire ne fasse remonter les cours, realisant un **profit colossal**.

Les historiens debattent de la veracite de cet episode. **Niall Ferguson**, biographe autorise des Rothschild, confirme que Nathan avait effectivement recu la nouvelle en avance, mais conteste l'ampleur de la speculation. D'autres sources suggerent que l'histoire a ete **largement embellie** au fil du temps.

### Le Financement des Guerres

L'une des accusations les plus recurrentes contre les Rothschild est d'avoir **finance les deux camps** dans de nombreux conflits :

- **Guerres napoleoniennes** : prets aux gouvernements britannique et autrichien tout en maintenant des relations commerciales avec la France
- **Guerre de Crimee** (1853-1856) : financement de la Grande-Bretagne et de la France
- **Guerre franco-prussienne** (1870-1871) : la branche parisienne et la branche francfortoise dans des camps opposes
- **Premiere Guerre mondiale** : des branches de la famille dans chaque camp belligerant

Cette strategie, si elle est averee dans toute son ampleur, representerait le cynisme financier ultime : **profiter de la destruction** quelle que soit l'issue du conflit.

### Les Banques Centrales et la Reserve Federale

Pour les conspirationnistes, le pouvoir supreme des Rothschild reside dans leur **controle suppose des banques centrales**. La citation attribuee (probablement apocryphe) a Mayer Amschel Rothschild resume cette theorie : *"Donnez-moi le controle de la monnaie d'une nation, et je me moque de qui fait ses lois."*

La creation de la **Reserve Federale americaine** en **1913** est un point focal de ces theories. La reunion secrete de **Jekyll Island** (novembre 1910), ou six banquiers et un senateur ont redige le projet de la Fed, incluait **Paul Warburg**, associe de la banque Kuhn, Loeb & Co., liee aux Rothschild par des mariages et des affaires. Pour les theoriciens, cela prouve que la Fed est une **creation Rothschild** deguisee en institution publique.

### Emmanuel Macron et la Connexion Francaise

En France, le lien entre **Emmanuel Macron** et la banque **Rothschild & Co** est un fait public : le futur president y a travaille comme **banquier d'affaires** de 2008 a 2012, pilotant notamment le rachat de **Pfizer Nutrition** par **Nestle** pour 9 milliards d'euros. Cette connexion alimente en permanence les theories sur l'influence des Rothschild sur la politique francaise.

Les defenseurs de Macron soulignent qu'il etait un employe parmi d'autres ; ses critiques y voient la preuve qu'il a ete **"fabrique"** par la finance pour acceder au pouvoir.

### Le Blason et la Devise

Le blason des Rothschild porte **cinq fleches** tenues dans un poing, representant les cinq fils et leur union. La devise familiale, *"Concordia, Integritas, Industria"* (Concorde, Integrite, Industrie), est vue par les conspirationnistes comme un **code** dissimulant leur veritable ambition : le controle financier mondial.

### Fortune et Patrimoine

Estimer la fortune des Rothschild est extremement difficile. Les estimations vont de quelques milliards a **plusieurs centaines de milliards** de dollars, repartis entre des dizaines de branches familiales, des fondations, des holdings et des trusts opaques. La famille possede des **vignobles** (Chateau Lafite, Chateau Mouton), des **collections d'art** parmi les plus importantes au monde, et des proprietes immobilieres dans les capitales europeennes.

### Conclusion

La dynastie Rothschild est un cas fascinant ou la **realite historique** nourrit les theories les plus extravagantes. Leur influence sur la finance europeenne des XIXe et XXe siecles est **incontestable et documentee**. Mais l'image d'une famille omnipotente controlant secretement l'economie mondiale depuis 250 ans releve davantage du **mythe** que de la realite contemporaine, ou leur empire, bien que toujours considerable, fait face a des concurrents bien plus puissants comme **BlackRock, Vanguard** ou les fonds souverains du Golfe."""

    slug_6 = slugify("La Dynastie Rothschild - L'Empire Financier Invisible")
    article_6 = {
        "title": "La Dynastie Rothschild - L'Empire Financier Invisible",
        "title_lower": "la dynastie rothschild - l'empire financier invisible",
        "slug": slug_6,
        "summary": truncate_text("La dynastie Rothschild : des cinq fils dans cinq capitales au controle suppose des banques centrales, en passant par Waterloo et Emmanuel Macron.", 200),
        "content": content_6,
        "content_html": render_markdown(content_6),
        "category": "finance",
        "tags": ["rothschild", "banque", "finance", "elite", "nouvel-ordre-mondial"],
        "sources": [
            {"title": "The House of Rothschild - Niall Ferguson", "url": "https://www.penguinrandomhouse.com/", "type": "media"},
            {"title": "Banque Rothschild & Co", "url": "https://www.rothschildandco.com/", "type": "officiel"},
        ],
        "related_articles": [],
        "author_uid": current_user.uid,
        "author_username": author_username,
        "generated_by_ai": False,
        "ai_model": "",
        "status": "published",
        "credibility": "speculatif",
        "classification": "confidentiel",
        "views": random.randint(50, 5000),
        "upvotes": random.randint(5, 500),
        "downvotes": random.randint(0, 50),
        "comment_count": 0,
        "created_at": timestamps[5],
        "updated_at": timestamps[5],
        "featured": True,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Coat_of_Arms_of_the_Rothschild_family.svg/480px-Coat_of_Arms_of_the_Rothschild_family.svg.png",
    }

    # =========================================================================
    # ARTICLE 7 : Symbolisme Occulte et Rituels dans l'Elite Mondiale
    # =========================================================================
    content_7 = """### Introduction

Derriere les portes closes des clubs les plus exclusifs du monde, les elites politiques et financieres participeraient a des **rituels occultes** herites de traditions ancestrales. Du **Bohemian Grove** californien aux revelations du *"Spirit Cooking"*, un faisceau d'indices troublants suggere que le pouvoir mondial s'accompagne de pratiques bien eloignees de la rationalite affichee en public.

### Le Bohemian Grove

Le **Bohemian Grove** est un domaine de **1 100 hectares** de sequoias geants situe a Monte Rio, en Californie. Depuis **1878**, le **Bohemian Club** de San Francisco y organise chaque ete, en juillet, un rassemblement de deux semaines reunissant environ **2 700 hommes** parmi les plus puissants de la planete.

**Parmi les membres et invites documentes :**
- Les presidents **Richard Nixon**, **Ronald Reagan**, **George H.W. Bush** et **George W. Bush**
- **Henry Kissinger**, secretaire d'Etat et figure omnipresente des cercles de pouvoir
- **Colin Powell**, **Dick Cheney**, **Donald Rumsfeld**
- Des PDG de Goldman Sachs, Bank of America, Bechtel, et d'innombrables entreprises du Fortune 500

Le point culminant du rassemblement est la ceremonie nocturne de la **"Cremation of Care"** (*Cremation du Souci*), ou les participants se reunissent au pied d'une **statue de hibou de 12 metres** pour bruler en effigie une figure humaine symbolisant les *soucis du monde*. La ceremonie, accompagnee de torches, de robes et d'incantations, a ete filmee clandestinement en **2000 par Alex Jones**, qui s'est infiltre dans le domaine.

Nixon, dans un enregistrement du Watergate, a qualifie le Bohemian Grove de *"la chose la plus mauditement faggoty que vous puissiez imaginer"*, suggerant que des pratiques sexuelles y avaient lieu. Les organisateurs insistent sur le caractere **theatral et humoristique** de l'evenement.

### La Statue du Hibou : Moloch ou Minerve ?

La statue de hibou geant est au coeur d'un debat : pour les conspirationnistes, elle represente **Moloch**, divinite canaanenne a qui l'on sacrifiait des enfants. Pour le Bohemian Club, il s'agit de **Minerve** (Athena), deesse de la sagesse, dont le hibou est l'attribut traditionnel. La cremation d'une effigie humaine devant cette statue evoque neanmoins des **paralleles troublants** avec les cultes antiques.

### Marina Abramovic et le Spirit Cooking

En **2016**, les emails de **John Podesta** (directeur de campagne de Hillary Clinton), publies par **WikiLeaks**, ont revele une invitation de l'artiste serbe **Marina Abramovic** a un diner de *"Spirit Cooking"*. Cette pratique artistique, inspiree de rituels de **Thelema** d'Aleister Crowley, implique l'utilisation de sang, de lait maternel et d'autres fluides corporels dans un contexte rituel.

Les images des *"Spirit Cooking dinners"* montrant des messages ecrits avec du sang sur les murs (*"Mix fresh breast milk with fresh sperm"*) ont provoque un **scandale mondial**. Abramovic a insiste sur la dimension purement **artistique et performative** de ces evenements, mais l'association avec des personnalites politiques de premier plan a alimente les theories les plus sombres sur des **rituels sataniques** au sein de l'elite.

### Skull and Bones

La societe secrete **Skull and Bones** (*Tete de mort et os croises*), fondee en **1832** a l'universite de **Yale**, est l'une des plus influentes des Etats-Unis. Chaque annee, seulement **15 nouveaux membres** sont recrutes parmi les etudiants de derniere annee.

**Membres celebres :**
- **George H.W. Bush** (promotion 1948) et **George W. Bush** (promotion 1968) : pere et fils, tous deux presents, tous deux devenus presidents des Etats-Unis
- **John Kerry** : candidat democrate a la presidentielle en 2004 face a Bush Jr., lui aussi Bonesman
- **William Howard Taft** : 27e president des Etats-Unis

Le fait que l'election presidentielle de 2004 ait oppose **deux membres de Skull and Bones** a souleve des questions legitimes sur le caractere reel de la *"democratie"* americaine. Les rituels d'initiation incluraient selon d'anciens membres des confessions intimes, des simulacres de cercueil et la veneration de reliques, dont le **crane suppose de Geronimo**, vole par Prescott Bush en 1918.

### Le Culte de Saturne

Une theorie plus esoterique relie les symboles de pouvoir a un ancien **culte de Saturne**. Selon ses proponents :

- Le **cube noir** (symbole saturnien) apparait dans de multiples contextes : la **Kaaba** a La Mecque, les **tefillin** juifs, le cube noir de l'**Apple Store**, le logo de **BlackRock**
- Les **anneaux de Saturne** seraient l'origine de la tradition des **alliances de mariage**
- Le **samedi** (*Saturday* en anglais, *Saturn's Day*) serait un jour de veneration cachee
- Le **hexagone** au pole nord de Saturne, decouvert par Voyager, serait la source de l'**etoile de David** (un hexagone inscrit)

Les sceptiques font remarquer que ces associations sont des exemples classiques d'**apophenie** : la tendance a percevoir des connexions significatives dans des elements non lies.

### Symboles dans les Logos d'Entreprise

Les chasseurs de symboles occultes trouvent des references dans d'innombrables logos corporatifs :

- **Procter & Gamble** : l'ancien logo montrait un visage dans un croissant de lune, accuse de contenir le chiffre 666 (le logo a ete change en 1985)
- **Monster Energy** : les trois griffures du logo formeraient le chiffre **666** en hebreu (la lettre *Vav*)
- **Starbucks** : la sirene serait un symbole occulte de **Melusine** ou d'**Ishtar**
- **Vodafone** : le logo contiendrait un **6** cache dans le crochet de dialogue

### Conclusion

Le symbolisme occulte dans les spheres de pouvoir est un sujet ou se melangent **faits documentes** (Bohemian Grove existe reellement, Skull and Bones aussi), **interpretations discutables** (la signification des rituels) et **fantasmes purs** (le culte saturnien mondial). La frontiere entre art, tradition, rituel social et veritable pratique occulte reste **deliberement floue**, et c'est peut-etre la le veritable pouvoir de ces symboles : maintenir le **mystere et la fascination** qui entourent ceux qui gouvernent le monde."""

    slug_7 = slugify("Symbolisme Occulte et Rituels dans l'Elite Mondiale")
    article_7 = {
        "title": "Symbolisme Occulte et Rituels dans l'Elite Mondiale",
        "title_lower": "symbolisme occulte et rituels dans l'elite mondiale",
        "slug": slug_7,
        "summary": truncate_text("Du Bohemian Grove a Skull and Bones, du Spirit Cooking au culte de Saturne : exploration des rituels occultes au sein des elites mondiales.", 200),
        "content": content_7,
        "content_html": render_markdown(content_7),
        "category": "occultisme",
        "tags": ["occultisme", "rituels", "bohemian-grove", "satanisme", "elite"],
        "sources": [
            {"title": "Bohemian Grove - Alex Jones infiltration 2000", "url": "https://www.bohemiangrove.org/", "type": "archive"},
            {"title": "Cremation of Care ceremony", "url": "https://en.wikipedia.org/wiki/Bohemian_Grove", "type": "media"},
        ],
        "related_articles": [],
        "author_uid": current_user.uid,
        "author_username": author_username,
        "generated_by_ai": False,
        "ai_model": "",
        "status": "published",
        "credibility": "speculatif",
        "classification": "secret",
        "views": random.randint(50, 5000),
        "upvotes": random.randint(5, 500),
        "downvotes": random.randint(0, 50),
        "comment_count": 0,
        "created_at": timestamps[6],
        "updated_at": timestamps[6],
        "featured": False,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Baphomet.png/440px-Baphomet.png",
    }

    # =========================================================================
    # ARTICLE 8 : MK-Ultra - Le Programme de Controle Mental de la CIA
    # =========================================================================
    content_8 = """### Introduction

**MK-Ultra** est le nom de code d'un programme **reel et documente** de la CIA consacre au **controle mental**. Mene de **1953 a 1973**, il constitue l'un des chapitres les plus sombres de l'histoire du renseignement americain. Contrairement a la plupart des theories du complot, MK-Ultra n'est pas une speculation : il a ete **reconnu officiellement** par la CIA, documente par le Congres americain et a fait l'objet de poursuites judiciaires.

### Origines et Contexte

Au debut de la Guerre froide, la CIA etait obsedee par la possibilite que l'URSS et la Chine aient developpe des techniques de **lavage de cerveau** (*brainwashing*). Les *"confessions"* de prisonniers americains pendant la **guerre de Coree**, ou des soldats reconnaissaient publiquement des crimes de guerre, ont convaincu les services de renseignement qu'un programme de recherche sur le controle mental etait indispensable.

Le **13 avril 1953**, le directeur de la CIA **Allen Dulles** autorise officiellement le projet MK-Ultra. Le programme est place sous la direction du **Dr. Sidney Gottlieb**, chimiste de la Division des Services Techniques (TSD), un personnage que ses collegues surnommaient *"le Sorcier Noir"*.

### Les Experiences au LSD

Le volet le plus connu de MK-Ultra concerne les experiences avec le **LSD** (acide lysergique diethylamide), alors une substance nouvelle et mal connue. La CIA en a achete la quasi-totalite de la production mondiale aupres de **Sandoz Laboratories** en Suisse.

Les experiences allaient du **consentement eclaire** (rare) a l'**administration a l'insu des sujets** (frequent) :

- Des **employes de la CIA** se dosaient mutuellement au LSD sans prevenir, dans le cadre de reunions de travail
- Des **soldats** de l'armee americaine a **Fort Detrick** recevaient du LSD sans leur consentement
- Des **prisonniers**, des **patients psychiatriques** et des **prostituees** etaient utilises comme cobayes
- Des **etudiants d'universite** participaient a des experiences presentees comme de la recherche psychologique benigne (c'est le cas de **Ted Kaczynski**, le futur *Unabomber*, soumis a des experiences psychologiques traumatisantes a Harvard entre 1959 et 1962 dans le cadre d'un sous-projet MK-Ultra dirige par le **Dr. Henry Murray**)

### Operation Midnight Climax

L'un des sous-projets les plus scandaleux etait l'**Operation Midnight Climax**. La CIA a ouvert des **maisons closes** a San Francisco et New York, ou des prostituees recrutees par l'agence administraient du **LSD a des clients a leur insu**. Des agents de la CIA observaient les effets depuis derriere des **miroirs sans tain**, filmant les scenes. L'objectif etait d'etudier les effets du LSD dans un contexte d'**exploitation sexuelle** et d'evaluer son potentiel comme serum de verite.

Le superviseur de l'operation, **George Hunter White**, agent du Bureau Federal des Narcotiques, ecrira plus tard : *"Ou d'autre un petit garcon americain aurait-il pu faire des choses pareilles avec l'approbation du gouvernement ?"*

### La Mort de Frank Olson

Le **28 novembre 1953**, **Frank Olson**, biochimiste militaire travaillant a **Fort Detrick** sur des armes biologiques, fait une chute mortelle du 13e etage de l'hotel Statler a New York. La CIA affirma qu'il s'etait suicide apres avoir recu du LSD a son insu lors d'une retraite de travail 9 jours plus tot.

En 1994, l'exhumation de son corps revela une **blessure cranienne** anterieure a la chute, incompatible avec un suicide. Son fils **Eric Olson** a consacre sa vie a prouver que son pere avait ete **assassine** parce qu'il souhaitait reveler les programmes d'armes biologiques de la CIA. En 2012, un juge federal a rejete la plainte de la famille, mais les circonstances restent profondement suspectes.

### Le Sous-Projet 68 : Dr. Donald Ewen Cameron

A l'**universite McGill** de Montreal (Canada), le **Dr. Donald Ewen Cameron** mena certaines des experiences les plus destructrices de MK-Ultra dans le cadre du **sous-projet 68**. Finance par la CIA via une fondation-ecran, Cameron soumettait ses patients a :

- Des sessions de **sommeil force** (jusqu'a 30 jours consecutifs sous sedatifs)
- Des **electrochocs massifs** (30 a 40 fois l'intensite therapeutique normale)
- L'ecoute en boucle de **messages enregistres** pendant des semaines (procede qu'il appelait *"psychic driving"*)
- L'administration de **cocktails de drogues** (LSD, PCP, barbituriques)

L'objectif etait de *"deprogrammer"* la personnalite du patient pour la *"reprogrammer"*. Les resultats furent catastrophiques : des patients autrefois fonctionnels ont ete reduits a un etat de **dependance infantile**, incapables de se souvenir de leur propre nom. Le gouvernement canadien a fini par indemniser les victimes dans les annees 1990.

### Le Concept du Candidat Mandchou

MK-Ultra visait ultimement a creer un **"Candidat Mandchou"** (du roman de Richard Condon, 1959) : un **assassin programme**, capable de tuer sur commande et d'oublier ensuite ses actes. Bien que la CIA n'ait jamais confirme avoir reussi, la possibilite que certains sous-projets aient atteint un niveau de sophistication inconnu reste une question ouverte.

### La Destruction des Preuves

En **1973**, le directeur de la CIA **Richard Helms**, sur le point de quitter ses fonctions, ordonna la **destruction de tous les dossiers MK-Ultra**. La majorite des documents furent detruits. Ce n'est qu'en **1977** qu'un archiviste decouvrit **20 000 documents financiers** ayant echappe a la destruction, dans un batiment different de celui des archives operationnelles.

Ces documents, bien que principalement financiers, ont permis de reconstituer partiellement l'ampleur du programme : **149 sous-projets**, impliquant **80 institutions**, dont des universites, des hopitaux, des prisons et des entreprises pharmaceutiques.

### Conclusion

MK-Ultra est la preuve documentee que les gouvernements sont **capables de mener des programmes secrets** d'une cruaute extreme contre leurs propres citoyens. La destruction deliberee des archives en 1973 souleve une question troublante : si ce qui a survecu est deja aussi horrifiant, **qu'y avait-il dans les documents detruits ?** Cette affaire constitue un rappel permanent que la frontiere entre *theorie du complot* et *realite documentee* peut etre beaucoup plus mince qu'on ne le pense."""

    slug_8 = slugify("MK-Ultra - Le Programme de Controle Mental de la CIA")
    article_8 = {
        "title": "MK-Ultra - Le Programme de Controle Mental de la CIA",
        "title_lower": "mk-ultra - le programme de controle mental de la cia",
        "slug": slug_8,
        "summary": truncate_text("Le programme MK-Ultra de la CIA (1953-1973) : experiences au LSD, Operation Midnight Climax, mort de Frank Olson, Dr. Cameron a McGill et destruction des archives.", 200),
        "content": content_8,
        "content_html": render_markdown(content_8),
        "category": "technologie",
        "tags": ["mk-ultra", "cia", "controle-mental", "lsd", "manchurian-candidate"],
        "sources": [
            {"title": "CIA FOIA - MK-Ultra documents", "url": "https://www.cia.gov/readingroom/collection/mkultra", "type": "officiel"},
            {"title": "Commission Church 1975", "url": "https://www.senate.gov/about/powers-procedures/investigations/church-committee.htm", "type": "officiel"},
        ],
        "related_articles": [],
        "author_uid": current_user.uid,
        "author_username": author_username,
        "generated_by_ai": False,
        "ai_model": "",
        "status": "published",
        "credibility": "documente",
        "classification": "top-secret",
        "views": random.randint(50, 5000),
        "upvotes": random.randint(5, 500),
        "downvotes": random.randint(0, 50),
        "comment_count": 0,
        "created_at": timestamps[7],
        "updated_at": timestamps[7],
        "featured": False,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/99/Mkultra-lsd-doc.jpg",
    }

    # =========================================================================
    # ARTICLE 9 : Le Groupe Bilderberg - Le Gouvernement de l'Ombre
    # =========================================================================
    content_9 = """### Introduction

Chaque annee, environ **130 des personnalites les plus influentes** de la planete se reunissent a huis clos pendant trois jours dans un hotel de luxe haute securite. Pas de cameras, pas de comptes rendus officiels, pas de communiques de presse detailles. Ce rassemblement, connu sous le nom de **Conference Bilderberg**, est pour beaucoup la preuve ultime de l'existence d'un **gouvernement mondial de l'ombre**.

### La Fondation en 1954

La premiere conference Bilderberg s'est tenue du **29 au 31 mai 1954** a l'**Hotel de Bilderberg** a Oosterbeek, aux Pays-Bas, d'ou le nom du groupe. Les fondateurs etaient :

- **Le prince Bernhard des Pays-Bas** (ancien membre du parti nazi avant la guerre, detail rarement mentionne dans les publications officielles)
- **David Rockefeller** : banquier americain, PDG de Chase Manhattan Bank
- **Joseph Retinger** : diplomate polonais et architecte de l'integration europeenne

L'objectif declare etait de **favoriser le dialogue** entre l'Europe et l'Amerique du Nord a une epoque ou les relations transatlantiques etaient tendues. La Guerre froide battait son plein, et les elites occidentales estimaient necessaire de **coordonner leurs positions** face a la menace sovietique.

### Le Fonctionnement

Les reunions Bilderberg suivent un protocole strict :

- **Environ 130 participants** : chefs d'Etat, ministres, PDG, banquiers, editorialistes, universitaires et militaires
- **La Chatham House Rule** : les participants peuvent utiliser les informations discutees, mais ne peuvent **jamais attribuer** une declaration a un participant specifique
- **Aucun media** n'est admis, aucun enregistrement n'est autorise
- Un **comite directeur** d'environ 35 membres organise les reunions et selectionne les participants
- La securite est assuree par les **forces de l'ordre du pays hote**, financees par le contribuable

### Les Participants Notables

La liste des participants au fil des decennies comprend un veritable *Who's Who* du pouvoir mondial :

**Politique :**
- **Henry Kissinger** : present pratiquement chaque annee depuis les annees 1950
- **Angela Merkel** : invitee en 2005, quelques mois avant de devenir chanceliere
- **Emmanuel Macron** : invite en 2014, trois ans avant son election
- **Tony Blair** : invite en 1993, quatre ans avant de devenir Premier ministre
- **Bill Clinton** : invite en 1991, un an avant son election

**Finance et entreprises :**
- **Jeff Bezos** (Amazon)
- **Eric Schmidt** (Google/Alphabet)
- **Peter Thiel** (PayPal, Palantir)
- **Christine Lagarde** (FMI, puis BCE)

**Medias :**
- Editeurs et directeurs du *Washington Post*, du *Financial Times*, de *The Economist*, du *New York Times*

### La Selection des Leaders

Le point le plus troublant pour les theoriciens du complot est la **correlation entre une invitation a Bilderberg et une accession au pouvoir** peu apres :

- **Bill Clinton** invite en 1991, elu president en 1992
- **Tony Blair** invite en 1993, Premier ministre en 1997
- **Angela Merkel** invitee en 2005, chanceliere la meme annee
- **Emmanuel Macron** invite en 2014, president en 2017
- **Mark Rutte** invite regulierement, devenu secretaire general de l'OTAN en 2024

Les defenseurs du groupe expliquent que les personnes invitees sont deja des **personnalites montantes** identifiees comme de futurs leaders, et que la correlation n'implique pas la causalite. Les sceptiques retorquent que l'inverse est tout aussi plausible : ces personnes accedent au pouvoir **parce qu'elles** ont ete validees par Bilderberg.

### Liens avec le CFR et la Commission Trilaterale

Le Groupe Bilderberg n'existe pas dans un vide. Il fait partie d'un **ecosysteme de cercles d'influence** :

- Le **Council on Foreign Relations** (CFR), fonde en 1921 a New York, dont les membres ont occupe pratiquement tous les postes cles de la politique etrangere americaine
- La **Commission Trilaterale**, fondee en 1973 par **David Rockefeller** et **Zbigniew Brzezinski**, reunissant des elites d'Amerique du Nord, d'Europe et du Japon (puis de la zone Asie-Pacifique)
- Le **Forum Economique Mondial de Davos**, fonde en 1971 par **Klaus Schwab**

De nombreux participants sont membres de **plusieurs de ces organisations simultanement**, creant un reseau d'influence dense et interconnecte.

### Theories et Contre-Arguments

**Les accusations :**
- Bilderberg serait un **gouvernement mondial non elu** ou les grandes decisions sont prises avant d'etre *"vendues"* au public
- Les elections democratiques ne seraient qu'une **facade**, les veritables choix ayant ete faits dans ces reunions privees
- L'Union Europeenne, l'euro, les guerres au Moyen-Orient et les crises economiques auraient ete **planifies** a Bilderberg

**Les contre-arguments :**
- Le groupe publie desormais la **liste des participants** et les sujets de discussion generaux
- Des personnes aux opinions tres divergentes sont invitees, suggerant un **veritable debat** plutot qu'un consensus preexistant
- D'anciens participants ont decrit les reunions comme **ennuyeuses** et peu productives
- L'idee que 130 personnalites puissent garder un secret aussi longtemps est **statistiquement improbable**

### Conclusion

Le Groupe Bilderberg occupe une position unique dans l'univers des theories du complot : il est **suffisamment reel et secret** pour alimenter les soupcons, tout en etant **suffisamment ouvert** pour desamorcer les accusations les plus extremes. La question fondamentale qu'il pose reste pertinente : est-il normal que les decisions affectant des milliards de personnes soient discutees a huis clos par un groupe non elu, meme si elles ne sont pas formellement *"prises"* dans ce cadre ?"""

    slug_9 = slugify("Le Groupe Bilderberg - Le Gouvernement de l'Ombre")
    article_9 = {
        "title": "Le Groupe Bilderberg - Le Gouvernement de l'Ombre",
        "title_lower": "le groupe bilderberg - le gouvernement de l'ombre",
        "slug": slug_9,
        "summary": truncate_text("Le Groupe Bilderberg : 130 personnalites reunies a huis clos depuis 1954. Participants celebres, pre-selection des leaders et liens avec le CFR et Davos.", 200),
        "content": content_9,
        "content_html": render_markdown(content_9),
        "category": "politique",
        "tags": ["bilderberg", "elite", "gouvernement-mondial", "davos", "politique"],
        "sources": [
            {"title": "Bilderberg Meetings - Site officiel", "url": "https://www.bilderbergmeetings.org/", "type": "officiel"},
            {"title": "Liste des participants 2023", "url": "https://www.bilderbergmeetings.org/meetings/meeting-2023/participants-2023", "type": "officiel"},
        ],
        "related_articles": [],
        "author_uid": current_user.uid,
        "author_username": author_username,
        "generated_by_ai": False,
        "ai_model": "",
        "status": "published",
        "credibility": "documente",
        "classification": "confidentiel",
        "views": random.randint(50, 5000),
        "upvotes": random.randint(5, 500),
        "downvotes": random.randint(0, 50),
        "comment_count": 0,
        "created_at": timestamps[8],
        "updated_at": timestamps[8],
        "featured": False,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Hotel_De_Bilderberg.jpg/640px-Hotel_De_Bilderberg.jpg",
    }

    # =========================================================================
    # ARTICLE 10 : HAARP - Manipulation Climatique et Armes Electromagnetiques
    # =========================================================================
    content_10 = """### Introduction

Au coeur de l'Alaska, dans la ville isolee de **Gakona**, se dresse l'une des installations scientifiques les plus controversees au monde : **HAARP** (*High-frequency Active Auroral Research Program*). Ce champ d'antennes, officiellement consacre a l'etude de l'ionosphere, est accuse par de nombreux theoriciens du complot d'etre une **arme climatique** capable de provoquer des seismes, des ouragans et des secheresses a volonte.

### L'Installation

HAARP est compose de **180 antennes HF** (haute frequence) deployees sur un terrain de **14 hectares**, formant un *"IRI"* (*Ionospheric Research Instrument*) capable d'emettre **3,6 megawatts** de puissance dans l'ionosphere. Ce faisceau d'ondes electromagnetiques peut temporairement **exciter une portion de l'ionosphere**, creant un *"miroir artificiel"* permettant d'etudier les proprietes de cette couche atmospherique situee entre **85 et 600 km** d'altitude.

Le programme a ete initie en **1993**, conjointement par l'**US Air Force**, l'**US Navy** et l'**universite de l'Alaska Fairbanks** (UAF). En 2014, la gestion a ete transferee entierement a l'UAF, la rendant techniquement civile.

### Le Brevet Eastlund

La controverse autour de HAARP trouve sa source dans un brevet depose en **1987** par le physicien **Bernard Eastlund** (brevet US4686605A), intitule *"Method and Apparatus for Altering a Region in the Earth's Atmosphere, Ionosphere, and/or Magnetosphere"*. Ce brevet decrit un systeme capable de :

- **Modifier les conditions meteorologiques** en alterant les patterns de vent et de precipitation
- **Perturber les communications** ennemies sur de vastes zones
- **Detruire les missiles** en vol grace a un bouclier electromagnetique
- **Detecter** les sous-marins et les installations souterraines

Eastlund a lui-meme affirme que HAARP etait **base sur ses travaux**, bien que les responsables du programme l'aient nie. Le brevet, librement consultable, est cite comme la preuve que la technologie de manipulation climatique existe au moins en **theorie brevetee**.

### Les Theories de Nikola Tesla

Les defenseurs de la theorie HAARP font souvent reference aux travaux de **Nikola Tesla** (1856-1943), qui avait envisage la **transmission d'energie sans fil** a travers l'ionosphere. Sa tour **Wardenclyffe** (1901-1917), bien que jamais achevee, etait concue pour exploiter les **resonances naturelles** de la Terre (resonances de Schumann) pour transmettre de l'energie a l'echelle planetaire.

Selon cette theorie, HAARP serait la **realisation militaire** du reve de Tesla : un systeme capable d'injecter de l'energie dans le systeme climatique terrestre a distance, en utilisant l'ionosphere comme **relais et amplificateur**.

### Les Accusations de Manipulation Climatique

De nombreux evenements meteorologiques et geologiques ont ete attribues a HAARP :

**Seismes :**
- **Haiti, 12 janvier 2010** (magnitude 7.0) : le president venezuelien **Hugo Chavez** a publiquement accuse les Etats-Unis d'avoir provoque le seisme a l'aide de HAARP, declarant que les Americains testaient une *"arme tectonique"*
- **Japon, 11 mars 2011** (magnitude 9.1) : des theoriciens ont pointe des *"lueurs"* inhabituelles dans le ciel avant le seisme comme preuve d'activite HAARP
- **Turquie-Syrie, 6 fevrier 2023** (magnitude 7.8) : les memes accusations ont resurgi

**Ouragans et phenomenes meteorologiques :**
- **Ouragan Katrina** (2005) : accuse d'avoir ete dirige vers la Nouvelle-Orleans
- **Secheresses en Afrique** : attribuees a la manipulation des courants-jets (jet streams)
- **Inondations en Europe** : certains y voient la main de HAARP

### Les Arguments Scientifiques

Les sceptiques avancent plusieurs arguments :

- La puissance de HAARP (**3,6 MW**) est **derisoire** comparee a l'energie d'un seul orage (equivalente a une **bombe nucleaire**) ou d'un seisme (des millions de fois plus puissant)
- L'ionosphere est situee trop haut pour affecter directement la **troposphere** (couche ou se forment les phenomenes meteorologiques)
- Les seismes se produisent a des profondeurs de **10 a 700 km** sous terre, bien au-dela de toute influence electromagnetique de surface
- Les phenomenes meteorologiques sont des systemes **chaotiques** extremement complexes, impossibles a controler avec precision

Les partisans repondent que la puissance declaree est peut-etre **sous-estimee**, que des technologies classifiees pourraient amplifier les effets, et que le but n'est pas de *creer* des phenomenes mais de **declencher** ou **amplifier** des processus naturels deja en gestation.

### La Resolution du Parlement Europeen (1999)

En **1999**, le Parlement europeen a adopte une resolution exprimant des **preoccupations** concernant HAARP. Le texte qualifiait le programme de *"preoccupation mondiale"* et demandait qu'il soit soumis a un examen independant. Le rapport estimait que *"HAARP constituait un sujet de preoccupation mondiale en raison de ses implications etendues pour l'environnement"* et appelait a un moratoire.

Cette resolution, bien que non contraignante, est frequemment citee comme la preuve que meme les **institutions officielles** prennent au serieux la menace que pourrait representer HAARP.

### Les Programmes Similaires dans le Monde

HAARP n'est pas unique. D'autres nations disposent d'installations similaires :

- **SURA** (Russie) : situe pres de Nijni Novgorod, operationnel depuis 1981, avec une puissance comparable
- **EISCAT** (Europe du Nord) : un reseau radar ionospherique en Norvege, Suede et Finlande
- La **Chine** a developpe ses propres installations d'etude ionospherique, dont les details restent largement classifies

L'existence de ces programmes paralleles est vue par les theoriciens comme la preuve d'une **course aux armes climatiques** entre grandes puissances.

### Conclusion

HAARP reste un sujet ou le **secret militaire** alimente les theories les plus extravagantes. L'installation existe reellement, les brevets sont publics, et les capacites theoriques decrites dans la litterature scientifique sont troublantes. Mais le gouffre entre la *theorie* et la *capacite operationnelle* de manipuler le climat ou provoquer des seismes reste immense. Tant que les installations comme HAARP resteront partiellement **opaques au regard public**, elles continueront d'etre le symbole parfait de la frontiere entre science et conspiration."""

    slug_10 = slugify("HAARP - Manipulation Climatique et Armes Electromagnetiques")
    article_10 = {
        "title": "HAARP - Manipulation Climatique et Armes Electromagnetiques",
        "title_lower": "haarp - manipulation climatique et armes electromagnetiques",
        "slug": slug_10,
        "summary": truncate_text("HAARP en Alaska : 180 antennes HF, le brevet Eastlund, les theories de Tesla, les accusations de manipulation climatique et la resolution du Parlement europeen.", 200),
        "content": content_10,
        "content_html": render_markdown(content_10),
        "category": "technologie",
        "tags": ["haarp", "climat", "arme", "electromagnétique", "alaska"],
        "sources": [
            {"title": "HAARP - University of Alaska Fairbanks", "url": "https://haarp.gi.alaska.edu/", "type": "officiel"},
            {"title": "Brevet Bernard Eastlund (1987)", "url": "https://patents.google.com/patent/US4686605A", "type": "document"},
        ],
        "related_articles": [],
        "author_uid": current_user.uid,
        "author_username": author_username,
        "generated_by_ai": False,
        "ai_model": "",
        "status": "published",
        "credibility": "speculatif",
        "classification": "secret",
        "views": random.randint(50, 5000),
        "upvotes": random.randint(5, 500),
        "downvotes": random.randint(0, 50),
        "comment_count": 0,
        "created_at": timestamps[9],
        "updated_at": timestamps[9],
        "featured": False,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/HAARP20l.jpg/640px-HAARP20l.jpg",
    }

    # =========================================================================
    # Insertion dans Firestore
    # =========================================================================
    articles = [
        article_1,
        article_2,
        article_3,
        article_4,
        article_5,
        article_6,
        article_7,
        article_8,
        article_9,
        article_10,
    ]

    for art_data in articles:
        fb.create_article(art_data)

    flash(f"{len(articles)} dossiers ont ete deployes dans les archives!", "success")
    return redirect(url_for("wiki.home"))


# =========================================================================
#  Route de nettoyage des doublons + correction images
# =========================================================================

IMAGE_MAP = {
    "terre-plate": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=640&h=400&fit=crop",
    "epstein": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=640&h=400&fit=crop",
    "emails": "https://images.unsplash.com/photo-1568667256549-094345857637?w=640&h=400&fit=crop",
    "franc-maconnerie": "https://images.unsplash.com/photo-1572883454114-efb8df45c926?w=640&h=400&fit=crop",
    "illuminati": "https://images.unsplash.com/photo-1518640467707-6811f4a6ab73?w=640&h=400&fit=crop",
    "rothschild": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=640&h=400&fit=crop",
    "occulte": "https://images.unsplash.com/photo-1509281373149-e957c6296406?w=640&h=400&fit=crop",
    "mk-ultra": "https://images.unsplash.com/photo-1517373116369-9bdb8cdc9f62?w=640&h=400&fit=crop",
    "bilderberg": "https://images.unsplash.com/photo-1577415124269-fc1140815e3d?w=640&h=400&fit=crop",
    "haarp": "https://images.unsplash.com/photo-1527482937786-6a7c43f73124?w=640&h=400&fit=crop",
}


@seed_bp.route("/admin/fix-wiki")
@login_required
def fix_wiki():
    """Supprime les doublons et corrige les URLs d'images."""
    fb = get_firebase()

    all_articles = fb.list_articles(status="published", limit=50)
    if not all_articles:
        flash("Aucun article a corriger.", "info")
        return redirect(url_for("wiki.home"))

    # Deduplication par slug
    seen_slugs = {}
    duplicates_removed = 0
    for art in all_articles:
        slug = art.get("slug", "")
        art_id = art.get("__id", "")
        if slug in seen_slugs:
            # Doublon - supprimer
            fb.delete_document("articles", art_id)
            duplicates_removed += 1
        else:
            seen_slugs[slug] = art_id

    # Corriger les images
    images_fixed = 0
    for slug, art_id in seen_slugs.items():
        new_img = None
        if "terre-plate" in slug:
            new_img = IMAGE_MAP["terre-plate"]
        elif "epstein" in slug and "email" not in slug:
            new_img = IMAGE_MAP["epstein"]
        elif "email" in slug or "document" in slug:
            new_img = IMAGE_MAP["emails"]
        elif "franc-macon" in slug:
            new_img = IMAGE_MAP["franc-maconnerie"]
        elif "illuminati" in slug:
            new_img = IMAGE_MAP["illuminati"]
        elif "rothschild" in slug:
            new_img = IMAGE_MAP["rothschild"]
        elif "symbolis" in slug or "occulte" in slug or "rituel" in slug:
            new_img = IMAGE_MAP["occulte"]
        elif "mk-ultra" in slug or "controle-mental" in slug:
            new_img = IMAGE_MAP["mk-ultra"]
        elif "bilderberg" in slug:
            new_img = IMAGE_MAP["bilderberg"]
        elif "haarp" in slug:
            new_img = IMAGE_MAP["haarp"]

        if new_img:
            fb.update_article(art_id, {"image_url": new_img})
            images_fixed += 1

    flash(f"Nettoyage termine : {duplicates_removed} doublons supprimes, {images_fixed} images corrigees.", "success")
    return redirect(url_for("wiki.home"))
