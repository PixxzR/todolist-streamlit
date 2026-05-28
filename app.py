# fichier : app.py
import sqlite3
from pathlib import Path

import streamlit as st

DB_FILE = Path("tasks.db")


# --- Couche base de données (SQLite) ---

def get_connection():
    # Connexion réutilisable, avec lignes accessibles par nom de colonne.
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # Crée la table tasks au premier lancement si elle n'existe pas encore.
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                task       TEXT    NOT NULL,
                done       INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def get_tasks():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, task, done FROM tasks ORDER BY id ASC"
        ).fetchall()
    return [{"id": r["id"], "task": r["task"], "done": bool(r["done"])} for r in rows]


def add_task(task_text):
    with get_connection() as conn:
        conn.execute("INSERT INTO tasks (task, done) VALUES (?, 0)", (task_text,))


def mark_done(task_id):
    with get_connection() as conn:
        conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))


# --- Interface Streamlit ---

init_db()

st.title("Ma TodoList")

# Ajouter une nouvelle tâche
new_task = st.text_input("Ajouter une tâche")
if st.button("Ajouter"):
    if new_task.strip() == "":
        st.warning("Impossible d'ajouter une tâche vide.")
    elif any(t["task"] == new_task.strip() for t in st.session_state["tasks"]):
        st.warning("Cette tâche existe déjà.")
    else:
        st.session_state["tasks"].append({"task": new_task, "done": False})

# Afficher les tâches (lues depuis la base à chaque rerun)
st.subheader("Liste des tâches")
for t in get_tasks():
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.write(("Terminé - " if t["done"] else "À faire - ") + t["task"])
    with col2:
        if not t["done"] and st.button("Marquer comme fait", key=f"done_{t['id']}"):
            mark_done(t["id"])
            st.rerun()

# Lancer l'application avec : streamlit run app.py
