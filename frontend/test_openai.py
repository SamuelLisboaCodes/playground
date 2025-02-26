import streamlit as st
from dotenv import load_dotenv
import openai
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para consultar o modelo OpenAI com base na entrada do usuário
def query_openai_model(model, system_message, user_message, role, temperature=1.0, max_tokens=150):
    prompt = system_message + "\n" + user_message
    
    # Usando a API de completions tradicional (versão 0.28.0)
    response = openai.Completion.create(  # Usando a versão antiga da API
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    return response.choices[0].text.strip()

def main():
    st.set_page_config(layout="wide", page_title="Playground - Assistants")
    
    st.markdown("# Playground")
    
    # Seção de Inputs
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Sidebar com botões de navegação
        st.sidebar.button("Chat")
        st.sidebar.button("Realtime")
        st.sidebar.button("Assistants", disabled=True)
        st.sidebar.button("TTS")
        st.sidebar.markdown("---")
        st.sidebar.button("Cookbook")
        st.sidebar.button("Forum")
        st.sidebar.button("Help")
    
    with col2:
        # Interface de interação com o modelo
        st.markdown("## Assistants")
        
        # Nome e instruções do sistema
        name = st.text_input("Name", placeholder="Ex: Assistant Name")
        system_message = st.text_area("System instructions", placeholder="Enter system instructions...")
        
        # Histórico de conversa
        st.markdown("### THREAD")
        chat_history = st.text_area("Chat history", height=300, key="chat_history")
        
        # Entradas do usuário
        user_message = st.text_input("Enter your message...")
        
        # Seleção do modelo e configurações
        st.markdown("### Model Configuration")
        model = st.selectbox("Model", ["gpt-4", "gpt-3.5-turbo"])
        temperature = st.slider("Temperature", 0.0, 2.0, 1.0)
        max_tokens = st.slider("Max tokens", 1, 4096, 2048)
        
        # Seletor de "role" (System ou User)
        role = st.selectbox("Role", ["system", "user"], index=1)

        # Botão de envio
        if st.button("Run", key="run_btn"):
            with st.spinner("Consultando a OpenAI..."):
                result = query_openai_model(
                    model=model, 
                    system_message=system_message, 
                    user_message=user_message,
                    role=role,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                st.success("Resposta recebida!")
                st.write(f"Resposta: {result}")
        
        # Upload de arquivo (opcional)
        uploaded_file = st.file_uploader("Upload file", type=["txt", "pdf", "json", "csv"])
        if uploaded_file:
            st.write(f"Arquivo {uploaded_file.name} carregado.")

if __name__ == "__main__":
    main()
