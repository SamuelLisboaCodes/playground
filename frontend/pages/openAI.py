import streamlit as st
from dotenv import load_dotenv
import openai
import requests
import os
from main import initialize_session_state, save_user_state
import openai
import json
import pandas as pd
import pdfplumber


API_URL = "http://127.0.0.1:8000/api/"  


def change_thread(): 
    st.session_state.messages = []
    response_data = requests.get(API_URL + f'threads/{st.session_state['thread_id']}/messages')
    messages = json.loads(response_data.text)
    for msg in messages:
        formatted_message = {
            "role": msg["role"],
            "content": msg["content"],

        }
        st.session_state.messages.append(formatted_message)
    return st.session_state.messages


def handle_logout_click():
    response = requests.post("http://127.0.0.1:8000/auth/logout", json={"email":st.session_state["email"]})
    if response.status_code == 200:
        save_user_state(logged_in=False, email='', auth_token=None)
        st.write("logout realizado com sucesso")
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
    model = st.selectbox("Escolha o Modelo", ["gpt-4o","gpt-4o-mini","gpt-4.5-preview" ,"gpt-3.5-turbo"])
    max_tokens = st.slider("Max tokens", 1, 4096, 2048)
    temperature = st.slider("Temperature", 0.0, 2.0, 1.0)
    top_p = st.slider("Top P", 0.0, 1.0, 1.0)

    if st.button("Salvar Assistente"):
        if not name:
            st.warning("O nome do assistente é obrigatório!")
        else:
                payload = {
                           "id": "0",
                "name": name,
                "instructions": system_message,
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p
            }

                response = requests.post(API_URL + 'assistants', json={"user_email": st.session_state["email"], "request": payload})
                
                if response.status_code == 200:
                    st.success("Assistente criado com sucesso!")
                    
                else:
                    st.error(f"Erro ao criar assistente: {response.text}")


