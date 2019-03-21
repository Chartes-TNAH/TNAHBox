# Point d'étape 3 21 mars 2019

## Page d'accueil
* Deux boutons vers les pages inscription et connexion
* Les trois derniers documents ajoutés à la BDD via l'interface du site (voi ci-après) sont présentés façon carrousel mais ce sont trois "card" bootstrap sur une ligne. Reprise du design de la page recherche pour homogénéité = reprise des img créées pour la page recherche par Ségolène : img, code, txt et autre.
* Footer à ajouter

## Recherche
recherche plein texte sur plusieurs champs de la page document et aussi à travers les labels des tags associés aux documents. Difficulté rencontrée : table de relation et donc bien requêter.
Pull request car modifications de la BDD.
* Les fonctionnalités de recherche sont terminées (21 mars), ajout des liens de téléchargement ; OK
* Apparence de la page recherche et résultats : **OK**
* fil à retordre donn par les tags : fonctionne. Les tags peuvent être ajoutés à chaque document et sont ajoutés à la BDD

## Profils utilisateur et comptes
* Recherche sur développement profil administrateur pour pouvoir modifier les données (accessible à certaines personnes uniquement)
* Idée aussi : possibilité de modifier son compte lorsqu'on est connecté, une interface : **OP**
* mise en forme : **OK**
* Problème de deux comptes au cours du développement, suppression d'entrées dans la BDD
* Ajout information : quand est-ce que la personne s'est connectée pour la dernière fois
* Description possible pour les utilisateurs à remplir sur leurs comptes.

## Page connexion
* Aspect amélioré ! simple et sobre, couleurs définies par le projet (couleur ENC + son inverse en bleu)

## Formulaire d'inscription
* Création d'une page pour modifier le compte ; désormais à l'inscription, l'utilisateur ne remplit pas tous les champs, juste Nom, Prénom, Login, Mdp1, Mdp2, Mail. Et une autre page pour CV, LinkedIn, GitHub et Promo, dans un second temps

## Import des documents
* Recherche solution avec WTFForm et Flask
* Recherche solution avec une fonction définie avec donnees.py `def add_doc` (`@staticmethod`) etc.
* grâce au formulaire, création d'une entrée dans la base de données lors de l'ajout d'un document.
* Il y aura une page permettant d'importer des documents, appelée 'import.html' et dans la barre de navigation : ajouter un document ; on pourra parcourir les documents présents dans l'ordinateur pour en choisir un, lui attribuer un titre, une description (des champs sont obligatoires selon le modèle de données et la BDD), un dropdown pour les matières et pour les format des choix à cliquer. + le date en AAAA ou AAAA-MM
* les informations sont liées à la BDD
* lien de téléchargement pour document
* Objectif : les documents ajoutés sont liés aux utilisateurs qui en sont les auteurs.

## Page annuaire (BONUS)
* Ajout onglet sur page accueil sur /templates/conteneur.html
* Pages /person.html (**à modifier en personne ?**) et /annuaire.html créées sur branche `dev_annuaire`
* routes.py modifié avec ajout des `@app.route("/annuaire")` et `("/person/<int:person_id>")`   >   **fonctionne**
* Problème constaté dans l'affichage de promotion sur la page person  > **BDD**
* Amélioration design et affichage,  >  bootstrap
* Documentation code : en cours
* solution pour indiquer si une personne est professeur ou étudiante : `<svg>` de couleur ENC (`#BD052D`) pour les professeurs, avec dans la partie supérieure de la page, deux boutons inactifs désignant les couleurs, sont peut-être peu visibles.
	**Page annuaire dans un état stable, pull request acceptée**


## A venir :
* Peuplement de la base de données
* Passage de localhost à serveur 
* Finitions diverses
* Documentation (modèle de données, README, etc.)