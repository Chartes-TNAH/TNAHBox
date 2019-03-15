# Point d'étape 15/mars/2019

Problème avec `venv` résolu : nécessité de mettre à jour les packages ensuite, lister tous les packages utilisés par tout le monde !

## utilisateurs et BDD
sur branche `dev_user` ; fonctionnalité de base, administrateur à venir. Interface graphique (bonus) en cours.
Des champs à rentrer. On peut s'enregistrer. On peut se connecter. 
! Actuellement pas de moyen de récupérer le mot de passe.
Dans la BDD, les valeurs de **promotion** deux données, deux années ; choix de réduire à une seule année. 
Problème dans le modèle de données : seuls sont obligatoire email, id, password, dans la base de données : plusieurs erreurs à modifier. Sinon injections compliquées, car les données envoyées sont incomplètes. 
Push à venir
**Pull request à venir** > à accepter. 
Un compte existe : utilisateur = essai, mot de passe = essai. Permet d'essayer si ça fonctionne. 
Il faudra décider d'ajoute un décorateur pour si le user est logué, il puisse accéder à la page de recherche. Un décorateur sera mis, boucle. 
Problème lorsque les entrées de la BDD sont reçus en bytes. Ce problème a été résolu grâce à un `.data`.
Des commentaires dans le code de cette partie seront ajoutés. 

## BDD
Les noms ne seront plus modifiés, sauf NOTNULL à deux endroits. Il faut le mettre sur la classe plus que sur la BDD.

## Page d'accueil du projet, design
fait
Sera modifié, quelques améliorations ont été réalisées. 

## Requête facettée
Recherche par mots-clés et matière avec date est désormais possible mais l'ajout d'autres paramètres de recherche (date et format) implique beaucoup d'imbrications : work in progress.
