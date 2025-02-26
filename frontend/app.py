import streamlit as st
from dotenv import load_dotenv
import openai
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API
openai.api_key = os.getenv("OPENAI_API_KEY")

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

    # Novo campo para escolher o assistente
    assistant = st.selectbox("Assistente", ["Escolha o Assistente", "Assistente 1", "Assistente 2", "Assistente 3"], key="assistant_select")

    # Campos de entrada
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
    st.file_uploader("Upload file", type=["txt", "pdf", "json", "csv"])

    # Botão "Run" centralizado
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    run_clicked = st.button("Run", key="run_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    # Processar a mensagem se o botão for clicado
    if run_clicked and name and system_message and user_input and assistant != "Escolha o Assistente":
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
        st.session_state.chat_history += f"**Assistente Selecionado:** {assistant}\n"
        st.session_state.chat_history += f"**Nome do Assistente:** {name}\n"
        st.session_state.chat_history += f"**Usuário:** {user_input}\n"
        st.session_state.chat_history += f"**Resposta do Assistente:** {result}"

        st.session_state.chat_history = st.session_state.chat_history.strip()
    elif run_clicked:
        st.error("Por favor, preencha todos os campos (Name, System instructions, Message e Assistente).")

    # Exibir histórico de chat
    chat_history = st.session_state.chat_history  
    st.text_area("Chat history", value=chat_history, height=300, key="chat_history_display", disabled=True)

if __name__ == "__main__":
    main()
