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

# Função para analisar texto e buscar palavras ou outros padrões
def analyze_text(text):
    # Exemplo simples: retornar todas as palavras
    words = re.findall(r'\w+', text.lower())  # Convertendo para minúsculas para normalizar
    return words

# Função para processar CSV
def process_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

# Função para processar JSON
def process_json(uploaded_file):
    data = json.loads(uploaded_file.getvalue().decode("utf-8"))
    return data

# Função para processar conteúdo de arquivos
def process_uploaded_file(uploaded_file):
    file_type = uploaded_file.type
    
    if file_type == "text/plain":
        return uploaded_file.getvalue().decode("utf-8")
    elif file_type == "application/json":
        return process_json(uploaded_file)
    elif file_type == "text/csv":
        return process_csv(uploaded_file)
    elif file_type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    else:
        return "Formato de arquivo não suportado."

# Função para realizar uma consulta geral
def query_openai_model_with_context(model, prompt, system_message, role, extracted_data, temperature=1.0, max_tokens=150):
    system_message += f"\n\nImportante: Você está rodando no modelo {model}. Certifique-se de mencionar isso em sua resposta."

    # Adicionar os dados extraídos do arquivo no contexto
    prompt = f"{prompt}\n\nConteúdo extraído do arquivo: {extracted_data}\n\nPor favor, analise o conteúdo e forneça a resposta com base no que foi extraído."

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

    # Título "Playground AI"
    st.markdown("<div class='playground-title'>Playground AI</div>", unsafe_allow_html=True)

    # Título "Assistants"
    st.markdown("<div class='assistants-title'>Assistants</div>", unsafe_allow_html=True)

    # Histórico de chat armazenado na sessão
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = ""

    # Campos de entrada
    assistant_name = st.selectbox("Assistente", ["Assistente 1", "Assistente 2", "Assistente 3"], key="assist_select")
    name = st.text_input("Name", placeholder="Ex: Assistant Name", key="name_input")
    system_message = st.text_area("System instructions", placeholder="Enter system instructions...", key="system_input")

    # **Garantindo que o modelo selecionado seja passado corretamente**
    model = st.selectbox("Model", ["gpt-4", "gpt-3.5-turbo"], key="model_select")

    temperature = st.slider("Temperature", 0.0, 2.0, 1.0, key="temp_slider")
    max_tokens = st.slider("Max tokens", 1, 4096, 2048, key="max_tokens_slider")

    # Caixa de texto "Enter your message..."
    st.markdown("### Enter your message...")
    user_input = st.text_input("Message", key="user_input", placeholder="Digite sua mensagem aqui...")

    # Upload de arquivo abaixo da caixa de texto
    uploaded_file = st.file_uploader("Upload file", type=["txt", "pdf", "json", "csv"])

    # Processar o arquivo quando for carregado
    if uploaded_file:
        extracted_data = process_uploaded_file(uploaded_file)
        st.text_area("Conteúdo do arquivo", value=str(extracted_data), height=300, key="file_content_display", disabled=True)

        # Quando o botão "Run" for clicado
        run_clicked = st.button("Run", key="run_btn")
        if run_clicked and name and system_message and user_input:
            role = "user"

            # Chamar o modelo GPT com os dados extraídos do arquivo
            result = query_openai_model_with_context(
                model=model,  
                prompt=user_input,
                system_message=system_message,
                role=role,
                extracted_data=extracted_data,
                temperature=temperature,
                max_tokens=max_tokens
            )

            # Atualizar histórico de chat na sessão
            if st.session_state.chat_history:
                st.session_state.chat_history += "\n\n"
            st.session_state.chat_history += f"Você: {user_input}\n"
            st.session_state.chat_history += f"Assistente ({assistant_name}): {result}"

            st.session_state.chat_history = st.session_state.chat_history.strip()

    # Exibir histórico de chat
    chat_history = st.session_state.chat_history  
    st.text_area("Chat history", value=chat_history, height=300, key="chat_history_display", disabled=True)

if __name__ == "__main__":
    main()
