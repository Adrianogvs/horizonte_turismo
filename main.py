import streamlit as st
import pandas as pd
import altair as alt
from loguru import logger
import sys
import os

# Função auxiliar para limpar os campos do st.session_state
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

# Imports internos
from src.auth.auth import AuthManager
from src.database.db_manager import DBManager
from src.utils.utils import to_excel_bytes
from src.utils.cep import consulta_cep

logger.info("Iniciando a aplicação Streamlit")

# --------------------------------------------------
# FUNÇÕES DE CADASTRO SIMPLES (Carros, Motoristas, etc.)
# --------------------------------------------------

def cadastro_carros(db: DBManager):
    st.subheader("Gerenciar Carros")
    novo_carro = st.text_input("Adicionar novo Carro", key="carro_input")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Adicionar Carro", key="botao_adicionar_carro"):
            db.inserir_carro(novo_carro)
            st.success("Carro adicionado com sucesso!")
    with col2:
        if st.button("Limpar Campos", key="botao_limpar_carro"):
            limpar_campos(["carro_input"])

    df_carros = db.obter_carros()
    st.dataframe(df_carros)

    excluir_id = st.number_input("ID do Carro para excluir", min_value=1, step=1, key="carro_excluir")
    if st.button("Excluir Carro", key="botao_excluir_carro"):
        db.excluir_registro("carros", excluir_id)
        st.success("Carro excluído com sucesso!")

def cadastro_motoristas(db: DBManager):
    st.subheader("Gerenciar Motoristas")
    novo_motorista = st.text_input("Adicionar novo Motorista", key="motorista_input")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Adicionar Motorista", key="botao_adicionar_motorista"):
            db.inserir_motorista(novo_motorista)
            st.success("Motorista adicionado com sucesso!")
    with col2:
        if st.button("Limpar Campos", key="botao_limpar_motorista"):
            limpar_campos(["motorista_input"])

    df_mot = db.obter_motoristas()
    st.dataframe(df_mot)

    excluir_id = st.number_input("ID do Motorista para excluir", min_value=1, step=1, key="motorista_excluir")
    if st.button("Excluir Motorista", key="botao_excluir_motorista"):
        db.excluir_registro("motoristas", excluir_id)
        st.success("Motorista excluído com sucesso!")

def cadastro_tipos_oleo(db: DBManager):
    st.subheader("Gerenciar Tipos de Óleo")
    novo_oleo = st.text_input("Adicionar novo Tipo de Óleo", key="oleo_input")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Adicionar Óleo", key="botao_adicionar_oleo"):
            db.inserir_tipo_oleo(novo_oleo)
            st.success("Óleo adicionado com sucesso!")
    with col2:
        if st.button("Limpar Campos", key="botao_limpar_oleo"):
            limpar_campos(["oleo_input"])

    df_oleo = db.obter_tipos_oleo()
    st.dataframe(df_oleo)

    excluir_id = st.number_input("ID do Óleo para excluir", min_value=1, step=1, key="oleo_excluir")
    if st.button("Excluir Óleo", key="botao_excluir_oleo"):
        db.excluir_registro("tipos_oleo", excluir_id)
        st.success("Óleo excluído com sucesso!")

# --------------------------------------------------
# FUNÇÕES DE CADASTRO DE ENDEREÇO (ORIGEM / DESTINO)
# --------------------------------------------------

def cadastro_origem(db: DBManager):
    st.subheader("Cadastro de Origem (Endereço)")
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
                db.inserir_origem(endereco_id)
                st.success("Origem cadastrada com sucesso!")
                logger.info(f"Origem cadastrada com endereço ID {endereco_id}")
            else:
                st.error("Informe um CEP válido e digite o número do endereço.")
    with col2:
        if st.button("Limpar Campos", key="botao_limpar_origem"):
            limpar_campos(["origem_cep_input", "origem_numero_input"])

