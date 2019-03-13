from flask import render_template, request, flash, redirect
from sqlalchemy import and_, or_
from flask_login import current_user, login_user, logout_user

from ..app import app, db
# on importe l'application provenant du fichier app.py un niveau au dessus dans l'arborescence des dossiers

from ..constantes import RESULTS_PER_PAGE
# on importe des constantes du fichier constantes.py un niveau au dessus dans l'arborescence des dossiers
from ..modeles.donnees import Document, Authorship
# on importe la classe Document du fichier donnees.py contenu dans le dossier modeles

# from ..modeles.utilisateurs import User
# on importe la classe User du fichier utilisateurs.py contenu dans le dossier modeles


@app.route("/recherche")
def recherche():
    """
    Route permettant des paramètres de recherche avancée parmi les métadonnées de la classe Document
    """
    motclef = request.args.get("keyword", None)
    # on stocke les mots clefs recherchés par l'utilisateur présents dans les arguments de l'URL
    page = request.args.get("page", 1)
    # on récupère la page courante dans les arguments, si non indiquée, la valeur par défaut est 1
    matiere = request.args.get("matiere", None)
    # on récupère la valeur matiere dans les arguments correspondant au choix de l'utilisateur

    docuMatiere = Document.document_teaching
    matieres = Document.query.with_entities(docuMatiere).order_by(docuMatiere).distinct(docuMatiere)
    matieres = [mat[0] for mat in matieres.all()]
    # pour chaque matiere de matieres

    if isinstance(page, str) and page.isdigit():
        # si la valeur de page est une chaine et ne contient que des nombres
        page = int(page)
        # on recaste la valeur en integer
    else:
        page = 1
        # sinon on lui attribue la valeur 1

    resultats = []
    # on crée une liste vide pour stocker les résultats

    titre = "Recherche"
    # on donne une valeur par défaut au titre à afficher

    if motclef:
        if str(matiere) != "all":
            resultats = Document.query.filter(
                db.and_(
                    Document.document_title.like("%{}%".format(motclef)),
                    Document.document_teaching == matiere)) \
                .paginate(page=page, per_page=RESULTS_PER_PAGE)
            titre = "Résultat pour la recherche `" + motclef + "` de matière " + str(matiere)
        else:
            resultats = Document.query.filter(
                Document.document_title.like("%{}%".format(motclef))) \
                .paginate(page=page, per_page=RESULTS_PER_PAGE)
            titre = "Résultat pour la recherche `" + motclef + "`"
    else:
        if matiere != "all":
            resultats = Document.query.filter(
                    Document.document_teaching == matiere) \
                .paginate(page=page, per_page=RESULTS_PER_PAGE)
            titre = "Résultat pour la recherche des documents de matière " + str(matiere)
        else:
            resultats = Document.query.paginate(page=page, per_page=RESULTS_PER_PAGE)
            titre = "Tous les résultats"

    # if motclef:
    #     # Si on a un mot clé, on requête toutes les tables de notre base de donnée pour vérifier s'il y a des correspondances
    #     # Le résultat de cette requête est stocké dans la liste resultats = []
    #     resultats = Document.query.filter(or_(
    #             Document.document_title.like("%{}%".format(motclef)),
    #             Document.document_format.like("%{}%".format(motclef)),
    #             Document.document_date.like("%{}%".format(motclef)),
    #             Document.document_teaching.like("%{}%".format(motclef)),
    #         )
    #     ).order_by(Document.document_title.asc()).paginate(page=page, per_page=RESULTS_PER_PAGE)
    #     titre = "Voici les résultats de votre recherche pour : '" + motclef + "`"
    #     # On affiche une phrase qui indiquera les résultats de la recherche en fonction du mot clé rentré par l'utilisateur
    #     # Cette variable titre sera réutilisée dans la page resultats.html
    #
    #     #

    return render_template(
        "pages/recherche.html",
        resultats=resultats,
        titre=titre,
        keyword=motclef,
        matiere=matiere,
        matieres=matieres
    )