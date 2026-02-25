"""
seed_routes.py - Routes de peuplement de la base ARCANA WIKI
Articles detailles avec ton conspirationniste, glossaire, images sensibles.
"""

from flask import Blueprint, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from .helpers import get_firebase, render_markdown, slugify, truncate_text
from datetime import datetime, timezone, timedelta
import random

seed_bp = Blueprint("seed", __name__)

# ── Glossary helper ──────────────────────────────────────────
def g(term, tooltip):
    """Shortcut pour creer un span glossary-term."""
    return f'<span class="glossary-term" data-tooltip="{tooltip}">{term}</span>'

def sensitive_img(src, caption):
    """Shortcut pour une image sensible avec overlay."""
    return f'''<div class="sensitive-image">
<img src="{src}" alt="{caption}">
<div class="sensitive-overlay">
<span class="text-3xl">&#128274;</span>
<span class="text-sm text-gray-300 mt-2">Cliquez pour reveler</span>
</div>
<span class="img-caption">{caption}</span>
</div>'''

def article_img(src, caption):
    """Image normale dans un article."""
    return f'''<img src="{src}" alt="{caption}">
<span class="img-caption">{caption}</span>'''


# =====================================================================
# ARTICLES DATA
# =====================================================================

def get_articles(author_username):
    base_date = datetime.now(timezone.utc)
    timestamps = []
    for i in range(10):
        d = random.randint(1, 30)
        h = random.randint(0, 23)
        m = random.randint(0, 59)
        ts = base_date - timedelta(days=d, hours=h, minutes=m)
        timestamps.append(ts.isoformat())
    timestamps.sort()

    articles = []

    # ─── 1. TERRE PLATE ─────────────────────────────────────
    articles.append({
        "title": "La Terre Plate et le Mur de Glace Antarctique",
        "slug": "la-terre-plate-et-le-mur-de-glace-antarctique",
        "content": f"""### Ils vous mentent depuis 500 ans

Depuis l'ecole, on vous repete que la Terre est une sphere qui tourne a 1670 km/h. Mais **personne ne l'a jamais prouve**. Les photos de la NASA ? Toutes retouchees, avouees par leurs propres employes. Le programme {g("Apollo", "Programme spatial americain 1961-1972. De nombreuses preuves suggerent que les alunissages ont ete filmes en studio.")} ? Un studio a Hollywood.

{article_img("https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&h=450&fit=crop", "La fameuse Blue Marble de la NASA - image composite, pas une photo reelle")}

### Le Modele reel

La Terre est un **disque plat** avec le Pole Nord au centre. Le Soleil et la Lune, bien plus petits et proches qu'on nous dit, tournent en cercles au-dessus du disque. L'{g("Antarctique", "Continent entourant le disque terrestre. Le Traite de 1959 interdit toute exploration independante au-dela du 60e parallele.")} forme un **mur de glace de 60 a 150 metres** tout autour, garde par les militaires de toutes les nations.

### Le Traite de l'Antarctique : la preuve ultime

En 1959, en pleine Guerre Froide, 12 nations ennemies signent un traite pour **interdire toute exploration libre** de l'Antarctique. Pourquoi ? Parce qu'au-dela du mur se trouvent potentiellement d'**autres terres**, d'autres civilisations. L'amiral {g("Richard Byrd", "Amiral americain qui a mene des expeditions en Antarctique. Son journal parle de terres au-dela du pole, d'une civilisation avancee et de vegetation luxuriante.")} a lui-meme declare dans son journal avoir decouvert des terres verdoyantes au-dela du pole.

{sensitive_img("https://images.unsplash.com/photo-1516912481808-3406841bd33c?w=800&h=450&fit=crop", "Le mur de glace antarctique - zone interdite au public depuis 1959")}

### Operation Fishbowl : tester le dome

En 1962, les USA lancent l'{g("Operation Fishbowl", "Serie de tests nucleaires en haute altitude (1962). Le nom signifie litteralement 'bocal a poissons', suggerant la connaissance d'un dome au-dessus de la Terre.")} : des bombes nucleaires tirees vers le ciel. Le nom dit tout - **fishbowl** signifie bocal a poissons. Ils testaient le {g("firmament", "Dome solide au-dessus de la Terre plate, mentionne dans la Bible et de nombreuses cosmologies anciennes.")} biblique, la barriere au-dessus de nos tetes.

### Pourquoi mentir ?

Le controle. Si les gens savaient que le monde est clos, que nous sommes dans un systeme ferme potentiellement **cree**, toute l'industrie spatiale s'effondrerait. Des milliards de dollars de budget NASA chaque annee, pour des images de synthese et des astronautes dans des piscines.

> *"La meilleure facon de cacher un secret, c'est de le mettre sous les yeux de tout le monde en le rendant ridicule."*
""",
        "category": "science",
        "tags": ["terre plate", "antarctique", "nasa", "firmament", "byrd"],
        "classification": "confidentiel",
        "credibility": "speculatif",
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=640&h=400&fit=crop",
        "views": random.randint(3000, 8000),
        "upvotes": random.randint(100, 500),
        "downvotes": random.randint(10, 50),
    })

    # ─── 2. EPSTEIN LE RESEAU ───────────────────────────────
    articles.append({
        "title": "L'Affaire Epstein : Le Reseau Pedocriminel des Elites",
        "slug": "laffaire-jeffrey-epstein-le-reseau-des-puissants",
        "content": f"""### Le plus grand scandale etouffe de l'histoire

{g("Jeffrey Epstein", "Financier americain (1953-2019). Condamne pour abus sur mineures. Retrouve mort en cellule dans des circonstances suspectes. Son reseau implique presidents, princes, et milliardaires.")} n'etait pas un simple pedophile milliardaire. Il etait le **maitre operateur** d'un reseau de chantage sexuel impliquant les personnalites les plus puissantes de la planete. Presidents, princes, PDGs, scientifiques - tous lies par un secret indicible.

{sensitive_img("https://images.unsplash.com/photo-1559128010-7c1ad6e1b6a5?w=800&h=450&fit=crop", "Little Saint James, surnommee Pedophile Island - l'ile privee d'Epstein dans les iles Vierges americaines")}

### L'ile de l'horreur : Little Saint James

Son ile privee dans les Iles Vierges, surnommee **"Pedophile Island"**, contenait un mysterieux {g("temple bleu et blanc", "Structure a rayures bleues et blanches au sommet de Little Saint James. Des photos satellites montrent qu'elle a ete demolie apres l'arrestation d'Epstein.")} visible par satellite. Des temoins parlent de **chambres souterraines**, de tunnels, et de rituels. Les employes devaient signer des accords de confidentialite draconiens.

### Le Lolita Express

Son Boeing 727 prive, le {g("Lolita Express", "Surnom du Boeing 727 prive d'Epstein. Les logs de vol revelent des dizaines de trajets avec des personnalites publiques vers son ile privee.")} , a transporte des dizaines de personnalites vers l'ile. Les **logs de vol declassifies** montrent des noms qui feraient trembler n'importe quel gouvernement. Bill Clinton : **26 vols**. Le Prince Andrew : plusieurs visites documentees avec photos.

{article_img("https://images.unsplash.com/photo-1540962351504-03099e0a754b?w=800&h=450&fit=crop", "Un jet prive similaire au Lolita Express d'Epstein - Boeing 727 modifie")}

### Le faux suicide

Le 10 aout 2019, Epstein est retrouve mort dans sa cellule au {g("Metropolitan Correctional Center", "Prison federale de New York. Les deux cameras devant la cellule d'Epstein ont miraculeusement dysfonctionne la nuit de sa mort. Les gardes dormaient.")} de New York. Officiellement : suicide. Les **deux cameras** devant sa cellule etaient en panne. Les deux gardiens dormaient. Son compagnon de cellule avait ete transfere la veille. L'autopsie independante du Dr. Baden revele des fractures compatibles avec un **strangulation**, pas une pendaison.

### Ghislaine Maxwell et le recrutement

{g("Ghislaine Maxwell", "Fille du magnat de la presse Robert Maxwell (mort mysterieusement en 1991). Principale recruteuse du reseau Epstein. Condamnee en 2022.")} , fille du magnat des medias Robert Maxwell (lui-meme retrouve mort mysterieusement sur son yacht en 1991), etait la **recruteuse en chef**. Elle approchait les victimes dans les centres commerciaux, les ecoles, les families vulnerables.

> *"Epstein ne s'est pas suicide. Il a ete reduit au silence parce qu'il connaissait les secrets de tout le monde."*
""",
        "category": "politique",
        "tags": ["epstein", "pedocriminalite", "elite", "maxwell", "clinton"],
        "classification": "top-secret",
        "credibility": "documente",
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=640&h=400&fit=crop",
        "views": random.randint(5000, 12000),
        "upvotes": random.randint(300, 800),
        "downvotes": random.randint(5, 30),
    })

    # ─── 3. DOCUMENTS EPSTEIN ───────────────────────────────
    articles.append({
        "title": "Les Documents Epstein Declassifies : Ce qu'ils revelent",
        "slug": "les-emails-et-documents-epstein-declassifies",
        "content": f"""### La liste noire

En janvier 2024, des milliers de pages de documents judiciaires ont ete rendus publics suite a l'affaire {g("Giuffre v. Maxwell", "Proces civil de Virginia Giuffre contre Ghislaine Maxwell. Les depositions et documents associes ont revele des noms et des details du reseau Epstein.")} . Ce qu'on y trouve glace le sang.

{article_img("https://images.unsplash.com/photo-1568667256549-094345857637?w=800&h=450&fit=crop", "Des milliers de pages de documents judiciaires declassifies")}

### Les noms reveles

Les depositions mentionnent directement :
- **Prince Andrew** : accuse par Virginia Giuffre d'abus sexuels a Londres, New York, et sur l'ile
- **Bill Clinton** : mentionne dans les logs de vol 26 fois, nie avoir visite l'ile
- **Alan Dershowitz** : avocat de Harvard, accuse par plusieurs victimes
- Des **PDGs de la tech**, des scientifiques, des politiciens europeens

### Le "petit carnet noir"

Le {g("Black Book", "Carnet d'adresses d'Epstein contenant plus de 1500 noms et numeros. Obtenu par un ancien employe. Contient les coordonnees de chefs d'Etat, milliardaires et celebrites.")} d'Epstein contenait plus de **1500 contacts** : numeros prives de presidents, premiers ministres, directeurs de services secrets. Pas un simple carnet d'adresses - un **registre de pouvoir**.

{sensitive_img("https://images.unsplash.com/photo-1450101499163-c8848e66ad76?w=800&h=450&fit=crop", "Reproduction symbolique du reseau de contacts d'Epstein - un des plus puissants jamais documentes")}

### Les emails : instructions de destruction

Certains emails montrent des instructions explicites pour :
- Detruire des preuves photographiques
- Transferer des fonds via des societes ecrans aux Iles Vierges
- Organiser des "massages" (terme code) avec des mineures
- Contacter des avocats pour faire taire les victimes

### L'{g("Adrenochrome", "Substance chimique produite par l'oxydation de l'adrenaline. Selon la theorie, les elites la recolteraient sur des enfants terrorises pour ses pretendus effets rajeunissants.")} : theorie ou realite ?

Plusieurs temoins et lanceurs d'alerte evoquent des **rituels** sur l'ile impliquant le prelevement de substances sur les victimes. La connexion entre le reseau Epstein et certaines pratiques occultes des elites fait l'objet de nombreuses enquetes independantes.

> *"La question n'est pas de savoir SI le reseau existait, mais combien de reseaux similaires operent encore."*
""",
        "category": "politique",
        "tags": ["epstein", "documents", "declassifie", "prince andrew", "black book"],
        "classification": "secret",
        "credibility": "documente",
        "featured": False,
        "image_url": "https://images.unsplash.com/photo-1568667256549-094345857637?w=640&h=400&fit=crop",
        "views": random.randint(4000, 9000),
        "upvotes": random.randint(200, 600),
        "downvotes": random.randint(5, 25),
    })

    # ─── 4. FRANC-MACONNERIE ────────────────────────────────
    articles.append({
        "title": "La Franc-Maconnerie : Les Architectes de l'Ombre",
        "slug": "la-franc-maconnerie-les-architectes-de-lombre",
        "content": f"""### La societe secrete la plus puissante au monde

Derriere chaque revolution, chaque guerre, chaque changement de regime se cache la main invisible de la {g("Franc-Maconnerie", "Ordre initiatique et fraternel fonde officiellement en 1717 a Londres. Organise en loges, utilise des rituels et symboles lies a l'architecture. Compte des millions de membres dans le monde.")}. De la Revolution francaise a la creation des Etats-Unis, leurs symboles sont partout - si vous savez ou regarder.

{article_img("https://images.unsplash.com/photo-1572883454114-efb8df45c926?w=800&h=450&fit=crop", "Symboles maconniques graves dans la pierre - l'equerre et le compas, emblemes universels de l'Ordre")}

### Les symboles qui vous entourent

Regardez un billet d'un dollar. La {g("pyramide inachevee", "Symbole present sur le Grand Sceau des Etats-Unis et le billet d'un dollar. L'oeil au sommet represente le Grand Architecte de l'Univers. La pyramide a 13 niveaux.")} avec l'{g("Oeil de la Providence", "Oeil dans un triangle rayonnant. Symbole du Grand Architecte de l'Univers en Franc-Maconnerie. Present sur le billet d'un dollar, dans les eglises, et sur de nombreux batiments officiels.")} vous fixe. Les mots {g("Novus Ordo Seclorum", "Devise latine sur le billet d'un dollar signifiant 'Nouvel Ordre des Siecles'. Interprete comme la preuve d'un plan pour un Nouvel Ordre Mondial.")} - "Nouvel Ordre des Siecles" - sont imprimes sous la pyramide. Ce n'est pas un hasard. Les {g("Peres fondateurs", "George Washington, Benjamin Franklin, et de nombreux signataires de la Declaration d'Independance etaient Francs-Macons.")} des USA etaient presque tous Francs-Macons.

### Les 33 degres

La plupart des Macons ne depassent jamais le 3e degre. Mais les **33 degres** du {g("Rite Ecossais", "Systeme de hauts grades maconniques comprenant 33 degres. Les niveaux superieurs sont reserves a une elite selectionnee.")} revelent des verites de plus en plus profondes. Au sommet, les inities connaissent le vrai nom du {g("Grand Architecte", "Figure supreme de la cosmologie maconnique. Au-dela du 30e degre, certains temoins affirment que le Grand Architecte est identifie comme Lucifer - porteur de lumiere.")} - et ce n'est pas celui que vous croyez.

{sensitive_img("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=450&fit=crop", "Interieur d'un temple maconnique - les deux colonnes Boaz et Jakin, le damier noir et blanc")}

### Le serment de sang

Chaque Franc-Macon prete un {g("serment d'initiation", "Au 1er degre, l'initie jure de garder les secrets de l'Ordre sous peine d'avoir la gorge tranchee. Au 2e degre, le coeur arrache. Au 3e degre, les entrailles brulees.")} sous peine de mort symbolique : gorge tranchee, coeur arrache, entrailles dispersees. "Symbolique" disent-ils. Mais combien de lanceurs d'alerte maconniques ont disparu ?

### Qui dirige vraiment ?

Presidents, juges de la Cour Supreme, generaux, PDGs - la proportion de Francs-Macons aux postes de pouvoir depasse largement le hasard statistique. Ce n'est pas un club social. C'est un **gouvernement parallele**.

> *"Les trois points ne sont pas qu'une signature. C'est un code de reconnaissance pour ceux qui gouvernent dans l'ombre."*
""",
        "category": "occultisme",
        "tags": ["franc-maconnerie", "societe secrete", "illuminati", "symboles", "nwo"],
        "classification": "secret",
        "credibility": "speculatif",
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1572883454114-efb8df45c926?w=640&h=400&fit=crop",
        "views": random.randint(3000, 7000),
        "upvotes": random.randint(200, 500),
        "downvotes": random.randint(10, 40),
    })

    # ─── 5. ILLUMINATI ──────────────────────────────────────
    articles.append({
        "title": "Les Illuminati : Du Mythe a la Realite du Pouvoir",
        "slug": "les-illuminati-de-baviere-du-mythe-a-la-realite",
        "content": f"""### L'ordre qui n'a jamais disparu

Le 1er mai 1776, Adam Weishaupt fonde l'{g("Illuminatenorden", "Ordre des Illumines de Baviere, fonde le 1er mai 1776 par Adam Weishaupt, professeur de droit canonique a Ingolstadt. Officiellement dissous en 1785, mais des preuves suggerent sa survie clandestine.")} a Ingolstadt, en Baviere. Officiellement dissous en 1785 par les autorites bavaroises, l'Ordre aurait en realite **infiltre la Franc-Maconnerie** et continue d'operer a travers elle.

{article_img("https://images.unsplash.com/photo-1518640467707-6811f4a6ab73?w=800&h=450&fit=crop", "L'Oeil qui voit tout - symbole des Illuminati present partout dans la culture populaire et l'architecture officielle")}

### Le plan en trois phases

Les documents saisis en 1785 par le gouvernement bavarois revelent un plan en trois etapes :
1. **Infiltrer** les loges maconniques et les universites
2. **Controler** les medias, la finance et l'education
3. **Instaurer** un {g("Nouvel Ordre Mondial", "Concept d'un gouvernement mondial unique controlant toutes les nations. Mentionne par George H.W. Bush dans son discours du 11 septembre 1990.")} sans frontieres ni religions

Deux siecles plus tard, regardez ou nous en sommes.

### Les symboles dans la culture pop

Ils ne se cachent plus - ils se **montrent**. Le signe du {g("triangle/pyramide", "Geste des mains formant un triangle, utilise par Jay-Z, Beyonce, Rihanna et de nombreuses celebrites. Signe de reconnaissance des Illuminati selon les theoriciens.")} fait par les celebrites, l'oeil unique cache par les pop stars, les pyramides dans les clips video... Ce n'est pas de la mode. C'est un **rituel d'obeissance publique**.

{sensitive_img("https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=450&fit=crop", "L'industrie musicale est saturee de symbolisme illuminati - un oeil cache, pyramides, rituels sur scene")}

### Le {g("Bohemian Grove", "Camp prive dans une foret de sequoias en Californie. Chaque ete, les hommes les plus puissants du monde s'y reunissent pour des ceremonies incluant la Cremation of Care devant une statue de hibou de 12 metres.")}

Chaque ete, dans une foret de sequoias en Californie, les **hommes les plus puissants du monde** se reunissent pour des rituels autour d'un hibou geant de 12 metres. Presidents, banquiers, industriels participent a la **"Cremation of Care"** - une ceremonie filmee en secret par Alex Jones en 2000.

### Le controle total

Les Illuminati de 2024 ne portent plus de robes. Ils portent des **costumes** et siegent dans les conseils d'administration du {g("World Economic Forum", "Organisation internationale fondee par Klaus Schwab. Promouvoit le Great Reset et la 4e revolution industrielle. Reunit chaque annee a Davos les dirigeants mondiaux.")}, de la {g("Banque mondiale", "Institution financiere internationale fondee en 1944. Accusee d'imposer des politiques economiques detruisant les economies des pays en developpement au profit des elites.")}, et de la {g("Commission Trilaterale", "Organisation fondee en 1973 par David Rockefeller. Reunit des elites d'Amerique du Nord, d'Europe et d'Asie pour coordonner les politiques mondiales.")}.

> *"Le plus grand tour que les Illuminati aient jamais joue, c'est de faire croire qu'ils n'existent plus."*
""",
        "category": "occultisme",
        "tags": ["illuminati", "nwo", "bohemian grove", "weishaupt", "elite"],
        "classification": "secret",
        "credibility": "speculatif",
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1518640467707-6811f4a6ab73?w=640&h=400&fit=crop",
        "views": random.randint(5000, 10000),
        "upvotes": random.randint(300, 700),
        "downvotes": random.randint(15, 45),
    })

    # ─── 6. ROTHSCHILD ──────────────────────────────────────
    articles.append({
        "title": "La Dynastie Rothschild : L'Empire Financier Invisible",
        "slug": "la-dynastie-rothschild-lempire-financier-invisible",
        "content": f"""### Les maitres de l'argent

*"Donnez-moi le controle de la monnaie d'une nation, et je me moque de qui fait ses lois."* — attribue a {g("Mayer Amschel Rothschild", "Fondateur de la dynastie bancaire Rothschild (1744-1812). A place ses cinq fils a la tete de banques dans cinq capitales europeennes : Londres, Paris, Francfort, Vienne, Naples.")}

Cette citation resument tout. Les Rothschild n'ont pas besoin de gouverner - ils **controlent ceux qui gouvernent** en controlant leur argent.

{article_img("https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=800&h=450&fit=crop", "La finance mondiale - un systeme concu par et pour les dynasties bancaires")}

### Le coup de Waterloo

En 1815, {g("Nathan Rothschild", "Fils de Mayer. A Londres, il aurait manipule la Bourse en faisant croire a une victoire de Napoleon a Waterloo, provoquant une panique, rachetant les actions a prix derisoire, puis revelant la victoire anglaise.")} utilise ses messagers prives pour apprendre la defaite de Napoleon **avant tout le monde**. Il fait semblant de vendre ses actions a la Bourse de Londres, provoquant une panique generale. Quand tout s'effondre, il rachete tout. En une journee, il **multiplie sa fortune par 20** et prend le controle de la Banque d'Angleterre.

### Les banques centrales

Les Rothschild sont derriere la creation de la plupart des {g("banques centrales", "Institutions privees controlant la creation monetaire d'un pays. La Federal Reserve (1913) n'est pas publique - elle appartient a des banquiers prives.")} du monde, y compris la {g("Federal Reserve", "Banque centrale des Etats-Unis, creee en 1913 lors d'une reunion secrete sur Jekyll Island. Malgre son nom, ce n'est pas une institution gouvernementale.")} americaine, creee lors d'une reunion secrete sur {g("Jekyll Island", "Ile au large de la Georgie (USA). En 1910, des banquiers representant 1/4 de la richesse mondiale s'y reunissent en secret pour rediger le Federal Reserve Act.")} en 1910.

{sensitive_img("https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=450&fit=crop", "Manoir Rothschild - la dynastie possede des centaines de proprietes a travers l'Europe")}

### La fortune cachee

La fortune officielle des Rothschild ? Quelques milliards. La fortune reelle, repartie sur des centaines de trusts, fondations et societes ecrans ? Estimee entre **2 et 5 trillions de dollars**. Ils possedent des vignobles, des mines, des banques, des medias - mais tout est cache derriere des structures opaques.

### Les guerres profitables

Chaque grande guerre a enrichi la dynastie. Ils financent **les deux camps** - Angleterre ET France pendant les guerres napoleoniennes, Nord ET Sud pendant la guerre civile americaine. La guerre n'est pas politique. C'est un **business model**.

> *"Quand le sang coule dans les rues, achetez de l'immobilier."* — Nathan Rothschild
""",
        "category": "finance",
        "tags": ["rothschild", "banque centrale", "federal reserve", "nwo", "finance"],
        "classification": "confidentiel",
        "credibility": "speculatif",
        "featured": False,
        "image_url": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=640&h=400&fit=crop",
        "views": random.randint(4000, 9000),
        "upvotes": random.randint(200, 500),
        "downvotes": random.randint(10, 40),
    })

    # ─── 7. SYMBOLISME OCCULTE ──────────────────────────────
    articles.append({
        "title": "Symbolisme Occulte et Rituels Sataniques dans l'Elite",
        "slug": "symbolisme-occulte-et-rituels-dans-lelite-mondiale",
        "content": f"""### Les symboles sont partout

Ouvrez les yeux. Les logos des plus grandes entreprises mondiales cachent des symboles {g("luciferiens", "Relatif a Lucifer, l'ange dechu. Dans l'occultisme d'elite, Lucifer est venere comme le porteur de lumiere et de connaissance, oppose au dieu des religions monotheistes.")}. Le logo de {g("CERN", "Organisation europeenne pour la recherche nucleaire. Son logo contient un triple 6 dissimule. Une statue de Shiva (dieu de la destruction) se trouve devant le batiment.")} contient un 666 dissimule. La statue de {g("Shiva", "Divinite hindoue de la destruction. Une statue de Shiva Nataraja de 2 metres se trouve devant le siege du CERN a Geneve, offerte par l'Inde en 2004.")} trone devant leurs locaux. Coincidence ?

{sensitive_img("https://images.unsplash.com/photo-1509281373149-e957c6296406?w=800&h=450&fit=crop", "Symbolisme occulte - pentagrammes, oeil omniscient, et rituels sont au coeur du pouvoir mondial")}

### Le {g("Spirit Cooking", "Rituels d'art performance de Marina Abramovic impliquant du sang, du sperme et du lait maternel. Des emails fuites de John Podesta (WikiLeaks) montrent des invitations a ces ceremonies.")}

En 2016, les emails {g("Podesta", "John Podesta, directeur de campagne d'Hillary Clinton. Ses emails fuites par WikiLeaks revelent des invitations a des Spirit Cooking et des references codees suspectes.")} fuites par WikiLeaks revelent des invitations a des soirees "Spirit Cooking" avec l'artiste Marina Abramovic. Des rituels impliquant du sang, des symboles kabbalistiques, et des mises en scene macabres. L'establishment a qualifie cela d'"art". Les participants sont des senateurs, des PDGs, des diplomates.

### Le {g("Pizzagate", "Theorie selon laquelle des references a la pizza dans les emails Podesta seraient un code pour des activites pedocriminelles. Le terme pizza apparaitrait comme jargon dans les milieux de trafic.")} : les emails codes

Les memes emails Podesta contiennent des references repetees a la "pizza", des "hot dogs", un "mouchoir avec une carte" - un langage qui, selon les enqueteurs citoyens, correspond a un **code pedocriminel** connu du FBI. L'enquete a ete immediatement etouffee par les medias mainstream.

{article_img("https://images.unsplash.com/photo-1534972195531-d756b9bfa9f2?w=800&h=450&fit=crop", "L'oeil qui voit tout - present dans l'architecture officielle de Washington D.C.")}

### Les ceremonies du {g("Skull and Bones", "Societe secrete de l'universite Yale, fondee en 1832. George H.W. Bush, George W. Bush, John Kerry, et de nombreux directeurs de la CIA en sont membres. Leur siege, 'the Tomb', contient des reliques humaines.")}

A Yale, l'une des universites les plus prestigieuses du monde, une societe secrete appelee Skull and Bones initie chaque annee 15 etudiants. Parmi les anciens : **deux presidents Bush, John Kerry, le fondateur de la CIA**. Leurs rituels impliquent des cercueils, des ossements humains, et des serments de loyaute a vie.

### Le message est clair

Ces symboles ne sont pas la par esthétique. C'est un **systeme de communication** entre inities, un moyen de marquer leur territoire, et un rituel de pouvoir. Quand vous les voyez, vous savez qui controle.

> *"Les symboles gouvernent le monde, pas les mots ni les lois."* — Confucius
""",
        "category": "occultisme",
        "tags": ["satanisme", "rituels", "skull and bones", "spirit cooking", "symboles"],
        "classification": "top-secret",
        "credibility": "speculatif",
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1509281373149-e957c6296406?w=640&h=400&fit=crop",
        "views": random.randint(6000, 12000),
        "upvotes": random.randint(400, 900),
        "downvotes": random.randint(20, 60),
    })

    # ─── 8. MK-ULTRA ────────────────────────────────────────
    articles.append({
        "title": "MK-Ultra : Le Programme de Controle Mental de la CIA",
        "slug": "mk-ultra-le-programme-de-controle-mental-de-la-cia",
        "content": f"""### Ce n'est pas une theorie. C'est declassifie.

Le programme {g("MK-Ultra", "Programme secret de la CIA (1953-1973) de recherche sur le controle mental. Declassifie en 1977. Impliquait LSD, hypnose, torture, privation sensorielle sur des sujets non consentants.")} est l'une des rares "theories du complot" confirmees par le gouvernement americain lui-meme. De 1953 a 1973, la {g("CIA", "Central Intelligence Agency. Service de renseignement exterieur des Etats-Unis. A mene des dizaines de programmes secrets impliquant torture, assassinats, et experimentation humaine.")} a mene des experiences de controle mental sur des **milliers de citoyens americains** sans leur consentement.

{article_img("https://images.unsplash.com/photo-1517373116369-9bdb8cdc9f62?w=800&h=450&fit=crop", "Documents declassifies MK-Ultra - la preuve que le controle mental est un fait, pas une theorie")}

### Les experiences

Sous la direction du Dr. {g("Sidney Gottlieb", "Chimiste de la CIA surnomme le 'sorcier noir'. Directeur de MK-Ultra. A administre du LSD a des centaines de personnes sans leur consentement. A detruit la plupart des dossiers en 1973.")} , surnomme le "Black Sorcerer", le programme comprenait :
- Administration de {g("LSD", "Diethylamide de l'acide lysergique. Puissant psychedelique utilise par la CIA pour tenter de briser la volonte des sujets et les rendre controlables.")} a des sujets non consentants (soldats, prisonniers, patients psychiatriques)
- **Privation sensorielle** prolongee (semaines dans le noir complet)
- **Electrochocs** a haute intensite combinee a des drogues
- **Hypnose** et suggestion post-hypnotique
- Creation d'**assassins programmes** ({g("Manchurian Candidate", "Concept d'un assassin programme par hypnose et conditionnement pour tuer sur commande, sans souvenir conscient de sa mission. Le film de 1962 s'inspire directement des recherches MK-Ultra.")})

{sensitive_img("https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&h=450&fit=crop", "Experimentation MK-Ultra - des sujets humains soumis a la torture psychologique dans des laboratoires secrets")}

### Le Dr. Cameron et l'hopital Allan Memorial

A Montreal, le Dr. {g("Donald Ewen Cameron", "Psychiatre ecossais president de l'Association mondiale de psychiatrie. A mene des experiences sur des patients canadiens : electrochocs extremes, comas artificiels, et reprogrammation mentale. Finance par la CIA.")} menait des experiences sur des patients canadiens : electrochocs 30 a 40 fois la puissance normale, comas artificials de semaines, ecoute repetitive de messages (jusqu'a 500 000 repetitions). Le but : **effacer la personnalite** et la reprogrammer.

### Destruction des preuves

En 1973, le directeur de la CIA Richard Helms ordonne la **destruction de tous les dossiers MK-Ultra**. Par miracle, 20 000 pages echappent a la destruction dans un fichier comptable mal classe. Ce qu'on sait n'est que la **pointe de l'iceberg**.

### Et aujourd'hui ?

MK-Ultra est officiellement termine. Mais ses successeurs - {g("Project Monarch", "Programme presume de controle mental hereditaire. Les sujets seraient programmes des l'enfance via des traumatismes systematiques, creant des personnalites multiples controlables.")} , {g("Project Artichoke", "Programme predecesseur de MK-Ultra (1951-1953). Objectif : creer un assassin amnesiaque utilisable et jetable. Impliquait drogues, hypnose et torture.")}, {g("Operation Mockingbird", "Programme de la CIA pour infiltrer et controler les medias americains. Des centaines de journalistes etaient finances par la CIA pour orienter l'opinion publique.")} - n'ont jamais ete pleinement exposes.

> *"20 000 pages ont survecu. Imaginez ce que contenaient les dizaines de milliers detruites."*
""",
        "category": "science",
        "tags": ["mk-ultra", "cia", "controle mental", "lsd", "gouvernement"],
        "classification": "confidentiel",
        "credibility": "documente",
        "featured": False,
        "image_url": "https://images.unsplash.com/photo-1517373116369-9bdb8cdc9f62?w=640&h=400&fit=crop",
        "views": random.randint(3000, 8000),
        "upvotes": random.randint(200, 500),
        "downvotes": random.randint(5, 20),
    })

    # ─── 9. BILDERBERG ──────────────────────────────────────
    articles.append({
        "title": "Le Groupe Bilderberg : Le Gouvernement de l'Ombre",
        "slug": "le-groupe-bilderberg-le-gouvernement-de-lombre",
        "content": f"""### 130 personnes qui decident du sort du monde

Chaque annee, environ 130 des personnes les plus puissantes de la planete se reunissent dans un hotel de luxe barre par la police et les services secrets. **Aucune couverture mediatique**. Aucun compte-rendu officiel. Aucune transparence. C'est le {g("Groupe Bilderberg", "Conference annuelle fondee en 1954 a l'hotel Bilderberg aux Pays-Bas. Reunit environ 130 leaders politiques, financiers, militaires et mediatiques d'Europe et d'Amerique du Nord.")}.

{article_img("https://images.unsplash.com/photo-1577415124269-fc1140815e3d?w=800&h=450&fit=crop", "Les reunions Bilderberg se deroulent dans des hotels de luxe isoles, sous protection militaire")}

### Qui participe ?

La liste est vertigineuse :
- **Chefs d'Etat** : Macron, Merkel, Blair, Clinton y ont assiste
- **Banquiers** : directeurs de Goldman Sachs, JP Morgan, Deutsche Bank
- **PDGs tech** : Google, Amazon, Microsoft, Meta
- **Medias** : directeurs du New York Times, Le Monde, BBC
- **Militaires** : generaux OTAN, directeurs de services secrets

Tous sous la {g("Chatham House Rule", "Regle stipulant que les participants peuvent utiliser les informations recues, mais ne doivent jamais reveler l'identite de la source. Permet des discussions 'off the record' entre les plus puissants.")} : ce qui se dit dans la salle ne doit jamais etre attribue a quiconque.

### Le schema qui se repete

Plusieurs observateurs ont note que les **decisions mondiales majeures** suivent les reunions Bilderberg :
- 1991 : Bill Clinton, gouverneur inconnu de l'Arkansas, est invite. Un an plus tard, il est president
- 2008 : Obama et Hillary Clinton disparaissent lors d'une soiree de campagne. Ils etaient a Bilderberg
- La **crise de l'euro**, le **Brexit**, les **sanctions contre la Russie** - tous discutes a Bilderberg avant d'etre "decides" par les gouvernements

{sensitive_img("https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800&h=450&fit=crop", "Hotel de luxe isole - lieu typique des conferences Bilderberg, entoure de securite militaire")}

### La {g("Commission Trilaterale", "Fondee en 1973 par David Rockefeller. Complement de Bilderberg, incluant le Japon et l'Asie-Pacifique. Zbigniew Brzezinski en fut le premier directeur.")} : l'extension

Quand Bilderberg s'est avere insuffisant pour inclure l'Asie, David Rockefeller a cree la Commission Trilaterale en 1973. Meme principe, couverture mondiale. Avec le {g("Council on Foreign Relations", "Think tank americain fonde en 1921. Pratiquement chaque Secretaire d'Etat americain en a ete membre. Considere comme le principal outil d'influence de l'elite sur la politique etrangere des USA.")} (CFR), ces trois organisations forment le **triangle du pouvoir mondial**.

> *"Nous sommes reconnaissants au Washington Post, au New York Times et aux autres grands journaux dont les directeurs ont assiste a nos reunions et respecte leurs promesses de discretion pendant pres de 40 ans."* — David Rockefeller, 1991
""",
        "category": "politique",
        "tags": ["bilderberg", "nwo", "rockefeller", "gouvernement mondial", "elite"],
        "classification": "secret",
        "credibility": "documente",
        "featured": False,
        "image_url": "https://images.unsplash.com/photo-1577415124269-fc1140815e3d?w=640&h=400&fit=crop",
        "views": random.randint(3000, 7000),
        "upvotes": random.randint(150, 400),
        "downvotes": random.randint(8, 30),
    })

    # ─── 10. HAARP ──────────────────────────────────────────
    articles.append({
        "title": "HAARP : Arme Climatique et Controle des Populations",
        "slug": "haarp-manipulation-climatique-et-armes-electromagnetiques",
        "content": f"""### Le programme qui controle la meteo

Au coeur de l'Alaska, 180 antennes geantes pointent vers le ciel. C'est {g("HAARP", "High-frequency Active Auroral Research Program. Installation militaire americaine en Alaska composee de 180 antennes haute frequence. Capable d'emettre 3.6 megawatts dans l'ionosphere.")} - le High-frequency Active Auroral Research Program. Officiellement : "recherche atmospherique". En realite : l'**arme climatique la plus puissante** jamais construite.

{article_img("https://images.unsplash.com/photo-1527482937786-6a7c43f73124?w=800&h=450&fit=crop", "Installation HAARP en Alaska - 180 antennes capables de modifier l'ionosphere terrestre")}

### Comment ca marche

HAARP bombarde l'{g("ionosphere", "Couche de l'atmosphere terrestre entre 60 et 1000 km d'altitude. Chargee electriquement, elle joue un role crucial dans la meteorologie et les communications.")} avec des ondes haute frequence a **3.6 megawatts** de puissance. En chauffant des zones specifiques de la haute atmosphere, il est possible de :
- Modifier les courants-jets et devier les systemes meteorologiques
- **Provoquer ou intensifier** des ouragans, secheresses, inondations
- Creer des tremblements de terre via la resonance {g("ELF", "Extremely Low Frequency. Ondes a tres basse frequence (3-30 Hz) pouvant penetrer le sol et les oceans. HAARP peut generer ces ondes en modulant les courants ionospheriques.")}
- Perturber les communications sur des zones entieres

### Les "coincidences"

- **Tremblement de terre d'Haiti 2010** : activite HAARP anormale detectee dans les jours precedents
- **Tsunami de 2004** : des scientifiques russes ont accuse les USA de tests ionospheriques
- **Ouragan Katrina 2005** : trajectoire anormale et intensification inexpliquee
- **Inondations en Pakistan 2010** : Hugo Chavez accuse les USA d'utiliser HAARP

{sensitive_img("https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=800&h=450&fit=crop", "Catastrophes naturelles ou armes climatiques ? Les coincidences entre activite HAARP et desastres sont troublantes")}

### Les {g("chemtrails", "Trainees chimiques. Theorie selon laquelle les trainees blanches des avions ne sont pas de la vapeur d'eau mais des produits chimiques repandus intentionnellement : baryum, aluminium, strontium.")} : le complement aerien

HAARP ne fonctionne pas seul. Les {g("trainees chimiques", "Epandage aerien presume de nanoparticules metalliques (baryum, aluminium) pour augmenter la conductivite atmospherique et faciliter les operations HAARP.")} dispersees par les avions repandent des **nanoparticules metalliques** (baryum, aluminium, strontium) qui augmentent la conductivite de l'atmosphere. Les analyses de sol dans les zones survolees montrent des niveaux anormaux de ces metaux.

### L'arme du 21e siecle

Pourquoi envoyer une armee quand on peut detruire l'economie d'un pays en provoquant une secheresse ? Pourquoi bombarder quand on peut inonder ? Le controle climatique est l'**arme ultime** : indeniable, invisible, et parfaitement deniable.

> *"D'ici 2025, nous possederons le temps."* — Rapport de l'US Air Force, "Weather as a Force Multiplier", 1996
""",
        "category": "technologie",
        "tags": ["haarp", "chemtrails", "manipulation climatique", "arme", "controle"],
        "classification": "confidentiel",
        "credibility": "speculatif",
        "featured": False,
        "image_url": "https://images.unsplash.com/photo-1527482937786-6a7c43f73124?w=640&h=400&fit=crop",
        "views": random.randint(3000, 7000),
        "upvotes": random.randint(150, 400),
        "downvotes": random.randint(10, 35),
    })

    # Assigner les timestamps
    for i, art in enumerate(articles):
        art["created_at"] = timestamps[i]
        art["updated_at"] = timestamps[i]
        art["author_uid"] = current_user.uid
        art["author_username"] = author_username
        art["status"] = "published"
        art["comment_count"] = 0
        art["title_lower"] = art["title"].lower()

    return articles


