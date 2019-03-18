from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import and_, or_
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.modeles.donnees import Person
from app.modeles.utilisateurs import LoginForm, RegistrationForm


from ..app import app, db
# on importe l'application provenant du fichier app.py un niveau au dessus dans l'arborescence des dossiers


from ..constantes import RESULTS_PER_PAGE
# on importe des constantes du fichier constantes.py un niveau au dessus dans l'arborescence des dossiers
from ..modeles.donnees import Document, Authorship
# on importe la classe Document du fichier donnees.py contenu dans le dossier modeles

@app.route('/')
def accueil ():
    return render_template("pages/accueil.html", title="Accueil")

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

    # print(jour + "-" + mois + "-" + annee)

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
        # Si on a un mot clé, on requête toutes les tables de notre base de donnée pour vérifier s'il y a des correspondances
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
        # On affiche une phrase qui indiquera les résultats de la recherche en fonction du mot clé rentré par l'utilisateur
        # Cette variable titre sera réutilisée dans la page resultats.html



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

@app.route('/login', methods=['GET', "POST"])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = Person.query.filter_by(person_login=form.person_login.data).first()
        if user is None or not user.check_password(form.person_password.data):
            flash('Nom d\'utilisateur ou mot de passe incorrect')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('recherche')
        return redirect(next_page)
    return render_template('pages/connexion.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Person(person_login=form.person_login.data,
                      person_email=form.person_email.data,
                      person_name=form.person_name.data,
                      person_firstName=form.person_firstName.data,
                      person_git=form.person_git.data,
                      person_linkedIn=form.person_linkedIn.data,
                      person_promotion=form.person_promotion.data)
        user.set_password(form.person_password.data)
        db.session.add(user)
        db.session.commit()
        flash('Inscription enregistrée. Bienvenue !')
        return redirect(url_for('login'))
    return render_template('pages/inscription.html', form=form)


@app.route("/person/<int:person_id>")
def person(person_id):
    requested_person = Person.query.get(person_id)
    # variable requested_person appelée pour classe person car requête query
    return render_template(
        "pages/person.html",
        person=requested_person)


@app.route("/annuaire")
def annuaire():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
        # reprise dans les 4 dernières lignes de code du code utilisé pour la page recherche ; permet à la fonction
        # paginate de fonctionner

    resultats = []
    resultats = Person.query.order_by(Person.person_name.asc()).paginate(page=page, per_page=RESULTS_PER_PAGE)
        # idée : création d'une liste vide, résultats dans laquelle se trouvent toutes les entrées person, requêtées par query
        # les résultats seront affichés par ordre alphabtique, grâce à order by et asc

    return render_template(
        "pages/annuaire.html",
        resultats=resultats)