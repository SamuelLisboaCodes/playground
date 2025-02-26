import streamlit as st
import requests
API_URL = "http://127.0.0.1:8000/api/"  

def main():
    st.set_page_config(layout="wide", page_title="Playground - Assistants")
    
    # Estilos CSS customizados
    st.markdown(
        """
        <style>
            body {
                background-color: #121212;
                color: #ffffff;
            }
            .sidebar, .top-bar, .chat-container, .input-container, .right-panel {
                background: #1e1e1e;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
            }
            .input-container input {
                width: 100%;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
                border: none;
                background: #333;
                color: white;
            }
            .sidebar p, .right-panel p {
                color: #bbbbbb;
                cursor: pointer;
            }
            .sidebar p:hover, .right-panel p:hover {
                color: white;
            }
            .btn {
                background: #00a884;
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                border: none;
                cursor: pointer;
            }
            .btn:hover {
                background: #008f6b;
            }
            .centered {
                display: flex;
                justify-content: center;
                margin-top: 10px;
            }
            .stButton button {
                height: 42px; /* Altura do botão */
                margin-top: 25px; /* Ajuste fino para alinhar com a caixa de texto */
            }

            /* Estilo para o botão de limpar com o GIF */
            .clear-thread-button {
                background: white;
                border: none;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 40px;  /* Botão ajustado menor */
                height: 40px; /* Botão ajustado menor */
                border-radius: 20px; /* Bordas mais arredondadas */
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
                position: relative;
                overflow: hidden;
                transition: background 0.3s ease;
            }
            .clear-thread-button:hover {
                background: #f0f0f0;
            }

            /* GIF estático */
            .clear-thread-button::before {
                content: "";
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 25px;  /* Tamanho reduzido do GIF */
                height: 25px; /* Tamanho reduzido do GIF */
                background-image: url("https://i.imgur.com/RGbpEEE.gif"); /* GIF animado */
                background-size: cover;
                background-position: center;
                transition: opacity 0.3s ease;
            }

            /* Estilo para o slider com barra branca */
            input[type="range"] {
                -webkit-appearance: none;
                width: 100%;
                height: 8px;
                background: #ffffff; /* Barra branca */
                border-radius: 5px;
                outline: none;
            }

            /* Estilo para o "thumb" do slider */
            input[type="range"]::-webkit-slider-thumb {
                -webkit-appearance: none;
                appearance: none;
                width: 20px;
                height: 20px;
                border-radius: 50%;
                background: #00a884; /* Cor do "thumb" */
                cursor: pointer;
                transition: background 0.3s ease;
            }

            input[type="range"]::-moz-range-thumb {
                width: 20px;
                height: 20px;
                border-radius: 50%;
                background: #00a884; /* Cor do "thumb" */
                cursor: pointer;
                transition: background 0.3s ease;
            }

            /* Estilo para o "thumb" do slider no hover */
            input[type="range"]:hover::-webkit-slider-thumb {
                background: #008f6b;
            }

            input[type="range"]:hover::-moz-range-thumb {
                background: #008f6b;
            }

        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("# Playground")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.sidebar.button("Chat")
        st.sidebar.button("Realtime")
        st.sidebar.button("Assistants", disabled=True)
        st.sidebar.button("TTS")
        st.sidebar.markdown("---")
        st.sidebar.button("Cookbook")
        st.sidebar.button("Forum")
        st.sidebar.button("Help")
    
    with col2:
        st.markdown("Create Assistant")
        
        # Alterado para placeholder
        name = st.text_input("Name", placeholder="Ex: Assistant Name")

        # Alterado para placeholder
        system_message = st.text_area("System instructions", placeholder="Enter system instructions...")
        
        st.file_uploader("Upload file", type=["txt", "pdf", "json", "csv"])

        st.markdown("### MODEL CONFIGURATION")
        
        with st.container():
            st.markdown('<div class="model-config">', unsafe_allow_html=True)
            
            model = st.selectbox("Model", ["gpt-4o", "gpt-4", "gpt-3.5-turbo"])
            temperature = st.slider("Temperature", 0.0, 2.0, 1.0)
            max_tokens = st.slider("Max tokens", 1, 4096, 2048)
            top_p = st.slider("Top P", 0.0, 1.0, 1.0)


            st.markdown('<div class="save-preset-container">', unsafe_allow_html=True)
            if st.button("Save as preset"):
                payload = {"id": "0",
                "name": name,
                "instructions": system_message,
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p
            }

                response = requests.post(API_URL + 'assistants', json=payload)
                
                if response.status_code == 200:
                    st.success("Assistente criado com sucesso!")
                    
                else:
                    st.error(f"Erro ao criar assistente: {response.text}")


            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)


                
if __name__ == "__main__":
    main()