# ── SOURCES DATA ──────────────────────────────────────────────
SOURCES_MAP = {
    "terre-plate": [
        {"title": "Flat Earth Society - FAQ", "url": "https://wiki.tfes.org/", "type": "alternatif"},
        {"title": "Operation Fishbowl - Wikipedia", "url": "https://en.wikipedia.org/wiki/Operation_Fishbowl", "type": "officiel"},
        {"title": "Admiral Byrd Diary", "url": "https://archive.org/details/AdmiralByrdSecretDiary", "type": "temoignage"},
    ],
    "epstein": [
        {"title": "Court Documents - Giuffre v. Maxwell", "url": "https://www.courtlistener.com/docket/4355835/giuffre-v-maxwell/", "type": "officiel"},
        {"title": "Epstein Flight Logs", "url": "https://epsteinsblackbook.com/", "type": "fuite"},
        {"title": "Dr. Baden Autopsy Report", "url": "https://www.nytimes.com/2019/10/30/nyregion/jeffrey-epstein-homicide-michael-baden.html", "type": "officiel"},
    ],
    "documents": [
        {"title": "Declassified Court Files 2024", "url": "https://www.documentcloud.org/", "type": "officiel"},
        {"title": "Epstein Black Book Analysis", "url": "https://epsteinsblackbook.com/", "type": "alternatif"},
    ],
    "franc-macon": [
        {"title": "Grand Orient de France", "url": "https://www.godf.org/", "type": "officiel"},
        {"title": "Morals and Dogma - Albert Pike (1871)", "url": "https://archive.org/details/moralsanddogma", "type": "temoignage"},
    ],
    "illuminati": [
        {"title": "Bavarian Illuminati Documents", "url": "https://archive.org/", "type": "officiel"},
        {"title": "Bohemian Grove Footage (Alex Jones, 2000)", "url": "https://archive.org/", "type": "temoignage"},
    ],
    "rothschild": [
        {"title": "House of Rothschild - Niall Ferguson", "url": "https://archive.org/", "type": "officiel"},
        {"title": "Federal Reserve Act - History", "url": "https://www.federalreservehistory.org/", "type": "officiel"},
    ],
    "occulte": [
        {"title": "WikiLeaks - Podesta Emails", "url": "https://wikileaks.org/podesta-emails/", "type": "fuite"},
        {"title": "Skull and Bones - History", "url": "https://archive.org/", "type": "alternatif"},
    ],
    "mk-ultra": [
        {"title": "MK-Ultra CIA Documents (FOIA)", "url": "https://www.cia.gov/readingroom/collection/mkultra", "type": "officiel"},
        {"title": "Senate Hearings on MK-Ultra (1977)", "url": "https://www.intelligence.senate.gov/", "type": "officiel"},
    ],
    "bilderberg": [
        {"title": "Bilderberg Official Participant Lists", "url": "https://bilderbergmeetings.org/", "type": "officiel"},
        {"title": "David Rockefeller Memoirs (2002)", "url": "https://archive.org/", "type": "temoignage"},
    ],
    "haarp": [
        {"title": "HAARP Official Site", "url": "https://haarp.gi.alaska.edu/", "type": "officiel"},
        {"title": "Weather as a Force Multiplier - USAF Report 1996", "url": "https://archive.org/", "type": "officiel"},
    ],
}


