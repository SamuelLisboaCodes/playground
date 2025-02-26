import streamlit as st
import os
import requests
from dotenv import load_dotenv

# variáveis do .env
load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8501" 


if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None

# Captura o código OAuth do Google na URL
query_params = st.query_params
auth_code = query_params.get("code")

if auth_code and not st.session_state["auth_token"]:
    st.info("Trocando código OAuth pelo token do Google...")

    # Trocar código OAuth pelo token do Google
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": auth_code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        token_data = response.json()
        st.session_state["auth_token"] = token_data["id_token"]  # O JWT do Google
        st.success("Login realizado com sucesso!")
        st.experimental_rerun()
    else:
        st.error("Falha ao obter o token do Google.")

st.set_page_config(page_title="Login", page_icon="🔑", layout="wide")

# CSS página
st.markdown(
    f"""
    <style>
        body {{
            background-color: #212121;
            color: #F7F7F8;
            font-family: Arial, sans-serif;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            flex-direction: column;
        }}
        .header {{
            width: 100%;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            justify-content: left;
        }}
        .header img {{
            width: 40px;
            margin-right: 10px;
        }}
        .header span {{
            color: white;
            font-size: 22px;
            font-weight: bold;
        }}
        .login-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            flex-grow: 1;
        }}
        .login-box {{
            background: #303030;
            padding: 40px;
            border-radius: 10px;
            width: 400px;
            text-align: center;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        }}
        .login-box h2 {{
            font-size: 24px;
            margin-bottom: 20px;
        }}
        .separator {{
            display: flex;
            align-items: center;
            text-align: center;
            margin: 20px 0;
        }}
        .separator::before,
        .separator::after {{
            content: '';
            flex: 1;
            border-bottom: 1px solid #444;
        }}
        .separator:not(:empty)::before {{
            margin-right: .5em;
        }}
        .separator:not(:empty)::after {{
            margin-left: .5em;
        }}
        .google-login button {{
            width: 100%;
            padding: 10px;
            background: #303030;
            color: white;
            border: 1px solid #444;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .google-login img {{
            width: 20px;
            margin-right: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown("""
    <div class='header'>
        <img src='https://img.icons8.com/pulsar-line/512/FFFFFF/chatgpt.png' alt='Logo'>
        <span>Playground AI</span>
    </div>
""", unsafe_allow_html=True)


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

# Se autenticado, exibir mensagem e token
else:
    st.success("Login bem-sucedido!")
    st.write("Token JWT do Google:", st.session_state["auth_token"])

  
    BACKEND_URL = "http://localhost:8000"
    headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}
    response = requests.get(f"{BACKEND_URL}/dados", headers=headers)

    if response.status_code == 200:
        st.write("Dados do backend:", response.json())
    else:
        st.error("Acesso negado")
