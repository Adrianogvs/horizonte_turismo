import streamlit as st
import pandas as pd
import altair as alt
from loguru import logger
import sys
import os
from io import BytesIO

# Função para limpar campos do st.session_state
def limpar_campos(campos):
    for campo in campos:
        if campo in st.session_state:
            del st.session_state[campo]

# Garante a pasta de logs
os.makedirs("logs", exist_ok=True)

# Configuração do Logger
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("logs/app_log_{time}.log", level="INFO")

# Imports internos – ajuste os caminhos conforme sua estrutura de pastas
from src.auth.auth import AuthManager
from src.database.db_manager import DBManager
from src.utils.cep import consulta_cep

# Função para exportar DataFrame para Excel em bytes (correção aplicada)
def to_excel_bytes(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data

logger.info("Iniciando a aplicação Streamlit")

# -----------------------------
# FUNÇÕES DE CADASTRO SIMPLES
# -----------------------------
def cadastro_carros(db: DBManager):
    st.subheader("Gerenciar Carros")
    user_name = st.session_state.get("user_name", "Desconhecido")

    novo_carro = st.text_input("Adicionar novo Carro", key="carro_input")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Adicionar Carro", key="botao_adicionar_carro"):
            db.inserir_carro(novo_carro)
            st.success("Carro adicionado com sucesso!")
            logger.info(f"[CADASTRO] Carro adicionado: '{novo_carro}' por {user_name}")
    with col2:
        if st.button("Limpar Campos", key="botao_limpar_carro"):
            limpar_campos(["carro_input"])

    df_carros = db.obter_carros()
    st.dataframe(df_carros)

    excluir_id = st.number_input("ID do Carro para excluir", min_value=1, step=1, key="carro_excluir")
    if st.button("Excluir Carro", key="botao_excluir_carro"):
        db.excluir_registro("carros", excluir_id)
        st.success("Carro excluído com sucesso!")
        logger.info(f"[EXCLUSAO] Carro excluído (ID={excluir_id}) por {user_name}")

def cadastro_motoristas(db: DBManager):
    st.subheader("Gerenciar Motoristas")
    user_name = st.session_state.get("user_name", "Desconhecido")

    novo_motorista = st.text_input("Adicionar novo Motorista", key="motorista_input")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Adicionar Motorista", key="botao_adicionar_motorista"):
            db.inserir_motorista(novo_motorista)
            st.success("Motorista adicionado com sucesso!")
            logger.info(f"[CADASTRO] Motorista adicionado: '{novo_motorista}' por {user_name}")
    with col2:
        if st.button("Limpar Campos", key="botao_limpar_motorista"):
            limpar_campos(["motorista_input"])

    df_mot = db.obter_motoristas()
    st.dataframe(df_mot)

    excluir_id = st.number_input("ID do Motorista para excluir", min_value=1, step=1, key="motorista_excluir")
    if st.button("Excluir Motorista", key="botao_excluir_motorista"):
        db.excluir_registro("motoristas", excluir_id)
        st.success("Motorista excluído com sucesso!")
        logger.info(f"[EXCLUSAO] Motorista excluído (ID={excluir_id}) por {user_name}")

def cadastro_tipos_oleo(db: DBManager):
    st.subheader("Gerenciar Tipos de Óleo")
    user_name = st.session_state.get("user_name", "Desconhecido")

    novo_oleo = st.text_input("Adicionar novo Tipo de Óleo", key="oleo_input")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Adicionar Óleo", key="botao_adicionar_oleo"):
            db.inserir_tipo_oleo(novo_oleo)
            st.success("Óleo adicionado com sucesso!")
            logger.info(f"[CADASTRO] Óleo adicionado: '{novo_oleo}' por {user_name}")
    with col2:
        if st.button("Limpar Campos", key="botao_limpar_oleo"):
            limpar_campos(["oleo_input"])

    df_oleo = db.obter_tipos_oleo()
    st.dataframe(df_oleo)

    excluir_id = st.number_input("ID do Óleo para excluir", min_value=1, step=1, key="oleo_excluir")
    if st.button("Excluir Óleo", key="botao_excluir_oleo"):
        db.excluir_registro("tipos_oleo", excluir_id)
        st.success("Óleo excluído com sucesso!")
        logger.info(f"[EXCLUSAO] Óleo excluído (ID={excluir_id}) por {user_name}")

# -----------------------------
# FUNÇÕES DE CADASTRO DE ENDEREÇO
# -----------------------------
def cadastro_origem(db: DBManager):
    st.subheader("Cadastro de Origem (Endereço)")
    user_name = st.session_state.get("user_name", "Desconhecido")

    cep_input = st.text_input("Informe o CEP", key="origem_cep_input")
    endereco_info = None
    if cep_input:
        endereco_info = consulta_cep(cep_input)
        if endereco_info:
            st.write("Endereço encontrado:")
            st.json(endereco_info)
        else:
            st.error("CEP não encontrado ou inválido.")

    numero = st.text_input("Digite o número do endereço", key="origem_numero_input")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Salvar Origem", key="botao_salvar_origem"):
            if endereco_info and numero:
                cep = endereco_info.get("cep", "")
                logradouro = endereco_info.get("logradouro", "")
                complemento = endereco_info.get("complemento", "")
                bairro = endereco_info.get("bairro", "")
                localidade = endereco_info.get("localidade", "")
                uf = endereco_info.get("uf", "")
                endereco_id = db.inserir_endereco(cep, logradouro, complemento, bairro, localidade, uf, numero)
                origem_id = db.inserir_origem(endereco_id)
                st.success("Origem cadastrada com sucesso!")
                logger.info(f"[CADASTRO] Origem cadastrada: CEP={cep}, Logradouro='{logradouro}', Número='{numero}', ID_Origem={origem_id} por {user_name}")
            else:
                st.error("Informe um CEP válido e digite o número do endereço.")
    with col2:
        if st.button("Limpar Campos", key="botao_limpar_origem"):
            limpar_campos(["origem_cep_input", "origem_numero_input"])

def cadastro_destino(db: DBManager):
    st.subheader("Cadastro de Destino (Endereço)")
    user_name = st.session_state.get("user_name", "Desconhecido")

    cep_input = st.text_input("Informe o CEP", key="destino_cep_input")
    endereco_info = None
    if cep_input:
        endereco_info = consulta_cep(cep_input)
        if endereco_info:
            st.write("Endereço encontrado:")
            st.json(endereco_info)
        else:
            st.error("CEP não encontrado ou inválido.")

    numero = st.text_input("Digite o número do endereço", key="destino_numero_input")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Salvar Destino", key="botao_salvar_destino"):
            if endereco_info and numero:
                cep = endereco_info.get("cep", "")
                logradouro = endereco_info.get("logradouro", "")
                complemento = endereco_info.get("complemento", "")
                bairro = endereco_info.get("bairro", "")
                localidade = endereco_info.get("localidade", "")
                uf = endereco_info.get("uf", "")
                endereco_id = db.inserir_endereco(cep, logradouro, complemento, bairro, localidade, uf, numero)
                destino_id = db.inserir_destino(endereco_id)
                st.success("Destino cadastrado com sucesso!")
                logger.info(f"[CADASTRO] Destino cadastrado: CEP={cep}, Logradouro='{logradouro}', Número='{numero}', ID_Destino={destino_id} por {user_name}")
            else:
                st.error("Informe um CEP válido e digite o número do endereço.")
    with col2:
        if st.button("Limpar Campos", key="botao_limpar_destino"):
            limpar_campos(["destino_cep_input", "destino_numero_input"])

# -----------------------------
# FUNÇÃO PRINCIPAL
# -----------------------------
def main_app():
    db = DBManager()

    st.sidebar.title("Menu")
    if st.sidebar.button("Logout", key="botao_logout"):
        st.session_state.authenticated = False
        st.experimental_rerun()
        logger.info("Usuário fez logout.")

    st.title("📌 Sistema de Gestão de Viagem - Horizonte Turismo")

    # Define a variável user_role no escopo desta função
    user_role = st.session_state.get("role", "operator")
    logger.info(f"Usuário com papel {user_role} acessando a aplicação.")

    if user_role == "admin":
        aba_principal, aba_tabela, aba_grafico, aba_cadastros = st.tabs([
            "Cadastro de Viagem",
            "Tabela de Viagens",
            "Gráfico de Viagens",
            "Cadastros"
        ])
    else:
        aba_principal = st.tabs(["Cadastro de Viagem"])[0]

    # Aba 1: Cadastro de Viagem
    with aba_principal:
        st.subheader("Cadastro de Nova Viagem")
        user_name = st.session_state.get("user_name", "Desconhecido")

        # Carrega origens e destinos
        origens = db.obter_origens()
        destinos = db.obter_destinos()

        opcoes_origem = [
            f"{o['cep']} {o['logradouro']} {o['complemento']} {o['bairro']} {o['localidade']} {o['uf']} {o['numero']}"
            for o in origens
        ]
        opcoes_destino = [
            f"{d['cep']} {d['logradouro']} {d['complemento']} {d['bairro']} {d['localidade']} {d['uf']} {d['numero']}"
            for d in destinos
        ]

        tem_origem = len(opcoes_origem) > 0
        tem_destino = len(opcoes_destino) > 0

        if not tem_origem:
            st.warning("Nenhuma origem cadastrada. Cadastre uma origem antes de registrar viagens.")
        if not tem_destino:
            st.warning("Nenhum destino cadastrado. Cadastre um destino antes de registrar viagens.")

        origem_escolhida = st.selectbox(
            "Selecione a Origem",
            opcoes_origem if tem_origem else ["(Nenhuma origem disponível)"],
            disabled=(not tem_origem),
            key="viagem_cadastro_origem"
        )
        destino_escolhida = st.selectbox(
            "Selecione o Destino",
            opcoes_destino if tem_destino else ["(Nenhum destino disponível)"],
            disabled=(not tem_destino),
            key="viagem_cadastro_destino"
        )

        if tem_origem:
            origem_idx = opcoes_origem.index(origem_escolhida)
            origem_id = origens[origem_idx]["origem_id"]
        else:
            origem_id = None

        if tem_destino:
            destino_idx = opcoes_destino.index(destino_escolhida)
            destino_id = destinos[destino_idx]["destino_id"]
        else:
            destino_id = None

        row1 = st.columns(2)
        with row1[0]:
            carros = db.obter_carros()
            carro = st.selectbox("Carro", carros["nome"].tolist(), key="viagem_select_carro")
        with row1[1]:
            motoristas = db.obter_motoristas()
            motorista = st.selectbox("Motorista", motoristas["nome"].tolist(), key="viagem_select_motorista")

        row2 = st.columns(3)
        with row2[0]:
            km_saida = st.number_input("KM Saída", min_value=0.0, format="%.2f", key="viagem_km_saida")
        with row2[1]:
            km_chegada = st.number_input("KM Chegada", min_value=0.0, format="%.2f", key="viagem_km_chegada")
        with row2[2]:
            calculated_total_km = max(0.0, km_chegada - km_saida)
            st.number_input("Total KM", value=calculated_total_km, format="%.2f", key="viagem_total_km", disabled=True)

        row3 = st.columns(3)
        with row3[0]:
            data_saida = st.date_input("Data da Saída", key="viagem_data_saida").strftime("%Y-%m-%d")
        with row3[1]:
            data_volta = st.date_input("Data da Volta", key="viagem_data_volta").strftime("%Y-%m-%d")
        with row3[2]:
            pedagio = st.number_input("Pedágio", min_value=0.0, format="%.2f", key="viagem_pedagio")

        row4 = st.columns(3)
        with row4[0]:
            diesel_s10 = st.number_input("Diesel S10", min_value=0.0, format="%.2f", key="viagem_diesel_s10")
        with row4[1]:
            diesel_s500 = st.number_input("Diesel S500", min_value=0.0, format="%.2f", key="viagem_diesel_s500")
        with row4[2]:
            litros = diesel_s10 + diesel_s500
            st.number_input("Litros", min_value=0.0, format="%.2f", key="viagem_litros", value=litros, disabled=True)

        row5 = st.columns(3)
        with row5[0]:
            valor = st.number_input("Valor (Preço por Litro)", min_value=0.0, format="%.2f", key="viagem_valor")
        with row5[1]:
            despesa_extra = st.number_input("Despesa Extra", min_value=0.0, format="%.2f", key="viagem_despesa_extra")
        with row5[2]:
            computed_valor_combustivel = litros * valor
            st.number_input("Valor Combustível", value=computed_valor_combustivel, format="%.2f",
                            key="viagem_valor_combustivel", disabled=True)

        row6 = st.columns(2)
        with row6[0]:
            diaria_motorista = st.number_input("Diária Motorista", min_value=0.0, format="%.2f", key="viagem_diaria_motorista")
        with row6[1]:
            # Atualize o cálculo para incluir o Pedágio
            computed_valor_total = computed_valor_combustivel + despesa_extra + diaria_motorista + pedagio
            st.number_input("Valor Total", value=computed_valor_total, format="%.2f",
                            key="viagem_valor_total", disabled=True)

        # Habilita o botão somente se houver origem e destino
        can_save = (origem_id is not None) and (destino_id is not None)

        col_salvar, col_limpar = st.columns(2)
        with col_salvar:
            if st.button("Salvar Viagem", key="botao_salvar_viagem", disabled=(not can_save)):
                dados = (
                    origem_id, destino_id, carro,
                    km_saida, km_chegada, calculated_total_km,
                    data_saida, data_volta, valor,
                    motorista, diaria_motorista, despesa_extra,
                    diesel_s10, diesel_s500, litros,
                    computed_valor_combustivel, pedagio, computed_valor_total
                )
                db.inserir_viagem(*dados)
                st.success("Viagem registrada com sucesso!")
                logger.info(
                    f"[CADASTRO] Viagem registrada por {user_name}. "
                    f"OrigemID={origem_id}, DestinoID={destino_id}, Carro='{carro}', Motorista='{motorista}', "
                    f"KM_Saída={km_saida}, KM_Chegada={km_chegada}, Valor={valor}, "
                    f"Diária={diaria_motorista}, DespesaExtra={despesa_extra}, DieselS10={diesel_s10}, DieselS500={diesel_s500}, "
                    f"Litros={litros}, ValorComb={computed_valor_combustivel}, Pedágio={pedagio}, ValorTotal={computed_valor_total}"
                )
        with col_limpar:
            if st.button("Limpar Campos", key="botao_limpar_viagem"):
                limpar_campos([
                    "viagem_select_carro", "viagem_select_motorista",
                    "viagem_km_saida", "viagem_km_chegada", "viagem_total_km",
                    "viagem_data_saida", "viagem_data_volta", "viagem_pedagio",
                    "viagem_diesel_s10", "viagem_diesel_s500", "viagem_litros",
                    "viagem_valor", "viagem_despesa_extra", "viagem_valor_combustivel",
                    "viagem_diaria_motorista", "viagem_valor_total"
                ])

    # Aba 2: Tabela de Viagens (somente para admin)
    if user_role == "admin":
        with aba_tabela:
            st.subheader("📋 Viagens Registradas")

            # Carrega o DataFrame completo do banco de dados
            df_viagens = db.obter_viagens_completo()

            if not df_viagens.empty:
                # 1) Converter colunas relevantes para numérico
                numeric_cols = [
                    "Total de KM",
                    "Valor Total da Viagem",
                    "Valor do Combustível",
                    "Valor do Pedágio",
                    "Despesas Extras",
                    "Diária do Motorista"
                ]
                for col in numeric_cols:
                    if col in df_viagens.columns:
                        df_viagens[col] = pd.to_numeric(df_viagens[col], errors="coerce")

                # 2) Converter a coluna "Data de Saída" para datetime
                if "Data de Saída" in df_viagens.columns:
                    df_viagens["Data de Saída"] = pd.to_datetime(df_viagens["Data de Saída"], errors="coerce")

                # Atualiza o campo "Valor Total da Viagem" para incluir o Pedágio
                if all(col in df_viagens.columns for col in ["Valor do Combustível", "Valor do Pedágio", "Despesas Extras", "Diária do Motorista"]):
                    df_viagens["Valor Total da Viagem"] = (
                        df_viagens["Valor do Combustível"] +
                        df_viagens["Valor do Pedágio"] +
                        df_viagens["Despesas Extras"] +
                        df_viagens["Diária do Motorista"]
                    )

                # 3) Criar filtros (Ano, Mês, Origem, Destino, Motorista)
                col1, col2, col3, col4, col5 = st.columns(5)

                with col1:
                    anos = sorted(df_viagens["Data de Saída"].dt.year.dropna().unique().tolist())
                    anos_str = [str(a) for a in anos]
                    selected_ano = st.selectbox("Ano", ["Todos"] + anos_str, index=0, key="tabela_filtro_ano")

                with col2:
                    meses = sorted(df_viagens["Data de Saída"].dt.month.dropna().unique().tolist())
                    meses_str = [str(m) for m in meses]
                    selected_mes = st.selectbox("Mês", ["Todos"] + meses_str, index=0, key="tabela_filtro_mes")

                with col3:
                    origens_list = sorted(df_viagens["Endereço de Origem"].dropna().unique().tolist())
                    selected_origem = st.selectbox("Origem", ["Todos"] + origens_list, index=0, key="tabela_filtro_origem")

                with col4:
                    destinos_list = sorted(df_viagens["Endereço de Destino"].dropna().unique().tolist())
                    selected_destino = st.selectbox("Destino", ["Todos"] + destinos_list, index=0, key="tabela_filtro_destino")

                with col5:
                    motoristas_list = sorted(df_viagens["Motorista"].dropna().unique().tolist())
                    selected_motorista = st.selectbox("Motorista", ["Todos"] + motoristas_list, index=0, key="tabela_filtro_motorista")

                # 4) Aplicar os filtros ao DataFrame
                df_filtrado = df_viagens.copy()
                if selected_ano != "Todos":
                    df_filtrado = df_filtrado[df_filtrado["Data de Saída"].dt.year == int(selected_ano)]
                if selected_mes != "Todos":
                    df_filtrado = df_filtrado[df_filtrado["Data de Saída"].dt.month == int(selected_mes)]
                if selected_origem != "Todos":
                    df_filtrado = df_filtrado[df_filtrado["Endereço de Origem"] == selected_origem]
                if selected_destino != "Todos":
                    df_filtrado = df_filtrado[df_filtrado["Endereço de Destino"] == selected_destino]
                if selected_motorista != "Todos":
                    df_filtrado = df_filtrado[df_filtrado["Motorista"] == selected_motorista]

                # 5) Calcular subtotais
                subtotal_total_km = df_filtrado["Total de KM"].sum()
                subtotal_valor_total = df_filtrado["Valor Total da Viagem"].sum()
                subtotal_valor_combustivel = df_filtrado["Valor do Combustível"].sum()
                subtotal_pedagio = df_filtrado["Valor do Pedágio"].sum()
                subtotal_despesa_extra = df_filtrado["Despesas Extras"].sum()
                subtotal_diaria = df_filtrado["Diária do Motorista"].sum()

                # 6) Exibir subtotais
                st.markdown("### Subtotais")
                st.write(f"**Total KM:** {subtotal_total_km:,.2f}")
                st.write(f"**Valor Total:** {subtotal_valor_total:,.2f}")
                st.write(f"**Valor Combustível:** {subtotal_valor_combustivel:,.2f}")
                st.write(f"**Pedágio:** {subtotal_pedagio:,.2f}")
                st.write(f"**Despesa Extra:** {subtotal_despesa_extra:,.2f}")
                st.write(f"**Diária do Motorista:** {subtotal_diaria:,.2f}")

                # 7) Exportar o DataFrame filtrado para Excel
                excel_data = to_excel_bytes(df_filtrado)
                st.download_button(
                    label="Exportar para Excel",
                    data=excel_data,
                    file_name="viagens_com_enderecos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="tabela_botao_exportar_excel"
                )

                # 8) Ajustar a exibição da coluna Data de Saída (somente a data, sem hora)
                df_filtrado["Data de Saída"] = df_filtrado["Data de Saída"].dt.date

                # 9) Exibir o DataFrame filtrado
                st.dataframe(df_filtrado)

            else:
                st.info("Nenhuma viagem registrada ainda.")

    # Aba 3: Gráficos de Viagens
    with aba_grafico:
        st.subheader("📊 Gráficos de Viagens")
        df_viagens = db.obter_viagens_completo()
        if not df_viagens.empty:
            # Garantir que a coluna de data seja do tipo datetime
            df_viagens["Data de Saída"] = pd.to_datetime(df_viagens["Data de Saída"], errors="coerce")
            
            # Cria seis abas para os gráficos
            grafico_tab1, grafico_tab2, grafico_tab3, grafico_tab4, grafico_tab5, grafico_tab6 = st.tabs([
                "Total KM & Custos por Data",
                "Distribuição dos Custos",
                "Valor Total x Total KM",
                "Histograma de Total KM",
                "Evolução dos Custos",
                "Previsão de Viagens Futuras"
            ])
            
            # Gráfico 1: Linha para Total KM, Valor Total e Valor do Combustível por Data
            with grafico_tab1:
                df_grouped = df_viagens.groupby("Data de Saída", as_index=False).agg({
                    "Total de KM": "sum",
                    "Valor Total da Viagem": "sum",
                    "Valor do Combustível": "sum"
                })
                # Reestruturar os dados para plotagem
                df_melted = df_grouped.melt(
                    id_vars="Data de Saída", 
                    value_vars=["Total de KM", "Valor Total da Viagem", "Valor do Combustível"],
                    var_name="Métrica", 
                    value_name="Valor"
                )
                chart1 = alt.Chart(df_melted).mark_line(point=True).encode(
                    x=alt.X("Data de Saída:T", title="Data"),
                    y=alt.Y("Valor:Q", title="Valor / KM"),
                    color=alt.Color("Métrica:N"),
                    tooltip=["Data de Saída:T", "Métrica:N", "Valor:Q"]
                ).properties(
                    title="Evolução Diária: Total KM, Valor Total e Valor do Combustível",
                    width=700,
                    height=400
                )
                st.altair_chart(chart1, use_container_width=True)
                st.write("Este gráfico mostra a evolução diária do Total de KM percorridos, do Valor Total das viagens e do Valor do Combustível, permitindo identificar tendências e sazonalidades.")
            
            # Gráfico 2: Distribuição dos Custos (pizza)
            with grafico_tab2:
                custos = pd.DataFrame({
                    "Categoria": ["Pedágio", "Despesa Extra", "Diária do Motorista", "Valor do Combustível"],
                    "Valor": [
                        df_viagens["Valor do Pedágio"].sum(),
                        df_viagens["Despesas Extras"].sum(),
                        df_viagens["Diária do Motorista"].sum(),
                        df_viagens["Valor do Combustível"].sum()
                    ]
                })
                custos["Percentual"] = (custos["Valor"] / custos["Valor"].sum()) * 100
                chart2 = alt.Chart(custos).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta(field="Valor", type="quantitative"),
                    color=alt.Color(field="Categoria", type="nominal"),
                    tooltip=[alt.Tooltip("Categoria:N"), alt.Tooltip("Valor:Q"), alt.Tooltip("Percentual:Q")]
                ).properties(
                    title="Distribuição Percentual dos Custos",
                    width=400,
                    height=400
                )
                st.altair_chart(chart2, use_container_width=True)
                st.write("Este gráfico analisa a distribuição percentual dos custos das viagens, evidenciando onde os recursos estão sendo mais consumidos.")
            
            # Gráfico 3: Dispersão entre Total KM e Valor Total com bubble size representando Valor do Combustível
            with grafico_tab3:
                chart3 = alt.Chart(df_viagens).mark_circle().encode(
                    x=alt.X("Total de KM:Q", title="Total KM"),
                    y=alt.Y("Valor Total da Viagem:Q", title="Valor Total"),
                    size=alt.Size("Valor do Combustível:Q", title="Valor do Combustível"),
                    color=alt.Color("Endereço de Origem:N", title="Origem"),
                    tooltip=["Endereço de Origem", "Endereço de Destino", "Total de KM", "Valor Total da Viagem", "Valor do Combustível"]
                ).properties(
                    title="Relação: Total KM x Valor Total (tamanho = Valor do Combustível)",
                    width=700,
                    height=400
                ).interactive()
                st.altair_chart(chart3, use_container_width=True)
                st.write("Este gráfico de dispersão relaciona o Total de KM com o Valor Total das viagens, utilizando o tamanho dos pontos para indicar o Valor do Combustível, o que pode revelar oportunidades de melhoria e eficiência operacional.")
            
            # Gráfico 4: Histograma do Total de KM
            with grafico_tab4:
                chart4 = alt.Chart(df_viagens).mark_bar().encode(
                    alt.X("Total de KM:Q", bin=alt.Bin(maxbins=20), title="Intervalos de Total KM"),
                    y=alt.Y("count():Q", title="Número de Viagens"),
                    color=alt.Color("Total de KM:Q", scale=alt.Scale(scheme='greens'))
                ).properties(
                    title="Distribuição do Total de KM por Viagem",
                    width=700,
                    height=400
                )
                st.altair_chart(chart4, use_container_width=True)
                st.write("Este histograma mostra como as viagens se distribuem em relação à distância percorrida, destacando os intervalos mais comuns.")
            
            # Gráfico 5: Evolução dos Custos de Viagem (área empilhada)
            with grafico_tab5:
                df_costos = df_viagens.groupby("Data de Saída")[
                    ["Valor do Pedágio", "Despesas Extras", "Diária do Motorista", "Valor do Combustível"]
                ].sum().reset_index()
                chart5 = alt.Chart(df_costos).mark_area().encode(
                    x=alt.X('Data de Saída:T', title="Data"),
                    y=alt.Y('value:Q', stack='zero', title="Custo Total"),
                    color=alt.Color('variable:N', title="Categoria de Custo"),
                    tooltip=["Data de Saída:T", "variable:N", "value:Q"]
                ).transform_fold(
                    ['Valor do Pedágio', 'Despesas Extras', 'Diária do Motorista', 'Valor do Combustível'],
                    as_=['variable', 'value']
                ).properties(
                    title="Evolução dos Custos das Viagens ao Longo do Tempo",
                    width=800,
                    height=400
                )
                st.altair_chart(chart5, use_container_width=True)
                st.write("O gráfico de área empilhada ilustra a evolução dos diferentes custos das viagens ao longo do tempo, possibilitando identificar tendências e sazonalidades em cada categoria.")
            
            # Gráfico 6: Previsão de Viagens Futuras com Regressão Linear Simples
            with grafico_tab6:
                import numpy as np
                import datetime
                
                # Agrupa por data e conta o número de viagens
                df_grouped = df_viagens.groupby("Data de Saída").size().reset_index(name="NumViagens")
                df_grouped = df_grouped.sort_values("Data de Saída")
                
                # Converte a data para um número ordinal para ajuste de regressão
                df_grouped["date_ord"] = df_grouped["Data de Saída"].apply(lambda d: d.toordinal())
                
                # Se houver dados suficientes, ajusta uma regressão linear
                if len(df_grouped) >= 2:
                    coef = np.polyfit(df_grouped["date_ord"], df_grouped["NumViagens"], 1)
                    poly_model = np.poly1d(coef)
                    
                    # Gera datas futuras para os próximos 30 dias
                    max_date = df_grouped["Data de Saída"].max()
                    future_dates = [max_date + datetime.timedelta(days=i) for i in range(1, 31)]
                    future_ord = [d.toordinal() for d in future_dates]
                    future_predictions = poly_model(future_ord)
                    
                    df_forecast = pd.DataFrame({
                        "Data": future_dates,
                        "Previsao": future_predictions
                    })
                    
                    # Dados históricos para comparação
                    df_grouped_hist = df_grouped.rename(columns={"Data de Saída": "Data", "NumViagens": "Histórico"})
                    
                    line_hist = alt.Chart(df_grouped_hist).mark_line(color="blue").encode(
                        x=alt.X("Data:T", title="Data"),
                        y=alt.Y("Histórico:Q", title="Número de Viagens"),
                        tooltip=["Data:T", "Histórico:Q"]
                    )
                    line_forecast = alt.Chart(df_forecast).mark_line(color="red", strokeDash=[5,5]).encode(
                        x=alt.X("Data:T", title="Data"),
                        y=alt.Y("Previsao:Q", title="Número de Viagens"),
                        tooltip=["Data:T", "Previsao:Q"]
                    )
                    combined_chart = alt.layer(line_hist, line_forecast).properties(
                        title="Previsão de Número de Viagens Futuras (Próximos 30 dias)",
                        width=800,
                        height=400
                    )
                    st.altair_chart(combined_chart, use_container_width=True)
                    st.write("Este gráfico mostra a tendência histórica do número de viagens (linha azul) e uma previsão linear para os próximos 30 dias (linha vermelha tracejada). Essa análise pode auxiliar na definição de estratégias para aumentar a quantidade de viagens.")
                else:
                    st.info("Não há dados suficientes para gerar uma previsão.")
        else:
            st.info("Nenhuma viagem registrada ainda.")


    # Aba 4: Cadastros
    with aba_cadastros:
        st.subheader("Cadastro de Dados")
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Carros",
            "Origens",
            "Destinos",
            "Tipos de Óleo",
            "Motoristas"
        ])
        with tab1:
            cadastro_carros(db)
        with tab2:
            cadastro_origem(db)
        with tab3:
            cadastro_destino(db)
        with tab4:
            cadastro_tipos_oleo(db)
        with tab5:
            cadastro_motoristas(db)

def main():
    auth = AuthManager(env_file=".env")
    if auth.login():
        main_app()

if __name__ == "__main__":
    main()