def openAI_page():
# Carregar variáveis de ambiente do arquivo .env
    
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    initialize_session_state()

    # Adicionar o botão de logout no canto superior direito
    st.markdown(
        """
        <style>
            .element-container:has(style){
                display: none;
            }
            #logout-button {
                display: none;
            }
            .element-container:has(#logout-button) {
                display: none;
            }
            .element-container:has(#logout-button) + div button{
                position: absolute;
                top: 5px;  /* Posição mais para cima */
                right: 5px;  /* Posição mais à direita */
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
                z-index: 9999;  /* Garante que o botão fique acima de outros elementos */
            }

            .element-container:has(#logout-button) + div button:hover {
                background-color: darkred;  /* Efeito de hover com cor vermelha mais escura */
                transform: scale(1.05);  /* Efeito de aumento ao passar o mouse */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Botão "Logout" no canto superior direito
    st.markdown("<span id='logout-button'></span>", unsafe_allow_html=True)
    st.button("logout", on_click=handle_logout_click)
    # Navegação entre as páginas
    page = st.sidebar.radio("Navegar para", ["Tela Inicial", "Criar Assistente"])

    if page == "Tela Inicial":
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

        if "messages" not in st.session_state:
            st.session_state.messages = []  

        col1, col2 = st.columns([2, 3])

        with col1:
            st.markdown("### Configuração do Assistente")
            response = requests.get(API_URL + f'assistants?email={st.session_state['email']}')
            id_assistentes = json.loads(response.text)
            print(id_assistentes)
            if id_assistentes:
                assistants_list = {i:requests.get( API_URL + 'assistants/' + ass + '/retrieve') for i, ass in enumerate(id_assistentes)}
                
                id_to_name = lambda id_procurado: next((a.json()["name"] for a in assistants_list.values() if a.json()['id'] == id_procurado),  "Não encontrado")

                assistant_id = st.selectbox("Assistente", id_assistentes, format_func = id_to_name, key="assistant_select")
                assistant = requests.get( API_URL + 'assistants/' + assistant_id + '/retrieve')
                assistant_attrs = json.loads(assistant.text)

                system_message = st.text_area("System instructions", assistant_attrs['instructions'], key="system_input")

                # **Garantindo que o modelo selecionado seja passado corretamente**
                model = st.selectbox("Model", ["gpt-4o","gpt-4o-mini","gpt-4.5-preview" ,"gpt-3.5-turbo"], key=assistant_attrs['model'])

                temperature = st.slider("Temperature", 0.0, 2.0, assistant_attrs['temperature'], key='temperature')
                top_p = st.slider("Top P",  0.0,1.0, assistant_attrs['top_p'], key = 'top_p')

                if st.button("Delete Assistant"): 
                    delete_assitant = requests.post(API_URL + f"assistants/{assistant_id}/delete", json={"user_email": st.session_state["email"]})
                    st.rerun()

        with col2:
            

            thread_list = ['thread_dYi0mgyjvOom6F4e5wT3mfSm']
            
            st.session_state['thread_id'] = st.selectbox("Threads", options= thread_list, index = None ,key="thread_select")

            if "thread_id"  in st.session_state: 
                try:
                    change_thread()
                except: 
                    pass
            

            chat_container = st.container(height=400)
            with chat_container:    
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
    
            if prompt := st.chat_input("Enter your message"):
            # Display user message in chat message container
                with chat_container:
                    st.chat_message("user").markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                if (system_message != assistant_attrs['instructions']) | (model != assistant_attrs['model'] )| (temperature != assistant_attrs['temperature']) | (top_p !=  assistant_attrs['top_p']):
                    
                    response = requests.post(API_URL + f"assistants/{assistant_id}/update", json ={'instructions':system_message,'temperature':temperature, top_p:'top_p','model':model})

                if "thread_id" not in st.session_state:
                    response = requests.post("http://127.0.0.1:8000/api/threads",json={"email": st.session_state["email"]})
                    st.session_state['thread_id'] = json.loads(response.text)['id']
            
                response = requests.post(API_URL + f'threads/{st.session_state['thread_id']}/messages', json = {"role":"user", "content":prompt})
                response = requests.post(API_URL + f'threads/{st.session_state['thread_id']}/{assistant_id}/run')
                
                chat_response = json.loads(response.text)
                response = chat_response['content']
                # Display assistant response in chat message container
                with chat_container:
                    st.chat_message(assistant_attrs['name']).markdown(response)
                # Add assistant response to chat history

                st.session_state.messages.append({"role": assistant_attrs['name'], "content": response})
            # text_uploaded_file = st.file_uploader("Adicione um arquivo ao seu prompt")
    elif page == "Criar Assistente":
        create_assistant_page()

    if st.button("Teste de API"):

        print(st.session_state)
        ''' criar assistente
        response = requests.post("http://127.0.0.1:8000/api/assistants", json={
        "id": "1",
        "name": "sub-criador",
        "instructions": "voce será o sub-criador de tudo",
        "model": "gpt-4o",
        "temperature": 1.0,
        "top_p": 1.0})
        '''
       
        #criar_thread = requests.post("http://127.0.0.1:8000/api/threads",json={"email": "rodrigoquaglio@hotmail.com"})
        messages_threads = requests.get(API_URL + f'threads/thread_dYi0mgyjvOom6F4e5wT3mfSm/messages')
        #todos_assistants = response = requests.get(API_URL + f'threads?email={st.session_state['email']}')
        ##criar_mensagem_na_thread = requests.post("http://127.0.0.1:8000/api/threads/thread_mHs4uDnlJ7XTBS96nZTyzO3i/messages",json={"role": "user", "content": "ola criador!"})
        #mandar_run = requests.post("http://127.0.0.1:8000/api/threads/thread_mHs4uDnlJ7XTBS96nZTyzO3i/asst_G8X32xNikCINLfqGhX6g1Gg4/run")
        
        st.write(messages_threads.json())
