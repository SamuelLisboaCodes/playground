import requests.cookies
import streamlit as st
import requests



FASTAPI_URL = "http://127.0.0.1:8000"

token = st.query_params.get("token", None)

# Interface
st.markdown("<h1 style='text-align: center;'>🔐 Login com Google</h1>", unsafe_allow_html=True)
st.write("Seja bem-vindo! Faça login com sua conta Google para continuar.")

# Obtendo informações do usuário
response = requests.get(f"{FASTAPI_URL}/auth/session-user")
print(response.cookies)
if response.status_code == 200:
    user_info = response.json()
    st.json(user_info)
else:
    st.error("Erro ao obter informações do usuário.")
    
login_url = f"{FASTAPI_URL}/auth/login"
st.markdown(f'<a href="{login_url}" target="_self"><button>Login com Google</button></a>', unsafe_allow_html=True)