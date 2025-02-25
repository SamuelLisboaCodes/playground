import streamlit as st
import os
from dotenv import load_dotenv
from streamlit.components.v1 import html

# variáveis do .env
load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


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
        .login-box input {{
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #444;
            border-radius: 5px;
            background: #222;
            color: #fff;
        }}
        .login-box button {{
            width: 100%;
            padding: 12px;
            background: #008060;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
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

# header
st.markdown("""
    <div class='header'>
        <img src='https://img.icons8.com/pulsar-line/512/FFFFFF/chatgpt.png' alt='Logo'>
        <span>Playground AI</span>
    </div>
""", unsafe_allow_html=True)

# login
st.markdown(f"""
    <div class='login-container'>
        <div class='login-box'>
            <h2>Que bom que você voltou</h2>
            <input type='text' placeholder='Endereço de e-mail*'>
            <button>Continuar</button>
            <p>Não tem uma conta? <a href='#' style='color:#008060;'>Cadastrar</a></p>
            <div class='separator'>ou</div>
            <div class='google-login'>
                <a href="https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri=http://localhost:8501&scope=openid%20email%20profile" 
                target="_blank">
                    <button>
                        <img src="https://auth.openai.com/assets/google-logo-NePEveMl.svg" alt="Google Logo">
                        Log in with Google
                    </button>
                </a>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)
