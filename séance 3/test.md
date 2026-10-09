# Séance 3 — TP Qualité et tests

Ce document explique chaque étape réalisée pour le TP de la séance 3.
Le repo de travail est une copie de l'état de fin de séance 2 (TodoList Streamlit + SQLite),
placée dans `séance 3/todolist-seance3/`.

---

## Structure finale du repo

```
todolist-seance3/
├── .github/workflows/python-tests.yml   # Bonus : CI GitHub Actions
├── app.py                               # Interface Streamlit (avec logs)
├── todolist_utils.py                    # Logique métier isolée (testable)
├── test_todolist.py                     # Tests unitaires
├── test_integration.py                  # Test d'intégration
├── test_regression.py                   # Test de régression
└── .gitignore
```

## Historique git (un commit par étape du TP)

```
f045127 CI: workflow GitHub Actions pour exécuter pytest sur push/PR
3e59db5 Test de régression: garantir la règle anti-doublon
b3457c1 Test d'intégration: ajout remove_task + scénario ajout/marquage/suppression
07aad54 Tests unitaires: extraction logique add_task dans todolist_utils + 3 tests pytest
cce1d00 Logs: remplacement des print par logging (info/warning)
cf8f36f Débogage: ajout traces print avant/après mark_done
7a7e7be Version initiale TodoList (état séance 2 - SQLite)
```

---

## Partie 1 — Débogage

**Situation :** un utilisateur signale que le bouton « Marquer comme fait »
ne met pas toujours la tâche à jour. On veut **observer** ce qui se passe
avant de corriger quoi que ce soit.

**Modification (commit `cf8f36f`) :** ajout de deux `print` autour de l'appel
à `mark_done` dans `app.py` pour comparer l'état avant/après le clic.

```python
if not t["done"] and st.button("Marquer comme fait", key=f"done_{t['id']}"):
    print("Avant :", t)
    mark_done(t["id"])
    print("Après :", next((x for x in get_tasks() if x["id"] == t["id"]), None))
    st.rerun()
```

**Réponses aux questions :**

1. **Avant le clic** : la tâche est un dict `{"id": …, "task": "...", "done": False}`.
2. **Quelle valeur change ?** Le champ `done` passe de `False` à `True` (en base, `0 → 1`).
3. **L'état interne correspond-il à l'affichage ?** Oui : après `mark_done` + `st.rerun()`,
   la prochaine boucle d'affichage relit la base et affiche « Terminé - ... ».
4. **Pourquoi le débogage en premier ?** On ne corrige jamais à l'aveugle : on
   reproduit, on observe (traces, valeurs), on diagnostique, **puis** on corrige.
   Sans cette étape on risque de « réparer » ce qui marchait déjà.

---

## Partie 2 — Logs

**Contexte :** en production, on n'a pas l'écran de l'utilisateur. Les `print`
disparaissent. Les **logs** restent et sont filtrables par niveau de gravité.

**Modification (commit `cce1d00`) :** remplacement des `print` par `logging`.

```python
import logging
logging.basicConfig(level=logging.INFO)

# Tâche vide → warning
logging.warning("Tentative d'ajout d'une tâche vide")

# Ajout normal → info
logging.info("Ajout d'une tâche : %s", new_task)

# Marquage fait → info
logging.info("Marquage tâche terminée : %s", t["task"])
```

**Réponses aux questions :**

1. **Pourquoi logs > print en prod ?** Niveaux (DEBUG/INFO/WARNING/ERROR),
   horodatage, redirection vers un fichier ou un service centralisé, désactivables
   sans toucher au code. `print` est non structuré et part dans stdout.
