from flask import render_template, request, flash, redirect, url_for, send_file
from sqlalchemy import and_, or_
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug import secure_filename
from app.modeles.donnees import Person, Document
from app.modeles.utilisateurs import LoginForm, RegistrationForm
from app.modeles.importer import ImportForm


from ..app import app, db
# on importe l'application provenant du fichier app.py un niveau au dessus dans l'arborescence des dossiers


from ..constantes import RESULTS_PER_PAGE, DOSSIER_UPLOAD
# on importe des constantes du fichier constantes.py un niveau au dessus dans l'arborescence des dossiers
from ..modeles.donnees import Document, Authorship, Person, Tag, HasTag
# on importe la classe Document du fichier donnees.py contenu dans le dossier modeles

@app.route('/')
def accueil ():
    return render_template("pages/accueil.html", title="Accueil")

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
    query = Document.query
    titre = "Tous les documents"

    if motclef:
        query = Document.query.filter(or_(
            Document.document_title.like("%{}%".format(motclef)),
            Document.document_format.like("%{}%".format(motclef)),
            Document.document_date.like("%{}%".format(motclef)),
            Document.document_teaching.like("%{}%".format(motclef)),
            Document.document_description.like("%{}%".format(motclef)),
            Document.document_tag.any(Tag.tag_label.like("%{}%".format(motclef)))
        ))
        titre = "Résultats de la recherche « " + motclef + " »"
    else:
        titre = "Résultat de la recherche"

    if matiere:
        query = query.filter(Document.document_teaching == matiere)
        titre = titre + " pour la matière " + matiere

    # # # REQUÊTAGE EN FONCTION DES CHECKBOXES
    if img or txt or code or autre:
        # si une case format est cochée
        if img and txt and code and autre:
            titre = titre + " pour tous les formats"
        elif img and txt and code:
            query = query.filter(or_(
                Document.document_format == img,
                Document.document_format == txt,
                Document.document_format == code,
            ))
            titre = titre + " pour les formats " + img + ", " + txt + " et " + code
        elif img and txt and autre:
            query = query.filter(or_(
                Document.document_format == img,
                Document.document_format == txt,
                Document.document_format == autre,
            ))
            titre = titre + " pour les formats " + img + ", " + txt + " ou " + autre
        elif img and code and autre:
            query = query.filter(or_(
                Document.document_format == img,
                Document.document_format == code,
                Document.document_format == autre,
            ))
            titre = titre + " pour les formats " + img + ", " + code + " ou " + autre
        elif txt and code and autre:
            query = query.filter(or_(
                Document.document_format == txt,
                Document.document_format == code,
                Document.document_format == autre,
            ))
            titre = titre + " pour les formats " + txt + ", " + code + " ou " + autre
        elif img and txt:
            query = query.filter(or_(
                Document.document_format == img,
                Document.document_format == txt
            ))
            titre = titre + " pour les formats " + img + " et " + txt
        elif img and code:
            query = query.filter(or_(
                Document.document_format == img,
                Document.document_format == code
            ))
            titre = titre + " pour les formats " + img + " et " + code
        elif img and autre:
            query = query.filter(or_(
                Document.document_format == img,
                Document.document_format == autre
            ))
            titre = titre + " pour les formats " + img + " et " + autre
        elif txt and code:
            query = query.filter(or_(
                Document.document_format == txt,
                Document.document_format == code
            ))
            titre = titre + " pour les formats " + txt + " et " + code
        elif txt and autre:
            query = query.filter(or_(
                Document.document_format == txt,
                Document.document_format == autre
            ))
            titre = titre + " pour les formats " + txt + " et " + autre
        elif code and autre:
            query = query.filter(or_(
                Document.document_format == code,
                Document.document_format == autre
            ))
            titre = titre + " pour les formats " + code + " et " + autre
        elif img:
            query = query.filter(Document.document_format == img)
            titre = titre + " pour le format " + img
        elif txt:
            query = query.filter(Document.document_format == txt)
            titre = titre + " pour le format " + txt
        elif code:
            query = query.filter(Document.document_format == code)
            titre = titre + " pour le format " + code
        elif autre:
            query = query.filter(Document.document_format == autre)
            titre = titre + " pour le format " + autre
        else:
            pass

    if date:
        query = Document.query.filter(Document.document_date.like("%{}%".format(date)))


    resultats = query.order_by(Document.document_title.asc()).paginate(page=page, per_page=RESULTS_PER_PAGE)

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
        autre=autre,
        date=date,
    )

