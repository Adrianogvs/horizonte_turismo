# auth.py
import os
import streamlit as st
from dotenv import load_dotenv

class AuthManager:
    def __init__(self, env_file=".env"):
        load_dotenv(dotenv_path=env_file)
        self.admin_username = (os.getenv("ADMIN_USERNAME") or "").strip()
        self.admin_password = (os.getenv("ADMIN_PASSWORD") or "").strip()
        self.operator_username = (os.getenv("OPERATOR_USERNAME") or "").strip()
        self.operator_password = (os.getenv("OPERATOR_PASSWORD") or "").strip()

    def login(self):
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False

        if st.session_state.authenticated:
            return True

        st.title("Login")
        username_input = st.text_input("Usuário")
        password_input = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            # Verifica se é administrador
            if username_input == self.admin_username and password_input == self.admin_password:
                st.session_state.authenticated = True
                st.session_state.role = "admin"  # Papel: administrador
                st.success("Login realizado com sucesso como Administrador!")
            # Verifica se é operador
            elif username_input == self.operator_username and password_input == self.operator_password:
                st.session_state.authenticated = True
                st.session_state.role = "operator"  # Papel: operador
                st.success("Login realizado com sucesso como Operador!")
            else:
                st.error("Credenciais inválidas!")

        return st.session_state.authenticated