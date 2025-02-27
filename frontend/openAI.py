import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import requests
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
      
# Obter a chave da API
if "auth_token" or "email" not in st.session_state:
    st.session_state["auth_token"] = None
    st.session_state["email"] = None
if "_auth_token" or "_email" not in st.session_state:
    st.session_state["_auth_token"] = st.session_state["auth_token"]
    st.session_state["_email"] = st.session_state["email"]

if not st.session_state["email"] or not st.session_state["auth_token"]:
    st.session_state["email"] = st.session_state["_email"]
    st.session_state["auth_token"] = st.session_state["_auth_token"]
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
# Função para consultar o modelo OpenAI
def query_openai_model(model, prompt, system_message, role, temperature=1.0, max_tokens=150):
    system_message += f"\n\nImportante: Você está rodando no modelo {model}. Certifique-se de mencionar isso em sua resposta."  # Garante que o modelo correto seja mencionado
    
    response = openai.chat.completions.create(  
        model=model,  
        messages=[
            {"role": "system", "content": system_message},  
            {"role": role, "content": prompt}  
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()



# Estilos CSS personalizados
st.markdown(
    """
    <style>
        .playground-title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            margin-top: 30px;
            margin-bottom: 20px;
        }
        .assistants-title {
            text-align: center;
            font-size: 20px;
            font-weight: normal;
            margin-bottom: 15px;
        }
        .center-container {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
        .stButton>button {
            display: block;
            margin: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Título "Playground AI"
st.markdown("<div class='playground-title'>Playground AI</div>", unsafe_allow_html=True)

# Título "Assistants"
st.markdown("<div class='assistants-title'>Assistants</div>", unsafe_allow_html=True)
#
#
#st.write(todos_assistants.json())
# Histórico de chat armazenado na sessão
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = ""

# Campos de entrada
name = st.text_input("Name", placeholder="Ex: Assistant Name", key="name_input")
system_message = st.text_area("System instructions", placeholder="Enter system instructions...", key="system_input")

# **Garantindo que o modelo selecionado seja passado corretamente**

model = st.selectbox("Model", ["gpt-4", "gpt-3.5-turbo"], key="model_select")
st.write(f"📌 **Modelo Selecionado:** {model}")  # Exibe o modelo selecionado para depuração

temperature = st.slider("Temperature", 0.0, 2.0, 1.0, key="temp_slider")
max_tokens = st.slider("Max tokens", 1, 4096, 2048, key="max_tokens_slider")

# Caixa de texto "Enter your message..."
st.markdown("### Enter your message...")
user_input = st.text_input("Message", key="user_input", placeholder="Digite sua mensagem aqui...")

# Upload de arquivo abaixo da caixa de texto
st.file_uploader("Upload file", type=["txt", "pdf", "json", "csv"])

# Botão "Run" centralizado
st.markdown('<div class="center-container">', unsafe_allow_html=True)
run_clicked = st.button("Run", key="run_btn")
st.markdown('</div>', unsafe_allow_html=True)

# Processar a mensagem se o botão for clicado
if run_clicked and name and system_message and user_input:
    role = "user"  
    result = query_openai_model(
        model=model,  
        prompt=user_input,
        system_message=system_message,
        role="user",
        temperature=temperature,
        max_tokens=max_tokens
    )

    # Atualizar histórico de chat na sessão
    if st.session_state.chat_history:
        st.session_state.chat_history += "\n\n"
    st.session_state.chat_history += f"**Usuário:** {user_input}\n"
    st.session_state.chat_history += f"**Assistente:** {result}"

    st.session_state.chat_history = st.session_state.chat_history.strip()
elif run_clicked:
    st.error("Por favor, preencha todos os campos (Name, System instructions e Message).")

# Exibir histórico de chat
chat_history = st.session_state.chat_history  
st.text_area("Chat history", value=chat_history, height=300, key="chat_history_display", disabled=True)

if st.button("aperte"):
    print(st.session_state)
    '''
    response = requests.post("http://127.0.0.1:8000/api/assistants", json={
    "id": "1",
    "name": "sub-criador",
    "instructions": "voce será o sub-criador de tudo",
    "model": "gpt-4o",
    "temperature": 1.0,
    "top_p": 1.0})
    '''
    #criar_thread = requests.post("http://127.0.0.1:8000/api/threads",json={"email": "rodrigoquaglio@hotmail.com"})
    #todos_assistants = requests.get("http://127.0.0.1:8000/api/assistants", {"email": st.session_state["email"]})
    #criar_mensagem_na_thread = requests.post("http://127.0.0.1:8000/api/threads/thread_mHs4uDnlJ7XTBS96nZTyzO3i/messages",json={"role": "user", "content": "ola criador!"})
    #mandar_run = requests.post("http://127.0.0.1:8000/api/threads/thread_mHs4uDnlJ7XTBS96nZTyzO3i/asst_G8X32xNikCINLfqGhX6g1Gg4/run")
    st.write(response.json())