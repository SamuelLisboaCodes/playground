
import streamlit as st
import os
import requests
from dotenv import load_dotenv
load_dotenv()
if "auth_token" or "email" not in st.session_state:
    st.session_state["auth_token"] = None
    st.session_state["email"] = None
def main():

    

    # Captura o código OAuth do Google na URL
    query_params = st.query_params
    auth_code = query_params.get("code")


    print(st.session_state)

    if auth_code and not st.session_state["auth_token"]:
        st.info("Trocando código OAuth pelo token do Google...")

        response = requests.get(f"http://127.0.0.1:8000/auth/callback?code={auth_code}")

        if response.status_code == 200:
            token_data = response.json()
            st.session_state["auth_token"] = token_data["refresh_token"]
            st.session_state["email"] = token_data["email"]
            st.success("Login realizado com sucesso!")
            st.session_state["logged_in"] = True
            
            
        else:
            st.error("Falha ao obter o token do Google.")

    

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
                        <a href="https://accounts.google.com/o/oauth2/auth?client_id={os.getenv("GOOGLE_CLIENT_ID")}&redirect_uri={os.getenv("GOOGLE_REDIRECT_URI")}&response_type=code&scope=openid email profile" 
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
        st.navigation([st.Page("openAI.py")]).run()

        


if __name__ == "__main__":
    main()