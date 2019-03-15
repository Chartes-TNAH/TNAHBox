from flask import render_template, request, flash, redirect
from sqlalchemy import and_, or_
from flask_login import current_user, login_user, logout_user

from ..app import app, db
# on importe l'application provenant du fichier app.py un niveau au dessus dans l'arborescence des dossiers


from ..constantes import RESULTS_PER_PAGE
# on importe des constantes du fichier constantes.py un niveau au dessus dans l'arborescence des dossiers
from ..modeles.donnees import Document, Authorship
# on importe la classe Document du fichier donnees.py contenu dans le dossier modeles

@app.route('/')
def accueil ():
    return render_template("pages/accueil.html", title="accueil")

@app.route("/recherche")
def recherche():
    """
    Route permettant des paramètres de recherche avancée parmi les métadonnées de la classe Document
    """

    # # # RECUPERATION DES PARAMETRES DE RECHERCHE INDIQUES PAR L'UTILISATEUR
    motclef = request.args.get("keyword", None)
    # on stocke les mots clefs recherchés par l'utilisateur présents dans les arguments de l'URL
    matiere = request.args.get("matiere", None)
    # on récupère la valeur matiere dans les arguments correspondant au choix de l'utilisateur
    img = request.args.get("img", None)
    # on récupère image si l'utilisateur a coché la case image
    txt = request.args.get("txt", None)
    # on récupère texte si l'utilisateur a coché la case txt
    code = request.args.get("code", None)
    # on récupère code si l'utilisateur a coché la case code
    autre = request.args.get("autre", None)
    # on récupère autre si l'utilisateur a coché la case autre
    if img or txt or code or autre:
        format = 1
        # si j'ai a minima une case de cochée, j'assigne la valeur 1 à format
    date = request.args.get("date", None)
    # on récupère la date indiquée par l'utilisateur sous forme JJ-MM-AAAA

    # # # GESTION DE LA VALEUR DE PAGE COURANTE
    page = request.args.get("page", 1)
    # on récupère la page courante dans les arguments, si non indiquée, la valeur par défaut est 1
    if isinstance(page, str) and page.isdigit():
        # si la valeur de page est une chaine et ne contient que des nombres
        page = int(page)
        # on recaste la valeur en integer
    else:
        page = 1
        # sinon on lui attribue la valeur 1

    # # # RECUPERATION DES VALEURS DE LA BDD À FAIRE AFFICHER SUR LA PAGE DE RECHERCHE
    docuMatiere = Document.document_teaching
    matieres = Document.query.with_entities(docuMatiere).order_by(docuMatiere).distinct(docuMatiere)
    matieres = [mat[0] for mat in matieres.all()]
    # permet d'obtenir une liste des enregistrements de matiere dans la table Document
    # où seulement le label est affiché

    # # # REQUÊTAGE EN FONCTION DES PARAMÈTRES DE RECHERCHE DE L'UTILISATEUR
    resultats = []
    # on crée une liste vide pour stocker les résultats

    titre = "Recherche"
    # on donne une valeur par défaut au titre à afficher

    if motclef:
        # Si on a un mot clé, on requête toutes les champs de Document
        # Le résultat de cette requête est stocké dans la liste resultats = []
        resultats = Document.query.filter(or_(
                Document.document_title.like("%{}%".format(motclef)),
                Document.document_format.like("%{}%".format(motclef)),
                Document.document_date.like("%{}%".format(motclef)),
                Document.document_teaching.like("%{}%".format(motclef)),
                Document.document_description.like("%{}%".format(motclef))
            )
        ).order_by(Document.document_title.asc()).paginate(page=page, per_page=RESULTS_PER_PAGE)
        titre = "Résultats de votre recherche pour : « " + motclef + " »"
        # Si l'utilisateur n'a renseigné qu'un mot clef, titre donne le message à afficher
    else:
        resultats = Document.query.paginate(page=page, per_page=RESULTS_PER_PAGE)
        titre = "Résultat de la recherche"
        # si l'utilisateur ne renseigne pas de mot clef, tous les documents de la base
        # sont stockés dans résultats

    resultats_facettes = []

    if matiere:
        # si une matière est spécifiée
        for resultat in resultats.items: # .item permet de rendre resultats iterable
            # pour chaque résultat pour la recherche par mot-clef
            if resultat.document_teaching == matiere:
                # si ce résultat a pour matière la même que celle sélectionnée par l'utilisateur
                # resultat.document_teaching = nom de matière (ex : XML TEI)
                # resultat = <Document id>
                resultats_facettes = resultats_facettes.append(resultat)

    if format:
        # si un format a été coché
        for resultat in resultats.items:  # .item permet de rendre resultats iterable
            # pour chaque résultat pour la recherche par mot-clef
            if img:
                if resultat.document_format == img:
                    resultats_facettes = resultats_facettes.append(resultat)
            if txt:
                if resultat.document_format == txt:
                    resultats_facettes = resultats_facettes.append(resultat)
            if code:
                if resultat.document_format == code:
                    resultats_facettes = resultats_facettes.append(resultat)
            if autre:
                if resultat.document_format == autre:
                    resultats_facettes = resultats_facettes.append(resultat)

    if date:
        for resultat in resultats.items:
            if len(date) == 10:
                if resultat.document_date == date:
                    resultats_facettes = resultats_facettes.append(resultat)
            elif len(date) == 7:
                resultats = Document.query.filter(
                    docu_date[0:7] == date) \
                    .paginate(page=page, per_page=RESULTS_PER_PAGE)
            elif len(date) == 4:
                resultats = Document.query.filter(
                    docu_date[0:4] == date) \
                    .paginate(page=page, per_page=RESULTS_PER_PAGE)

    print(resultats_facettes)

    return render_template(
        "pages/recherche.html",
        resultats=resultats,
        titre=titre,
        keyword=motclef,
        matiere=matiere,
        matieres=matieres,
        img=img,
        txt=txt,
        code=code,
        date=date,
    )

@app.route("/document/<int:docu_id>")
def document(docu_id):
    """
    Route permettant l'affichage d'une notice affichant les métadonnées relatives
    au document dont l'id est donnée en paramètre

    :param docu_id: Identifiant d'un document de la base de données

    """

    requested_docu = Document.query.get(docu_id)
    # stocke dans la variable requested_docu le nom du document correspondant à l'id docu_id

    return render_template("pages/document.html", docu=requested_docu)