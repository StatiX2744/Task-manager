# Projet de web serveur S4 :

Auteurs : 
- Vivien THOMAS 
- Tristan PICHARD

# Lancement du serveur et utilisation du site

Pour Lancer le serveur, se placer dans le répertoire `task_manager` et effectuer la commande suivante:

`python tasks_manager/manage.py runserver`

Puis aller à l'URL `http://127.0.0.1:8000/`.

Une base de donnée par défaut à été fournie, elle contient certains comptes pré-enregistrés, les voici :
- Nom d'utilisateur : Tristan, mot de passe :Password999
- Nom d'utilisateur : Vivien, mot de passe :Password999
- Nom d'utilisateur : Dorian, mot de passe :Password999

# But du projet :

Dans le cadre de ce projet, nous sommes ammenés à créer un site de gestion de tâches avec un système d'authentification 
et d'équipes. 
Le site est divisé en plusieurs parties qui ont différentes fonctions. Ainsi :
- La partie "Utilisateurs" regroupe les pages de création de compte, de connexion, et de visualisation d'un utilisateur.
- La partie "Tâches" regroupe les pages de création, suppression, visualisation de toutes les tâches et la visualisation détaillée d'une tâche.
- La partie "Équipe" regroupe les pages de création, visualisation de l'ensemble des équipes et visualisation des détails d'une tâche.

# Architecture du projet :

## Le dossier "admin"

Ce dossier contient tous les fichiers relatifs à l'utilisation du site par un administrateur, tel que les fichiers de paramétrage du site. 

## Le dossier "polls" :

Ce dossier contient le site en lui même, dont le contenu est séparé selon le modèle Modèle Vue Controleur (MVC). Qui consiste à séparer le traitement des données et l'affichage du site. Ainsi, grossièrement:
### La vue :
Elle est constituée du fichiers `views.py` et sert à gérer l'affichage du site.
Elle contient également le dossier `templates`, qui met à disposition les patrons des pages web en HTML5.

### Le modèle :

Il gère l'interface avec la base de données. Il regroupe les fichiers `models.py`, `tasks.py` et `teams.py`

### Le controleur :

Il sert à contrôler l'interaction entre l'utilisateur et le site.
Les fichiers `tasks.py` et `teams.py` rentrent également dans cette partie puisque il permettent de gérer les requètes de l'utilisateur.

## le dossier static :

Ce dossier sert à stocker les fichiers de stylisation du contenu, dans notre cas du CSS.

# Le fonctionnement du site :

On peut :
- Créer un utilisateur.
- Se connecter si on est déjà inscrit.
- Se déconnecter si on est connecté.

Lorsque que l'on est connecté, on peut :
- Créer une tâche.
- Supprimer/modifier cette tâche (si et seulement si on l'a créée).
- Voir les tâches publiques ou les tâches qui nous sont assignées (à nous ou à une equipe dont nous sommes membre).
- Voir toutes les équipes.
- Rejoindre/quitter une équipe.
- Changer le statut d'une tâche.

La création d'une tâche se fait par un formulaire. La liste des utilisateurs et des équipes assignées à une tâche
correspond aux deux champs "Userlist" et "Teamlist" du formulaire. Il s'agit d'entrer les noms d'utilisateurs
(ou les noms des équipes) séparés par des espaces. En cas d'un nom invalide rentré, rien ne sera validé. L'utilisation
d'espace dans les noms d'équipes n'est pas prévue.

De même, pour modifier une tâche, il faut remplir un formulaire.

Il est aussi possible de créer une sous-tâche d'une certaine tâche à condition que l'on a été assignée à celle-ci (mêmes
critères que pour changer son statut en "Effectuée" ou l'inverse.). Une sous-tâche peut avoir des utilisateurs et équipes 
assignés ainsi qu'un statut différents de la tâche mère.

Pour les équipes, il est possible de rejoindre et quitter librement toute équipe. Seul le créateur d'une équipe peut supprimer
une équipe. Une équipe peut avoir aucun membre, ce choix à été fait si les utilisateurs n'ont plus besoin d'une certaine équipe
mais que celà pouvait changer dans le futur.