@app.route("/document/<int:docu_id>")
def document(docu_id):
    """
    Route permettant l'affichage d'une notice affichant les métadonnées relatives
    au document dont l'id est donnée en paramètre

    :param docu_id: Identifiant d'un document de la base de données (int)
    """
    # # # AJOUT D'UN NOUVEAU TAG AU DOCUMENT COURANT
    tag_label = request.args.get("tag", None)
    # on stocke le label du tag donné par l'utilisateur

    if tag_label:
        tag = Tag.add_tag(tag_label)
        # si j'ai un tag donné par l'utilisateur
        # je l'ajoute à la table Tag et je le staocke dans tag OU
        # je récupère l'enregistrement qui existe déjà avec ce label dans la table Tag
        tag_id = tag.get_id()
        # je récupère l'id de ce tag
        Tag.associate_tag_and_docu(tag_id, docu_id)
        # j'associe ce tag au document de la page courante

    # # # AFFICHAGE DE L'AUTEUR DU DOCUMENT
    requested_docu = Document.query.get(docu_id)
    # je récupère le document dont l'id correspond à l'URL de la page
    auteur = Person.query.filter(Person.created_document.any(Document.document_id == docu_id)).first()
    # j'en récupère l'auteur

    return render_template("pages/document.html", docu = requested_docu, auteur = auteur)

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

@app.route("/personne/<int:person_id>")
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


def extension_ok(nom_fichier=""):
    """ Renvoie True si le fichier possède une extension valide. """
    return '.' in nom_fichier and nom_fichier.rsplit('.', 1)[1] in ('txt', 'pdf', 'csv', 'doc', 'jpg', 'json',
                                                          'jpeg', 'gif', 'bmp', 'png', 'word', 'xml', 'py', 'odt')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    # # # VALEURS À AFFICHER DANS LES SELECTS
    docuMatiere = Document.document_teaching
    matieres = Document.query.with_entities(docuMatiere).order_by(docuMatiere).distinct(docuMatiere)
    matieres = [mat[0] for mat in matieres.all()]

    docuFormat = Document.document_format
    formats = Document.query.with_entities(docuFormat).order_by(docuFormat).distinct(docuFormat)
    formats = [formt[0] for formt in formats.all()]

    # # # VALEURS RENSEIGNÉES PAR L'UTILISATEUR
    title = request.form.get("title", None)
    description = request.form.get("desc", None)
    format = request.form.get("format", None)
    date = request.form.get("date", None)
    matiere = request.form.get("matiere", None)

    # # # IMPORT DE FICHIER
    if request.method == 'POST':
        f = request.files['file']
        # dans f, on stocke le fichier uploadé
        if f:  # on vérifie qu'un fichier a bien été envoyé
            if extension_ok(f.filename):  # on vérifie que son extension est valide
                nom = secure_filename(f.filename) # on stocke le nom de fichier dans nom
                f.save(DOSSIER_UPLOAD + nom) # et on l'enregistre dans le dossier d'upload

                dwnldLink = url_for('upped', nom=nom)
                # on stocke le lien de téléchargement du fichier uploadé
                docu = Document.add_doc(title, description, format, date, matiere, dwnldLink)
                # on ajoute le document à la BDD
                Document.associate_docu_and_user(current_user, docu)
                # on l'associe à l'user connecté dans la table Authorship
                flash(u'Fichier envoyé ! Voici <a href="{lien}">son lien</a>.'.format(lien=url_for('upped', nom=nom)),
                      'suc')
            else:
                flash(u'Ce fichier ne porte pas une extension autorisée !', 'error')
        else:
            flash(u'Vous avez oublié le fichier !', 'error')


    # form = ImportForm()
    # # formulaire ImportForm
    # if form.validate_on_submit():
    #         importer = Document(document_title=form.document_title.data,
    #                        document_description=form.document_description.data,
    #                        document_format=form.document_format.data,
    #                        document_date=form.document_date.data,
    #                        document_teaching=form.document_teaching.data,
    #                        document_downloadLink=form.document_downloadLink.data)
    #         #manque trois lignes de code, demander à Lauryne, comprendre :
    #         #importer.set_password(form.person_password.data)
    #         db.session.add(document)
    #         db.session.commit()
    #         flash('Document enregistré ! merci')
    return render_template('pages/import.html', matieres=matieres, formats=formats) #, form=form)
