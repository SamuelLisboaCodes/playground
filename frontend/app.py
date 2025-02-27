import streamlit as st
from dotenv import load_dotenv
import json
import openai
import os
import requests

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API
API_URL = "http://127.0.0.1:8000/api/"  
#%%


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

    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("### Configuração do Assistente")
        response = requests.get(API_URL + 'assistants')
        dict_assistentes = json.loads(response.text)
        id_assistentes = [ass['id'] for ass in dict_assistentes]
        id_to_name = lambda id_procurado: next((a["name"] for a in dict_assistentes if a["id"] == id_procurado),  "Não encontrado")

        assistant_id = st.selectbox("Assistente", id_assistentes, format_func = id_to_name, key="assistant_select")

        assistant = requests.get( API_URL + 'assistants/' + assistant_id + '/retrieve')
        assistant_attrs = json.loads(assistant.text)
    
        system_message = st.text_area("System instructions", assistant_attrs['instructions'], key="system_input")

        # **Garantindo que o modelo selecionado seja passado corretamente**
        model = st.selectbox("Model", ["gpt-4", "gpt-3.5-turbo"], key=assistant_attrs['model'])

        temperature = st.slider("Temperature", 0.0, 2.0, assistant_attrs['temperature'], key='temperature')
        top_p = st.slider("Top P",  0.0,1.0, assistant_attrs['top_p'], key = 'top_p')


    with col2:
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if prompt := st.chat_input("Enter your message"):
        # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            if (system_message != assistant_attrs['instructions']) | (model != assistant_attrs['model'] )| (temperature != assistant_attrs['temperature']) | (top_p !=  assistant_attrs['top_p']):
                response = requests.post(API_URL + f"assistants/{assistant_id}/update?instructions={system_message}&temperature={temperature}&top_p={top_p}&model={model}")
            
            if not thread_id: 
                response = requests.post(API_URL + 'threads?assistant_id='+ assistant_id)
                thread_id = json.loads(response.text)['id']
        
            response = requests.post(API_URL + f'threads/{thread_id}/messages?role=user&content={prompt}')
            response = requests.post(API_URL + f'threads/{thread_id}/run?assistant_id={assistant_id}')
            
            chat_response = json.loads(response.text)
            response = chat_response['content']
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history

            st.session_state.messages.append({"role": "assistant", "content": response})

        # Upload de arquivo abaixo da caixa de texto
        st.file_uploader("Upload file", type=["txt", "pdf", "json", "csv"])



if __name__ == "__main__":
    main()