
import streamlit as st
import openai
import re
import json
import pandas as pd
import pdfplumber
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env (se necessário)
load_dotenv()

# Obter a chave da API do OpenAI (certifique-se de definir no .env ou diretamente)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para extrair números do texto
def extract_numbers_from_text(text):
    # Usar expressões regulares para capturar todos os números
    return re.findall(r'\d+', text)

# Função para processar conteúdo de arquivos
def process_uploaded_file(uploaded_file):
    file_type = uploaded_file.type
    if file_type == "text/plain":
        return uploaded_file.getvalue().decode("utf-8")
    elif file_type == "application/json":
        return json.loads(uploaded_file.getvalue().decode("utf-8"))
    elif file_type == "text/csv":
        return pd.read_csv(uploaded_file)
    elif file_type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    else:
        return "Formato de arquivo não suportado."

# Função para realizar uma consulta ao OpenAI com contexto
def query_openai_model_with_context(model, prompt, system_message, role, extracted_data, temperature=1.0, max_tokens=150, top_p=1.0):
    system_message += f"\n\nImportante: Você está rodando no modelo {model}. Certifique-se de mencionar isso em sua resposta."
    prompt = f"{prompt}\n\nConteúdo extraído do arquivo: {extracted_data}\n\nPor favor, analise o conteúdo e forneça a resposta com base no que foi extraído."
    
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_message},
                  {"role": role, "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p
    )
    return response.choices[0].message.content.strip()

def main():

    

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = "http://127.0.0.1:8501" 

    # Captura o código OAuth do Google na URL
    query_params = st.query_params
    auth_code = query_params.get("code")


    print(st.session_state)

    if auth_code and not st.session_state["auth_token"]:
        st.info("Trocando código OAuth pelo token do Google...")

        response = requests.get(f"http://127.0.0.1:8000/auth/callback?code={auth_code}")

        if response.status_code == 200:
            token_data = response.json()
            st.session_state["auth_token"] = token_data["refresh_token"]
            st.session_state["email"] = token_data["email"]
            st.success("Login realizado com sucesso!")
            st.session_state["logged_in"] = True
            
            
        else:
            st.error("Falha ao obter o token do Google.")



    # CSS página
    st.markdown(
        f"""
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
                align-items: center;
                justify-content: center;
                align-items: center;
                width: 100%;
            }
            .stButton>button {
                display: block;
                margin: auto;
            }
            .logout-button {
                position: fixed;
                top: 70px;  /* Ajustando para o botão não ficar sobre outros elementos */
                right: 20px;
                background-color: red;  /* Cor de fundo vermelha */
                color: white;  /* Texto branco */
                border: 1px solid #ccc;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                font-weight: 500;
            }
            .logout-button:hover {
                background-color: darkred;  /* Efeito de hover com cor vermelha mais escura */
                transform: scale(1.05);  /* Efeito de aumento ao passar o mouse */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Botão de "Logout" no canto superior direito
    st.markdown("<button class='logout-button'>Logout</button>", unsafe_allow_html=True)

    # Título "Playground AI"
    st.markdown("<div class='playground-title'>Playground AI</div>", unsafe_allow_html=True)


    if not st.session_state["auth_token"]:
        st.markdown(f"""
            <div class='login-container'>
                <div class='login-box'>
                    <h2>Que bom que você voltou</h2>
                    <div class='separator'>ou</div>
                    <div class='google-login'>
                        <a href="https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid%20email%20profile" 
                        target="_self">
                            <button>
                                <img src="https://auth.openai.com/assets/google-logo-NePEveMl.svg" alt="Google Logo">
                                Log in with Google
                            </button>
                        </a>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Histórico de chat armazenado na sessão
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = ""

    # Lista de assistentes na sessão
    if 'assistants' not in st.session_state:
        st.session_state.assistants = []

    # Adicionar assistente ao clicar no botão
    if st.button("Adicionar Assistente", key="add_assistant"):
        new_assistant = {"name": f"Assistente {len(st.session_state.assistants) + 1}", "system_message": "", "id": len(st.session_state.assistants)}
        st.session_state.assistants.append(new_assistant)

    # Exibir os assistentes adicionados com caixas de seleção e caixa de texto
    for assistant in st.session_state.assistants:
        col1, col2 = st.columns([1, 6])

        with col1:
            # Exibir a caixa de seleção do assistente
            assistant["name"] = st.selectbox(f"Assistente {assistant['id'] + 1}", ["Selecionar Assistente...", "Assistente 1", "Assistente 2", "Assistente 3"], key=f"assist_name_{assistant['id']}")

        with col2:
            # Exibir a caixa de texto "Instruções do Sistema" do assistente
            assistant["system_message"] = st.text_area(f"Instruções do Sistema para {assistant['id'] + 1}", key=f"system_input_{assistant['id']}", value=assistant["system_message"])

        # Exibir o botão "Remover Assistente" à esquerda da linha
        if st.button(f"Remover Assistente {assistant['id'] + 1}", key=f"remove_assist_{assistant['id']}"):
            st.session_state.assistants.remove(assistant)

    # Caixa de texto para o prompt do usuário
    st.markdown("### Enter your message...")
    user_input = st.text_input("Message", key="user_input", placeholder="Digite sua mensagem aqui...")

    # Exibir controles de parâmetros antes do botão Run
    st.markdown("### Configurações do Modelo")
    model = st.selectbox("Model", ["gpt-4", "gpt-3.5-turbo"], key="model_select")
    temperature = st.slider("Temperature", 0.0, 2.0, 1.0, key="temp_slider")
    max_tokens = st.slider("Max tokens", 1, 4096, 2048, key="max_tokens_slider")
    top_p = st.slider("Top P", 0.0, 1.0, 1.0, key="top_p_slider")  # Novo controle para top_p

    # Upload de arquivo
    uploaded_file = st.file_uploader("Upload file", type=["txt", "pdf", "json", "csv"])

    # Variável extracted_data inicialmente vazia
    extracted_data = ""

    # Processar o arquivo quando for carregado
    if uploaded_file:
        extracted_data = process_uploaded_file(uploaded_file)
        st.text_area("Conteúdo do arquivo", value=str(extracted_data), height=300, key="file_content_display", disabled=True)

    # Botão "Run" para enviar a consulta ao modelo
    run_clicked = st.button("Run", key="run_btn")
    if run_clicked and user_input:
        role = "user"

        # Chamar o modelo GPT com os dados extraídos do arquivo para cada assistente
        for assistant in st.session_state.assistants:
            result = query_openai_model_with_context(
                model=model,  
                prompt=user_input,
                system_message=assistant["system_message"],
                role=role,
                extracted_data=extracted_data,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p  # Passando top_p
            )

            # Atualizar histórico de chat na sessão
            if st.session_state.chat_history:
                st.session_state.chat_history += "\n\n"
            st.session_state.chat_history += f"Você: {user_input}\n"
            st.session_state.chat_history += f"Assistente ({assistant['name']}): {result}"

        st.session_state.chat_history = st.session_state.chat_history.strip()

    # Exibir histórico de chat
    chat_history = st.session_state.chat_history  
    st.text_area("Chat history", value=chat_history, height=300, key="chat_history_display", disabled=True)
>>>>>>> 984cd1d (Adicionei a opção de selecionar Assistente)

if __name__ == "__main__":
    main()