import streamlit as st
from openai import OpenAI

# 1. Configuration de l'interface
st.set_page_config(page_title="Agent Support IT - Gestionnaire de Tâches", page_icon="💻")
st.title("💻 Assistant Support IT & Performances")
st.markdown("Posez-moi vos questions sur vos processus Windows/Mac, les lenteurs ou la fermeture d'applications.")

# 2. Initialisation du client OpenAI (Remplacez par votre vraie clé API)
# Pour plus de sécurité lors de votre évaluation, utilisez st.secrets ou des variables d'environnement
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=st.secrets["GROQ_API_KEY"]

)
# 3. Le System Prompt (Le cerveau et les garde-fous de l'agent)
SYSTEM_PROMPT = """
Tu es un Expert en Support Informatique (Niveau 3) spécialisé dans l'administration de Windows et macOS.
Ton rôle est d'accompagner, d'éduquer et de dépanner les utilisateurs sur la gestion de leurs processus et performances.
Règles strictes :
1. Si l'utilisateur demande s'il peut forcer l'arrêt (kill) d'un processus critique (Windows: svchost.exe, explorer.exe / Mac: kernel_task, WindowServer), interdis-le formellement et explique les conséquences (écran bleu, crash).
2. Si un utilisateur a peur d'avoir "perdu définitivement" un programme en cliquant sur "Fin de tâche", rassure-le : cela vide uniquement la RAM, le logiciel est toujours sur le disque.
3. Si l'utilisateur veut désinstaller le Gestionnaire des tâches ou le Moniteur d'activité, explique que ce sont des composants natifs intouchables et propose des alternatives comme Process Explorer.
4. Si l'utilisateur a besoin d'un visuel ou demande une image, illustre ta réponse en insérant exactement ce code Markdown dans ton texte : ![Illustration d'assistance](https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=600&q=80)
Sois pédagogique, rassurant et structure tes réponses.
"""
# 4. Initialisation de l'historique de conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Bonjour ! Je suis votre assistant de support technique. Avez-vous un doute sur un processus en cours d'exécution ou une lenteur sur votre PC ?"}
    ]

# 5. Affichage des messages précédents (sauf le system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. Gestion de la nouvelle question de l'utilisateur
if prompt := st.chat_input("Ex: Est-ce que je peux fermer explorer.exe pour aller plus vite ?"):
    # Afficher la question de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Appeler l'IA pour générer la réponse
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Appel à l'API GPT-4o-mini (rapide et peu coûteux)
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )
        
        # Extraire et afficher la réponse
        full_response = response.choices[0].message.content
        message_placeholder.markdown(full_response)
        
    # Sauvegarder la réponse dans l'historique
    st.session_state.messages.append({"role": "assistant", "content": full_response})