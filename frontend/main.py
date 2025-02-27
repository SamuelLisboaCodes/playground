import streamlit as st
import time
from pages import openAI, login

@st.cache_data
def get_cached_user():
    return {"logged_in": False, "email": "", "auth_token": None}

def save_user_state(logged_in, email, auth_token):
    st.session_state["logged_in"] = logged_in
    st.session_state["email"] = email
    st.session_state["auth_token"] = auth_token

def initialize_session_state():
    if "logged_in" not in st.session_state:
        cached_user = get_cached_user()
        st.session_state["logged_in"] = cached_user["logged_in"]
        st.session_state["email"] = cached_user["email"]
        st.session_state["auth_token"] = cached_user["auth_token"]

def main():
    st.set_page_config(initial_sidebar_state="collapsed",layout="wide")
    initialize_session_state()

    time.sleep(0.1)

    if st.session_state["logged_in"]:
        openAI.openAI_page()
    else:
        login.login_page()

if __name__ == "__main__":
    main()
