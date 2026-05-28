# fichier : app.py
import streamlit as st

# Stockage des tâches en mémoire (disparaît si on relance l'app)
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

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

# Afficher les tâches
st.subheader("Liste des tâches")
for i, t in enumerate(st.session_state["tasks"]):
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.write(("Terminé - " if t["done"] else "À faire - ") + t["task"])
    with col2:
        if st.button("Marquer comme fait", key=f"done_{i}"):
            st.session_state["tasks"][i]["done"] = True

# Lancer l'application avec : streamlit run app.py
