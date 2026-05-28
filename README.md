# TodoList Streamlit — Projet fil rouge Maintenance Applicative

Application TodoList développée pendant la séance 1 du module **Maintenance Applicative** (BUT).
Le projet sert de support au projet fil rouge collaboratif : chaque membre du groupe va maintenir,
faire évoluer et améliorer cette application en équipe en suivant les quatre types de
maintenance (corrective, évolutive, adaptative, perfective).

## Démarrer l'application

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install streamlit
streamlit run app.py
```

L'application est ensuite accessible sur http://localhost:8501.

## Organisation collaborative

### Workflow

1. Fork du dépôt sur votre compte GitHub.
2. Clone local du fork.
3. Création d'une branche dédiée à chaque tâche de maintenance.
4. Commits réguliers et descriptifs sur la branche.
5. Pull Request vers `main` du dépôt principal une fois la modification prête.
6. Revue de code par le leader / les coéquipiers, puis merge.

### Convention de nommage des branches

| Préfixe         | Type de maintenance | Exemple                              |
|-----------------|---------------------|--------------------------------------|
| `bugfix/`       | Corrective          | `bugfix/tache-vide`                  |
| `feature/`      | Évolutive           | `feature/suppression-tache`          |
| `adaptation/`   | Adaptative          | `adaptation/streamlit-cloud`         |
| `perfective/`   | Perfective          | `perfective/interface-optimisee`     |

### Convention de commits

Format court et explicite, en français :

- `Fix: empêcher les tâches vides`
- `Feat: ajouter la suppression d'une tâche`
- `Refactor: extraire la logique de stockage`
- `Docs: documenter le démarrage`

### Issues

Une **issue** est créée pour chaque tâche de maintenance et étiquetée selon son type
(`corrective`, `évolutive`, `adaptative`, `perfective`). L'issue est ensuite liée à la
Pull Request correspondante via un mot-clé (`Closes #N`).

### Pull Requests

- La branche `main` est protégée : aucun push direct, seulement via PR.
- Toute PR doit décrire clairement la modification, référencer l'issue concernée et
  préciser le type de maintenance.
- Au moins une revue est attendue avant le merge.

## Types de maintenance

| Type        | Objectif                                            |
|-------------|-----------------------------------------------------|
| Corrective  | Corriger un bug, une anomalie, une faille.          |
| Évolutive   | Ajouter / modifier une fonctionnalité métier.       |
| Adaptative  | S'adapter à un changement d'environnement technique.|
| Perfective  | Améliorer la qualité du code, l'UX, la performance. |

## Équipe

- **Leader** : [@PixxzR](https://github.com/PixxzR)
- Membres : à compléter

## Licence

Projet pédagogique BUT — usage interne.