2. **Quel niveau utiliser ?**
   - Information normale → `INFO` (ex. ajout d'une tâche)
   - Comportement suspect / non bloquant → `WARNING` (ex. tâche vide refusée)
3. **En quoi les logs facilitent la maintenance à distance ?** Le mainteneur
   relit la trace d'exécution sans avoir besoin de reproduire le bug ni
   d'interroger l'utilisateur.

---

## Partie 3 — Tests unitaires

**Problème :** la logique d'ajout est mélangée à Streamlit, donc non testable
sans lancer l'UI. Un mainteneur **isole toujours la logique critique**.

**Modification (commit `07aad54`) :**

- Création de `todolist_utils.py` avec une fonction pure `add_task` qui applique
  les règles métier (tâche non vide, pas de doublon) sur une simple liste de dicts.
- Création de `test_todolist.py` avec 3 tests pytest :
  - `test_add_valid_task` : ajout normal accepté
  - `test_add_empty_task` : tâche vide refusée
  - `test_add_duplicate_task` : doublon refusé

```python
# todolist_utils.py
def add_task(tasks, task, due_date):
    if task.strip() == "":
        return False
    if any(t["task"] == task for t in tasks):
        return False
    tasks.append({"task": task, "done": False, "due_date": due_date})
    return True
```

**Réponses aux questions :**

1. **Pourquoi tester sans Streamlit ?** Streamlit a besoin d'un navigateur et
   d'une session. Tester la logique pure est rapide (millisecondes), reproductible
   et n'a aucune dépendance UI.
2. **Que se passe-t-il si un test échoue après une modification ?** Le mainteneur
   sait **immédiatement** quelle règle métier a été cassée, et de quelle ligne
   vient le problème.
3. **Pourquoi « ceinture de sécurité » ?** Les tests rattrapent les régressions
   silencieuses : une modif qui « a l'air OK » mais casse un cas limite qu'on
   avait oublié.

---

## Partie 4 — Test d'intégration

**Objectif :** valider un **scénario réel** complet : ajouter → marquer fait
→ supprimer. Aucune fonction n'est testée en silo.

**Modification (commit `b3457c1`) :**

- Ajout de `remove_task` dans `todolist_utils.py`.
- Création de `test_integration.py` qui enchaîne les 3 opérations et vérifie
  l'état final.

```python
def test_task_lifecycle():
    tasks = []
    add_task(tasks, "Faire le TP", datetime.date.today())
    assert len(tasks) == 1
    tasks[0]["done"] = True
    assert tasks[0]["done"] == True
    remove_task(tasks, "Faire le TP")
    assert len(tasks) == 0
```

**Réponse à la question :** une fonction peut marcher seule (testée en unitaire)
mais casser **l'interaction** : ex. `remove_task` cherche par `task_name` mais
si `add_task` enregistre la tâche avec un nom modifié (trim, casse), la suppression
échoue. Le test d'intégration attrape ce désaccord entre fonctions.

---

## Partie 5 — Test de régression

**Situation :** un futur mainteneur refactore `add_task` et **oublie**
la règle anti-doublon. Bug réintroduit. Le test de régression doit l'empêcher
de partir en prod.

**Modification (commit `3e59db5`) :** création de `test_regression.py`.

```python
def test_no_duplicate_regression():
    tasks = []
    add_task(tasks, "Projet maintenance", datetime.date.today())
    add_task(tasks, "Projet maintenance", datetime.date.today())
    assert len(tasks) == 1
```

**Réponse à la question essentielle :** sur un projet maintenu plusieurs années,
les développeurs changent, le contexte se perd. Une règle métier ajoutée pour
résoudre un bug passé peut être réintroduite par mégarde. Le test de régression
**fige** la règle : tant qu'il est vert, on garantit que le bug d'origine ne
reviendra pas. C'est la **mémoire automatique** du projet.

---

## Bonus — Automatisation des tests avec GitHub Actions

**Modification (commit `f045127`) :** création de `.github/workflows/python-tests.yml`
pour que **chaque push et chaque pull request** déclenche `pytest` automatiquement.

```yaml
name: Python Tests
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    - run: pip install pytest streamlit
    - run: pytest
```

**Intérêt en maintenance :** un PR qui casse un test ne peut plus être mergé
sans qu'on s'en aperçoive. On passe d'une discipline humaine (« pensez à lancer
les tests ») à une **garantie automatique**.

---

## Vérification locale

```bash
cd "séance 3/todolist-seance3"
pip install pytest
pytest -v
```

Résultat obtenu :

```
test_integration.py::test_task_lifecycle PASSED            [ 20%]
test_regression.py::test_no_duplicate_regression PASSED    [ 40%]
test_todolist.py::test_add_valid_task PASSED               [ 60%]
test_todolist.py::test_add_empty_task PASSED               [ 80%]
test_todolist.py::test_add_duplicate_task PASSED           [100%]

============================== 5 passed in 0.02s ===============================
```

---

## Synthèse — ce que le TP démontre

| Pratique             | Sert à…                                              | Outil utilisé      |
|----------------------|-------------------------------------------------------|--------------------|
| Débogage             | Comprendre un comportement anormal                    | `print` temporaires|
| Logs                 | Suivre l'app en production sans accès utilisateur     | `logging`          |
| Tests unitaires      | Sécuriser une règle métier isolée                     | `pytest`           |
| Tests d'intégration  | Vérifier que plusieurs fonctions coopèrent            | `pytest`           |
| Tests de régression  | Empêcher la réapparition d'un bug déjà corrigé        | `pytest`           |
| Intégration continue | Automatiser les tests à chaque modification           | GitHub Actions     |

Ensemble, ces pratiques rendent la maintenance applicative **fiable, traçable
et durable**.
