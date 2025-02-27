import streamlit as st
import openai
import re
import json
import pandas as pd
import pdfplumber
from dotenv import load_dotenv
import os
import requests

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
        messages=[
            {"role": "system", "content": system_message},
            {"role": role, "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p
    )
    return response.choices[0].message.content.strip()

def main():
    st.set_page_config(layout="wide", page_title="Playground AI - Assistants")
    
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
    thread_id = False
    # Título "Playground AI"
    st.markdown("<div class='playground-title'>Playground AI</div>", unsafe_allow_html=True)

    # Título "Assistants"
    st.markdown("<div class='assistants-title'>Assistants</div>", unsafe_allow_html=True)

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

if __name__ == "__main__":
    main()