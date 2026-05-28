# fichier : app.py
import streamlit as st

# Stockage des tâches en mémoire (disparaît si on relance l'app)
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

st.title("Ma TodoList")

# Ajouter une nouvelle tâche
new_task = st.text_input("Ajouter une tâche")
if st.button("Ajouter"):
    if new_task.strip() != "":
        st.session_state["tasks"].append({"task": new_task, "done": False})

# Afficher les tâches
st.subheader("Liste des tâches")
for i, t in enumerate(st.session_state["tasks"]):
    col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
    with col1:
        st.write(("Terminé - " if t["done"] else "À faire - ") + t["task"])
    with col2:
        if st.button("Fait", key=f"done_{i}"):
            st.session_state["tasks"][i]["done"] = True
            st.rerun()
    with col3:
        if st.button("Supprimer", key=f"delete_{i}"):
            st.session_state["tasks"].pop(i)
            st.rerun()

# Lancer l'application avec : streamlit run app.py
