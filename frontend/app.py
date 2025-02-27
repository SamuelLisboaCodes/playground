import streamlit as st
import openai
import json
import pandas as pd
import pdfplumber
from dotenv import load_dotenv
import os
import re

# Carregar variáveis de ambiente
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para processar arquivos carregados
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
    return None

# Função para consultar o modelo da OpenAI
def query_openai_model(model, prompt, system_message, extracted_data, temperature, max_tokens, top_p):
    # Inclui o conteúdo extraído do arquivo no prompt, caso haja
    prompt_with_context = f"{prompt}\n\nConteúdo extraído do arquivo:\n{extracted_data}\n\nPor favor, baseie sua resposta no conteúdo extraído."
    
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": prompt_with_context}],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p
    )
    return response.choices[0].message.content.strip()

# Página de criação do assistente
def create_assistant_page():
    st.title("Criar Novo Assistente")

    name = st.text_input("Nome do Assistente")
    system_message = st.text_area("Instruções do Sistema")
    model = st.selectbox("Escolha o Modelo", ["gpt-4", "gpt-3.5-turbo"])
    temperature = st.slider("Temperature", 0.0, 2.0, 1.0)
    top_p = st.slider("Top P", 0.0, 1.0, 1.0)

    if st.button("Salvar Assistente"):
        if not name:
            st.warning("O nome do assistente é obrigatório!")
        else:
            new_assistant = {
                "name": name,
                "system_message": system_message,
                "model": model,
                "temperature": temperature,
                "top_p": top_p
            }

            if 'assistants' not in st.session_state:
                st.session_state.assistants = []
            
            st.session_state.assistants.append(new_assistant)
            st.success(f"Assistente '{name}' criado com sucesso!")

# Página inicial (Playground)
def main():
    st.set_page_config(layout="wide", page_title="Playground AI - Assistants")

    # Adicionar o botão de logout no canto superior direito
    st.markdown(
        """
        <style>
            .logout-button {
                position: fixed;
                top: 60px;  /* Posição ajustada */
                right: 20px;  /* Posição à direita */
                background-color: red;  /* Cor de fundo vermelha */
                color: white;  /* Texto branco */
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                font-weight: 500;
                transition: transform 0.2s ease, background-color 0.2s ease; /* Adicionando transição para o hover */
            }
            .logout-button:hover {
                background-color: darkred;  /* Efeito de hover com cor vermelha mais escura */
                transform: scale(1.05);  /* Efeito de aumento ao passar o mouse */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Botão "Logout" no canto superior direito
    st.markdown("<button class='logout-button'>Logout</button>", unsafe_allow_html=True)

    # Navegação entre as páginas
    page = st.sidebar.radio("Navegar para", ["Tela Inicial", "Criar Assistente"])

    if page == "Tela Inicial":
        st.markdown("<h1 style='text-align: center;'>Playground AI</h1>", unsafe_allow_html=True)

        st.subheader("Assistentes")

        # Lista de assistentes na sessão
        if 'assistants' not in st.session_state:
            st.session_state.assistants = []

        # Selecionar assistente
        assistant_names = ["Selecionar Assistente..."] + [assistant["name"] for assistant in st.session_state.assistants]
        selected_assistant = st.selectbox("Selecionar Assistente", assistant_names)

        # Exibir detalhes do assistente selecionado
        selected_data = None
        if selected_assistant != "Selecionar Assistente...":
            selected_data = next((a for a in st.session_state.assistants if a["name"] == selected_assistant), None)
            if selected_data:
                st.write(f"**Modelo:** {selected_data['model']}")
                st.write(f"**Temperature:** {selected_data['temperature']}")
                st.write(f"**Top P:** {selected_data['top_p']}")
                st.text_area("Instruções do Sistema", selected_data["system_message"], height=150, disabled=True)

        # **Upload de Arquivo**
        uploaded_file = st.file_uploader("Upload de Arquivo (Opcional)", type=["txt", "pdf", "json", "csv"])
        extracted_data = ""
        if uploaded_file:
            extracted_data = process_uploaded_file(uploaded_file)
            st.text_area("Conteúdo do arquivo", value=str(extracted_data), height=200, disabled=True)

        # **Histórico do Chat**
        st.subheader("Histórico do Chat")
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = ""

        st.text_area("Chat", value=st.session_state.chat_history, height=300, disabled=True)

        # **Campo para Entrada de Mensagem**
        user_message = st.text_input("Enter Message", "")
        if st.button("Enviar"):
            if user_message and selected_data:
                response = query_openai_model(
                    model=selected_data["model"],
                    prompt=user_message,
                    system_message=selected_data["system_message"],
                    extracted_data=extracted_data,  # Passar o conteúdo extraído para o modelo
                    temperature=selected_data["temperature"],
                    max_tokens=150,
                    top_p=selected_data["top_p"]
                )

                st.session_state.chat_history += f"\nUsuário: {user_message}\n{selected_assistant}: {response}"
                st.rerun()
            elif not selected_data:
                st.warning("Por favor, selecione um assistente antes de enviar a mensagem.")

    elif page == "Criar Assistente":
        create_assistant_page()

if __name__ == "__main__":
    main()
