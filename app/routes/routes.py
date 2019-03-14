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
    motclef = request.args.get("keyword", None)
    # on stocke les mots clefs recherchés par l'utilisateur présents dans les arguments de l'URL
    matiere = request.args.get("matiere", None)
    # on récupère la valeur matiere dans les arguments correspondant au choix de l'utilisateur
    img = request.args.get("img", None)
    # on récupère 1 si l'utilisateur a coché la case image
    txt = request.args.get("txt", None)
    # on récupère 1 si l'utilisateur a coché la case txt
    code = request.args.get("code", None)
    # on récupère 1 si l'utilisateur a coché la case code
    date = request.args.get("date", None)
    # on récupère la date indiquée par l'utilisateur sous forme JJ-MM-AAAA
    jour = str(date)[7:]
    mois = str(date)[5:7]
    annee = str(date)[0:4]

    # on stocke dans des liste les extensions correspondant au différents formats de documents
    # format_img = ["jpg", "jpeg", "png", "gif"]
    # format_txt = ["odt", "doc", "docx", "pdf"]
    # format_code = ["html", "py", "js", "xml"]

    page = request.args.get("page", 1)
    # on récupère la page courante dans les arguments, si non indiquée, la valeur par défaut est 1

    docuMatiere = Document.document_teaching
    matieres = Document.query.with_entities(docuMatiere).order_by(docuMatiere).distinct(docuMatiere)
    matieres = [mat[0] for mat in matieres.all()]
    # permet d'obtenir une liste des enregistrements de matiere dans la table Document
    # où seulement le label est affiché

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

    # if motclef:
    #     if matiere:
    #         resultats = Document.query.filter(
    #             db.and_(
    #                 Document.document_title.like("%{}%".format(motclef)),
    #                 Document.document_teaching == matiere)) \
    #             .paginate(page=page, per_page=RESULTS_PER_PAGE)
    #         titre = "Résultat pour la recherche « " + motclef + " » de matière " + str(matiere)
    #     else:
    #         resultats = Document.query.filter(
    #             Document.document_title.like("%{}%".format(motclef))) \
    #             .paginate(page=page, per_page=RESULTS_PER_PAGE)
    #         titre = "Résultat pour la recherche « " + motclef + " »"
    # else:
    #     if matiere:
    #         resultats = Document.query.filter(
    #                 Document.document_teaching == matiere) \
    #             .paginate(page=page, per_page=RESULTS_PER_PAGE)
    #         titre = "Résultat pour la recherche des documents de matière " + str(matiere)
    #     else:
    #         resultats = Document.query.paginate(page=page, per_page=RESULTS_PER_PAGE)
    #         titre = "Tous les documents de la base de données"

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
        titre = "Tous les documents de la base de données"
        # si l'utilisateur ne renseigne pas de mot clef, tous les documents de la base
        # sont stockés dans résultats

    resultat_matiere = []

    if matiere:
        # si une matière est spécifiée
        for resultat in resultats.items: # .item permet de rendre resultats iterable
            # pour chaque résultat pour la recherche par mot-clef
            if resultat.document_teaching == matiere:
                # si ce résultat a pour matière la même que celle sélectionnée par l'utilisateur
                # resultat.document_teaching = nom de matière (ex : XML TEI)
                # resultat = <Document id>
                resultats = resultats.items.append(resultat)

    print(resultats)
    # else:
    #     print(resultats.items)

        #titre = "Résultat pour la recherche « " + motclef + " » de matière " + str(matiere)




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

    :param document_id: Identifiant d'un document de la base de données

    """

    requested_docu = Document.query.get(docu_id)
    # stocke dans la variable requested_docu le nom du document correspondant à l'id docu_id

    return render_template("pages/document.html", docu=requested_docu)