def cadastro_destino(db: DBManager):
    st.subheader("Cadastro de Destino (Endereço)")
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
                db.inserir_destino(endereco_id)
                st.success("Destino cadastrado com sucesso!")
                logger.info(f"Destino cadastrado com endereço ID {endereco_id}")
            else:
                st.error("Informe um CEP válido e digite o número do endereço.")
    with col2:
        if st.button("Limpar Campos", key="botao_limpar_destino"):
            limpar_campos(["destino_cep_input", "destino_numero_input"])

# --------------------------------------------------
# FUNÇÃO PRINCIPAL
# --------------------------------------------------

def main_app():
    db = DBManager()

    st.sidebar.title("Menu")
    if st.sidebar.button("Logout", key="botao_logout"):
        st.session_state.authenticated = False
        st.experimental_rerun()
        logger.info("Usuário fez logout.")

    st.title("📌 Sistema de Gestão de Viagem - Horizonte Turismo")

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

    # ========== ABA 1: Cadastro de Viagem ==========
    with aba_principal:
        st.subheader("Cadastro de Nova Viagem")

        # Carrega as origens e destinos
        origens = db.obter_origens()
        destinos = db.obter_destinos()

        # Concatena os campos para exibir o endereço completo
        opcoes_origem = [
            f"{o['cep']} {o['logradouro']} {o['complemento']} {o['bairro']} {o['localidade']} {o['uf']} {o['numero']}"
            for o in origens
        ]
        opcoes_destino = [
            f"{d['cep']} {d['logradouro']} {d['complemento']} {d['bairro']} {d['localidade']} {d['uf']} {d['numero']}"
            for d in destinos
        ]

        # Verifica se há pelo menos uma origem e destino
        tem_origem = len(opcoes_origem) > 0
        tem_destino = len(opcoes_destino) > 0

        if not tem_origem:
            st.warning("Nenhuma origem cadastrada. Cadastre uma origem antes de registrar viagens.")
        if not tem_destino:
            st.warning("Nenhum destino cadastrado. Cadastre um destino antes de registrar viagens.")

        # Cria selectboxes. Se não houver registros, ficam desabilitados
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

        # Recupera o ID interno, se houver
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
            litros = st.number_input("Litros", min_value=0.0, format="%.2f", key="viagem_litros")

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
            computed_valor_total = computed_valor_combustivel + despesa_extra + diaria_motorista
            st.number_input("Valor Total", value=computed_valor_total, format="%.2f",
                            key="viagem_valor_total", disabled=True)

        # Se não houver origem/destino, desabilita "Salvar Viagem"
        can_save = (origem_id is not None) and (destino_id is not None)

        col_salvar, col_limpar = st.columns(2)
        with col_salvar:
            if st.button("Salvar Viagem", key="botao_salvar_viagem", disabled=(not can_save)):
                db.inserir_viagem(
                    origem_id=origem_id,
                    destino_id=destino_id,
                    carro=carro,
                    km_saida=km_saida,
                    km_chegada=km_chegada,
                    total_km=calculated_total_km,
                    data_saida=data_saida,
                    data_volta=data_volta,
                    valor=valor,
                    motorista=motorista,
                    diaria_motorista=diaria_motorista,
                    despesa_extra=despesa_extra,
                    diesel_s10=diesel_s10,
                    diesel_s500=diesel_s500,
                    litros=litros,
                    valor_combustivel=computed_valor_combustivel,
                    pedagio=pedagio,
                    valor_total=computed_valor_total
                )
                st.success("Viagem registrada com sucesso!")
                logger.info(f"Viagem inserida: origem_id={origem_id}, destino_id={destino_id}")
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

    # ========== ABA 2: Tabela de Viagens (Admin) ==========
    if user_role == "admin":
        with aba_tabela:
            st.subheader("📋 Viagens Registradas")
            df_viagens = db.obter_viagens_completo()
            if not df_viagens.empty:
                df_viagens["data_saida"] = pd.to_datetime(df_viagens["data_saida"], errors="coerce")
                # Filtros
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    anos = sorted(df_viagens["data_saida"].dt.year.dropna().unique().tolist())
                    anos_str = [str(a) for a in anos]
                    selected_ano = st.selectbox("Ano", ["Todos"] + anos_str, index=0, key="tabela_filtro_ano")
                with col2:
                    meses = sorted(df_viagens["data_saida"].dt.month.dropna().unique().tolist())
                    meses_str = [str(m) for m in meses]
                    selected_mes = st.selectbox("Mês", ["Todos"] + meses_str, index=0, key="tabela_filtro_mes")
                with col3:
                    origens_list = sorted(df_viagens["origem"].dropna().unique().tolist())
                    selected_origem = st.selectbox("Origem", ["Todos"] + origens_list, index=0, key="tabela_filtro_origem")
                with col4:
                    destinos_list = sorted(df_viagens["destino"].dropna().unique().tolist())
                    selected_destino = st.selectbox("Destino", ["Todos"] + destinos_list, index=0, key="tabela_filtro_destino")
                with col5:
                    motoristas_list = sorted(df_viagens["motorista"].dropna().unique().tolist())
                    selected_motorista = st.selectbox("Motorista", ["Todos"] + motoristas_list, index=0, key="tabela_filtro_motorista")

                df_filtrado = df_viagens.copy()
                if selected_ano != "Todos":
                    df_filtrado = df_filtrado[df_filtrado["data_saida"].dt.year == int(selected_ano)]
                if selected_mes != "Todos":
                    df_filtrado = df_filtrado[df_filtrado["data_saida"].dt.month == int(selected_mes)]
                if selected_origem != "Todos":
                    df_filtrado = df_filtrado[df_filtrado["origem"] == selected_origem]
                if selected_destino != "Todos":
                    df_filtrado = df_filtrado[df_filtrado["destino"] == selected_destino]
                if selected_motorista != "Todos":
                    df_filtrado = df_filtrado[df_filtrado["motorista"] == selected_motorista]

                # Subtotais
                subtotal_total_km = df_filtrado["total_km"].sum()
                subtotal_valor_total = df_filtrado["valor_total"].sum()
                subtotal_valor_combustivel = df_filtrado["valor_combustivel"].sum()
                subtotal_pedagio = df_filtrado["pedagio"].sum()
                subtotal_despesa_extra = df_filtrado["despesa_extra"].sum()
                subtotal_diaria = df_filtrado["diaria_motorista"].sum()

                st.markdown("### Subtotais")
                st.write(f"**Total KM:** {subtotal_total_km:,.2f}")
                st.write(f"**Valor Total:** {subtotal_valor_total:,.2f}")
                st.write(f"**Valor Combustível:** {subtotal_valor_combustivel:,.2f}")
                st.write(f"**Pedágio:** {subtotal_pedagio:,.2f}")
                st.write(f"**Despesa Extra:** {subtotal_despesa_extra:,.2f}")
                st.write(f"**Diária Motorista:** {subtotal_diaria:,.2f}")

                excel_data = to_excel_bytes(df_filtrado)
                st.download_button(
                    label="Exportar para Excel",
                    data=excel_data,
                    file_name="viagens_com_enderecos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="tabela_botao_exportar_excel"
                )

                st.dataframe(df_filtrado)
            else:
                st.info("Nenhuma viagem registrada ainda.")

        # ========== ABA 3: Gráficos de Viagens ==========
        with aba_grafico:
            st.subheader("📊 Gráficos de Viagens")
            df_viagens = db.obter_viagens_completo()
            if not df_viagens.empty:
                grafico_tab1, grafico_tab2, grafico_tab3, grafico_tab4, grafico_tab5 = st.tabs([
                    "Total KM por Data",
                    "Distribuição dos Custos",
                    "Valor Total x Total KM",
                    "Histograma de Total KM",
                    "Evolução dos Custos de Viagem"
                ])
                with grafico_tab1:
                    df_viagens["data_saida"] = pd.to_datetime(df_viagens["data_saida"])
                    df_km = df_viagens.groupby("data_saida", as_index=False).agg({
                        'total_km': 'sum',
                        'valor_total': 'sum'
                    })
                    st.line_chart(df_km.set_index("data_saida")[['total_km', 'valor_total']])
                    st.write("Este gráfico mostra a evolução do Total de KM percorridos e do Valor Total das viagens ao longo do tempo. Identifique padrões sazonais e a relação entre o KM e os custos.")

                with grafico_tab2:
                    custos = pd.DataFrame({
                        "Categoria": ["Pedágio", "Despesa Extra", "Diária Motorista", "Valor Combustível"],
                        "Valor": [
                            df_viagens["pedagio"].sum(),
                            df_viagens["despesa_extra"].sum(),
                            df_viagens["diaria_motorista"].sum(),
                            df_viagens["valor_combustivel"].sum()
                        ]
                    })
                    custos["Percentual"] = (custos["Valor"] / custos["Valor"].sum()) * 100
                    import altair as alt
                    chart = alt.Chart(custos).mark_arc(innerRadius=50).encode(
                        theta=alt.Theta(field="Valor", type="quantitative"),
                        color=alt.Color(field="Categoria", type="nominal"),
                        tooltip=[
                            alt.Tooltip(field="Categoria", type="nominal"),
                            alt.Tooltip(field="Valor", type="quantitative"),
                            alt.Tooltip(field="Percentual", type="quantitative")
                        ]
                    ).properties(width=400, height=400)
                    st.altair_chart(chart, use_container_width=True)
                    st.write("A distribuição dos custos das viagens pode ajudar a identificar as áreas onde os recursos estão sendo mais consumidos. Analise o impacto de cada categoria de custo.")

                with grafico_tab3:
                    chart_scatter = alt.Chart(df_viagens).mark_circle(size=60).encode(
                        x=alt.X("total_km:Q", title="Total KM"),
                        y=alt.Y("valor_total:Q", title="Valor Total"),
                        color=alt.Color("origem:O", legend=alt.Legend(title="Origem")),
                        size=alt.Size("valor_total:Q", legend=alt.Legend(title="Valor Total")),
                        tooltip=["origem", "destino", "total_km", "valor_total"]
                    ).interactive()
                    st.altair_chart(chart_scatter, use_container_width=True)
                    st.write("O gráfico de dispersão mostra a relação entre o Total de KM percorridos e o Valor Total das viagens. A segmentação por origem pode revelar padrões de custo e eficiência de cada região.")

                with grafico_tab4:
                    chart_hist = alt.Chart(df_viagens).mark_bar().encode(
                        alt.X("total_km:Q", bin=alt.Bin(maxbins=20), title="Total KM (binning)"),
                        y=alt.Y("count():Q", title="Número de Viagens"),
                        color=alt.Color("total_km:Q", scale=alt.Scale(scheme='greens'))
                    ).properties(width=600, height=400)
                    st.altair_chart(chart_hist, use_container_width=True)
                    st.write("Este histograma mostra a distribuição do Total KM percorrido nas viagens. Pode ajudar a identificar os intervalos de distância mais frequentes e onde as viagens mais longas ou curtas predominam.")

                with grafico_tab5:
                    df_costos = df_viagens.groupby("data_saida")[
                        ["pedagio", "despesa_extra", "diaria_motorista", "valor_combustivel"]
                    ].sum().reset_index()
                    chart_area = alt.Chart(df_costos).mark_area().encode(
                        x='data_saida:T',
                        y=alt.Y('pedagio:Q', stack='zero', title="Custo Total"),
                        color=alt.Color('variable:N', title="Categoria de Custo"),
                    ).transform_fold(
                        ['pedagio', 'despesa_extra', 'diaria_motorista', 'valor_combustivel'],
                        as_=['variable', 'value']
                    ).properties(
                        title="Evolução dos Custos de Viagem ao Longo do Tempo",
                        width=800,
                        height=400
                    )
                    st.altair_chart(chart_area, use_container_width=True)
                    st.write("Este gráfico de área empilhada mostra a evolução dos custos de viagem ao longo do tempo. A segmentação por categoria de custo revela como cada tipo de custo contribui para o custo total das viagens ao longo dos dias.")
            else:
                st.info("Nenhuma viagem registrada ainda.")

        # ========== ABA 4: Cadastros ==========
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
