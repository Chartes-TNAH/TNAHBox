# Point d'étape 1
# 13/03/2019

## discussion à propos de la table `person` dans la BDD 
### Anticipation d'un éventuel problème :
Que faire si les champs rentrés au moment de l’inscription sont les mêmes que ceux dans la table = si un utilisateur déjà présent dans la BDD s'inscrit.

Lors de l’inscription sur le site, création d’une entrée dans `person`. Question : est-ce qu'un problème viendrait si on enregistre "Thibaut Clérice" dans la BDD et qu’il crée son compte ensuite => **conflit**. 

### problème de l'annuaire 
Il faudrait une table personne pour l'annuaire. Annuaire a pour objectif : personnes recensées dans le Master TNAH, avec peu d'informations, mais tout le monde est présente. Dans la BDD, d'autres informations, doivent-elles apparaître ?

1. Question : deux tables `person` et `user` si une personne a deux comptes ou un compte deux personnes, mais toujours unité pour la BDD pas forcément possibilité inverse. 
2. Question dans l’architecture : doit-on rentrer tout le monde dans l’annuaire ? ou laisser les utilisateurs rentrer leurs informations par eux-mêmes

### Proposition solution :
On part toujours sur la même table qui s’appelle `Person`. Une seule table son nom en anglais

- Changer la base de données ?  **réflexion**
- Choix : mieux vaut avoir des doublons qu'une nouvelle table dans la BDD




 