# =====================================================================
# ROUTES
# =====================================================================

@seed_bp.route("/admin/seed-wiki")
@login_required
def seed_wiki():
    fb = get_firebase()

    # Verifier si des articles existent deja
    existing = fb.query_collection("articles", "status", "EQUAL", "published",
                                    order_by="", limit=1)
    if existing:
        flash("Les archives sont deja remplies! Utilisez /admin/reseed-wiki pour remplacer.", "info")
        return redirect(url_for("wiki.home"))

    articles = get_articles(current_user.username or current_user.display_name or "ARCANA")

    created = 0
    for art in articles:
        content_md = art.pop("content")
        content_html = render_markdown(content_md)
        art["content"] = content_md
        art["content_html"] = content_html
        art["excerpt"] = truncate_text(content_md.replace("#", "").replace("*", "").strip(), 200)

        # Ajouter les sources
        for key, sources in SOURCES_MAP.items():
            if key in art["slug"]:
                art["sources"] = sources
                break

        fb.add_document("articles", art)
        created += 1

    flash(f"{created} dossiers ont ete deposes dans les archives.", "success")
    return redirect(url_for("wiki.home"))


@seed_bp.route("/admin/reseed-wiki")
@login_required
def reseed_wiki():
    """Supprime tous les articles et re-seed avec le nouveau contenu."""
    import traceback

    try:
        fb = get_firebase()

        # Supprimer tous les articles existants
        all_articles = fb.query_collection("articles", "status", "EQUAL", "published",
                                            order_by="", limit=100)
        deleted = 0
        for art in all_articles:
            art_id = art.get("__id", "")
            if art_id:
                fb.delete_document("articles", art_id)
                deleted += 1

        # Also delete drafts
        drafts = fb.query_collection("articles", "status", "EQUAL", "draft",
                                      order_by="", limit=100)
        for art in drafts:
            art_id = art.get("__id", "")
            if art_id:
                fb.delete_document("articles", art_id)
                deleted += 1

        # Re-seed
        username = "ARCANA"
        try:
            username = current_user.username or current_user.display_name or "ARCANA"
        except Exception:
            pass

        articles = get_articles(username)

        created = 0
        errors = []
        for art in articles:
            try:
                content_md = art.pop("content")
                content_html = render_markdown(content_md)
                art["content"] = content_md
                art["content_html"] = content_html
                art["excerpt"] = truncate_text(
                    content_md.replace("#", "").replace("*", "").replace("<", "").strip(), 200
                )

                for key, sources in SOURCES_MAP.items():
                    if key in art["slug"]:
                        art["sources"] = sources
                        break

                fb.add_document("articles", art)
                created += 1
            except Exception as e:
                errors.append({"slug": art.get("slug", "?"), "error": str(e)})

        return jsonify({
            "deleted": deleted,
            "created": created,
            "errors": errors,
            "status": "ok"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc(),
            "status": "failed"
        }), 500


@seed_bp.route("/admin/fix-wiki")
@login_required
def fix_wiki():
    """Supprime les doublons et corrige les URLs d'images."""
    import requests as req

    fb = get_firebase()

    all_articles = fb.query_collection("articles", "status", "EQUAL", "published",
                                        order_by="", limit=100)

    if not all_articles:
        try:
            list_url = fb._fs_url("articles")
            resp = req.get(list_url, headers=fb._get_headers(), params={"pageSize": 100}, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                docs = data.get("documents", [])
                all_articles = [fb._parse_doc(d) for d in docs]
        except Exception:
            pass

    if not all_articles:
        return jsonify({"error": "Aucun article trouve", "method": "both_failed"}), 404

    seen_slugs = {}
    duplicates_removed = 0
    for art in all_articles:
        slug = art.get("slug", "")
        art_id = art.get("__id", "")
        if not slug or not art_id:
            continue
        if slug in seen_slugs:
            fb.delete_document("articles", art_id)
            duplicates_removed += 1
        else:
            seen_slugs[slug] = art_id

    return jsonify({
        "total_found": len(all_articles),
        "unique_slugs": list(seen_slugs.keys()),
        "duplicates_removed": duplicates_removed,
    })
