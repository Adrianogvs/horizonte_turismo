import os
import streamlit as st
from dotenv import load_dotenv

class AuthManager:
    def __init__(self, env_file=".env"):
        """
        Carrega as variáveis do .env e remove espaços residuais.
        """
        load_dotenv(dotenv_path=env_file)
        self.username_env = (os.getenv("USERNAME") or "").strip()
        self.password_env = (os.getenv("PASSWORD") or "").strip()

    def login(self):
        """
        Exibe a tela de login (usuário/senha) SOMENTE se o usuário
        não estiver autenticado. Se já estiver, não mostra nada.
        Retorna True se autenticado.
        """
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False

        # Se já estiver autenticado, não mostra o formulário
        if st.session_state.authenticated:
            return True

        # Caso não esteja autenticado, exibe o formulário
        st.title("Login")
        username_input = st.text_input("Usuário")
        password_input = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if username_input == self.username_env and password_input == self.password_env:
                st.session_state.authenticated = True
                st.success("Login realizado com sucesso!")
                # Removemos o st.experimental_rerun() para evitar erro de fluxo
            else:
                st.error("Credenciais inválidas!")

        return st.session_state.authenticated
