from dotenv import load_dotenv
import streamlit as st

class AuthManager:
    def __init__(self):
        # Carregar variáveis de ambiente usando st.secrets em vez de .env
        self.admin_username = st.secrets["ADMIN_USERNAME"]
        self.admin_password = st.secrets["ADMIN_PASSWORD"]
        self.operator_username = st.secrets["OPERATOR_USERNAME"]
        self.operator_password = st.secrets["OPERATOR_PASSWORD"]

        # Se a senha do administrador não estiver definida, mostra um erro
        if not self.admin_password:
            raise ValueError("A variável de ambiente ADMIN_PASSWORD não foi carregada corretamente.")

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
