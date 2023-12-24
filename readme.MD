# TP_IGL: Backend

Repo du Backend du TP IGL

## Specifications:
- Le Backend est developpé avec le framework de python **FastAPI**.
- Pour un projet propre, l'utilisation d'un environnement virtuel est super-importante, voici [Miniconda], un gestionnaire d'environnement à utiliser dans ce projet.

## Lancer l'application:
pour lancer l'application, il faut d'abord installer les bibliothèques (dependencies)
- Creer un environnement de developpement pour ce projet.
- Passer à l'environnement de developpement crée pour ce projet:
```
conda activate "environnement_name"
```
- Executer la commande suivante pour installer les bibliothèques necessaires:
```
pip install -r requirements.txt
```
- Executer la commande suivante pour lancer l'application:
```
python main.py
```
## Conventions de code:
- A la fin, si vous avez utilisé une bibliothèque qui n'a pas été deja installée, donc vous avez du utiliser la commande
```
pip install <package-name>
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;avant de "commit" les changement et les "push" sur github, executez la commande:
```
pip freeze > requirements.txt
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pour ajouter les bibliothèques utilisées aux dépendances du projet.
- toutes les requetes d'acces a la base de données doivent etre faites avec l'ORM **SQLAlchemy** pour le clean code et la securité
- avant d'implementer une fonctionnalité, creez une nouvelle branche en executant
```
git checkout -b "prenom/fonctionnalité"
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;puis apres la fin de l'implémentation, push sur la meme branche
```
git push origin "prenom/fonctionnalité"
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pour que le main reste clean et stable.
## Structure des dossiers du projet:
- **models**: pour les entités.
- **controllers**: pour les controlleurs.
- **tests**: pour les tests unitaires.
- **routes**: pour regrouper les endpoints.
- **validators**: pour les classes utilisés dans la validation des données dans les requetes.
- **utils**: pour les fonctions generales utilisés partout et les credentials.

[Miniconda]: <https://docs.conda.io/projects/miniconda/en/latest/>
