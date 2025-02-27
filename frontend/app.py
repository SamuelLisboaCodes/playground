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
<<<<<<< HEAD
    prompt_with_context = prompt
    if extracted_data:
        prompt_with_context += f"\n\nConteúdo extraído do arquivo:\n{extracted_data}\n\nPor favor, baseie sua resposta no conteúdo extraído."
    
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_message}] + st.session_state.chat_messages +
                 [{"role": "user", "content": prompt_with_context}],
=======
    # Inclui o conteúdo extraído do arquivo no prompt, caso haja
    prompt_with_context = f"{prompt}\n\nConteúdo extraído do arquivo:\n{extracted_data}\n\nPor favor, baseie sua resposta no conteúdo extraído."
    
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": prompt_with_context}],
>>>>>>> e8bc4cd (Botão logout e Sidebar (Tela inicial/Criar assistente))
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p
    )
    return response.choices[0].message.content.strip()

# Página de criação do assistente
def create_assistant_page():
<<<<<<< HEAD
    st.markdown(
        """
        <h1 style="display: flex; align-items: center;">
            Criar Novo Assistente
            <img src="https://static.wixstatic.com/media/950c70_eb49b9b040b14b70972c9777d736f7ea~mv2_d_2112_2112_s_2.gif" alt="Gif" style="margin-left: 10px; height: 50px;">
        </h1>
    """, unsafe_allow_html=True)
=======
    st.title("Criar Novo Assistente")
>>>>>>> e8bc4cd (Botão logout e Sidebar (Tela inicial/Criar assistente))

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

<<<<<<< HEAD
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

=======
    # Adicionar o botão de logout no canto superior direito
>>>>>>> e8bc4cd (Botão logout e Sidebar (Tela inicial/Criar assistente))
    st.markdown(
        """
        <style>
            .logout-button {
<<<<<<< HEAD
                position: absolute;
                top: 5px;
                right: 5px;
                background-color: red;
                color: white;
=======
                position: fixed;
                top: 80px;  /* Ajustei a posição para 80px */
                right: 20px;  /* Posição à direita */
                background-color: red;  /* Cor de fundo vermelha */
                color: white;  /* Texto branco */
>>>>>>> e8bc4cd (Botão logout e Sidebar (Tela inicial/Criar assistente))
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                font-weight: 500;
<<<<<<< HEAD
                transition: transform 0.2s ease, background-color 0.2s ease;
                z-index: 9999;
=======
                transition: transform 0.2s ease, background-color 0.2s ease; /* Adicionando transição para o hover */
>>>>>>> e8bc4cd (Botão logout e Sidebar (Tela inicial/Criar assistente))
            }
            .logout-button:hover {
                background-color: darkred;
                transform: scale(1.05);
            }
        </style>
        <button class='logout-button'>Logout</button>
        """,
        unsafe_allow_html=True
    )

<<<<<<< HEAD
    page = st.sidebar.radio("Navegar para", ["Tela Inicial", "Criar Assistente"])

    if page == "Tela Inicial":
        st.markdown("<h1 style='text-align: center;'>Playground AI</h1>", unsafe_allow_html=True)

        st.subheader("Assistentes")

        if 'assistants' not in st.session_state:
            st.session_state.assistants = []

        assistant_names = ["Selecionar Assistente..."] + [assistant["name"] for assistant in st.session_state.assistants]
        selected_assistant = st.selectbox("Selecionar Assistente", assistant_names)

        selected_data = None
        if selected_assistant != "Selecionar Assistente...":
            selected_data = next((a for a in st.session_state.assistants if a["name"] == selected_assistant), None)
            if selected_data:
                st.write(f"**Modelo:** {selected_data['model']}")
                st.write(f"**Temperature:** {selected_data['temperature']}")
                st.write(f"**Top P:** {selected_data['top_p']}")
                st.text_area("Instruções do Sistema", selected_data["system_message"], height=150, disabled=True)

        uploaded_file = st.file_uploader("Upload de Arquivo (Opcional)", type=["txt", "pdf", "json", "csv"])
        extracted_data = ""
        if uploaded_file:
            extracted_data = process_uploaded_file(uploaded_file)
            st.text_area("Conteúdo do arquivo", value=str(extracted_data), height=200, disabled=True)

        st.subheader("Histórico do Chat")
        chat_history = "\n".join([f"Você: {msg['content']}\nAssistente: {st.session_state.chat_messages[i + 1]['content']}" if msg['role'] == "user" and i + 1 < len(st.session_state.chat_messages) and st.session_state.chat_messages[i + 1]['role'] == "assistant" else "" for i, msg in enumerate(st.session_state.chat_messages)]).strip()
        chat_box = st.text_area("Chat", value=chat_history, height=300, disabled=True)

        if st.button("Limpar Histórico"):
            st.session_state.chat_messages = []
            st.rerun()

        user_message = st.text_input("Enter Message", "")
        if st.button("Enviar"):
            if user_message and selected_data:
                response = query_openai_model(
                    model=selected_data["model"],
                    prompt=user_message,
                    system_message=selected_data["system_message"],
                    extracted_data=extracted_data,
                    temperature=selected_data["temperature"],
                    max_tokens=150,
                    top_p=selected_data["top_p"]
                )

                st.session_state.chat_messages.append({"role": "user", "content": user_message})
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
                st.rerun()
            elif not selected_data:
                st.warning("Por favor, selecione um assistente antes de enviar a mensagem.")

=======
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

>>>>>>> e8bc4cd (Botão logout e Sidebar (Tela inicial/Criar assistente))
    elif page == "Criar Assistente":
        create_assistant_page()

if __name__ == "__main__":
    main()
