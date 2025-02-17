import streamlit as st
import pandas as pd
import altair as alt

from auth import AuthManager
from db_manager import DBManager
from utils import to_excel_bytes

def menu_cadastro(db: DBManager, nome, tabela):
    """
    Função auxiliar para gerenciar cadastros (carros, origens, destinos, etc.).
    """
    st.subheader(f"Gerenciar {nome}")
    novo_item = st.text_input(f"Adicionar novo {nome}", key=f"input_{tabela}")
    if st.button("Adicionar", key=f"add_{tabela}"):
        db.inserir_registro(tabela, novo_item)
        st.success(f"{nome} adicionado com sucesso!")

    registros = db.obter_registros(tabela)
    st.dataframe(registros)

    excluir_id = st.number_input(f"ID do {nome} para excluir", min_value=1, step=1, key=f"del_id_{tabela}")
    if st.button("Excluir", key=f"del_{tabela}"):
        db.excluir_registro(tabela, excluir_id)
        st.success(f"{nome} excluído com sucesso!")

def main_app():
    db = DBManager()  # Cria/garante as tabelas

    # Menu lateral com botão de Logout
    st.sidebar.title("Menu")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.experimental_rerun()

    st.title("📌 Sistema Gestão de Viagem - Horizonte Turismo")

    # Recupera o papel do usuário salvo na sessão (definido durante o login)
    user_role = st.session_state.get("role", "operator")  # padrão: operador

    # Define as abas de acordo com o papel do usuário
    if user_role == "admin":
        # Administrador tem acesso a todas as funcionalidades
        aba_principal, aba_tabela, aba_grafico, aba_cadastros = st.tabs([
            "Cadastro de Viagem",
            "Tabela de Viagens",
            "Gráfico de Viagens",
            "Cadastros"
        ])
    else:
        # Operador tem acesso somente ao Cadastro de Viagem e aos Cadastros
        aba_principal, aba_cadastros = st.tabs([
            "Cadastro de Viagem",
            "Cadastros"
        ])

    # ====================
    # ABA 1: Cadastro de Viagem
    # ====================
    with aba_principal:
        st.subheader("Dados da Viagem")

        # Linha 1: Origem, Destino, Carro, Motorista
        row1 = st.columns(4)
        with row1[0]:
            origens = db.obter_registros("origens")
            origem = st.selectbox("Origem", origens["nome"].tolist(), key="select_origem")
        with row1[1]:
            destinos = db.obter_registros("destinos")
            destino = st.selectbox("Destino", destinos["nome"].tolist(), key="select_destino")
        with row1[2]:
            carros = db.obter_registros("carros")
            carro = st.selectbox("Carro", carros["nome"].tolist(), key="select_carro")
        with row1[3]:
            motoristas = db.obter_registros("motoristas")
            motorista = st.selectbox("Motorista", motoristas["nome"].tolist(), key="select_motorista")

        # Linha 2: KM Saída, KM Chegada, Total KM
        row2 = st.columns(3)
        with row2[0]:
            km_saida = st.number_input("KM Saída", min_value=0.0, format="%.2f", key="km_saida")
        with row2[1]:
            km_chegada = st.number_input("KM Chegada", min_value=0.0, format="%.2f", key="km_chegada")
        with row2[2]:
            calculated_total_km = max(0.0, km_chegada - km_saida)
            st.number_input("Total KM", value=calculated_total_km, format="%.2f", key="total_km", disabled=True)

        # Linha 3: Datas e Pedágio
        row3 = st.columns(3)
        with row3[0]:
            data_saida = st.date_input("Data da Saída", key="data_saida").strftime("%Y-%m-%d")
        with row3[1]:
            data_volta = st.date_input("Data da Volta", key="data_volta").strftime("%Y-%m-%d")
        with row3[2]:
            pedagio = st.number_input("Pedágio", min_value=0.0, format="%.2f", key="pedagio")

        # Linha 4: Diesel S10, Diesel S500, Litros
        row4 = st.columns(3)
        with row4[0]:
            diesel_s10 = st.number_input("Diesel S10", min_value=0.0, format="%.2f", key="diesel_s10")
        with row4[1]:
            diesel_s500 = st.number_input("Diesel S500", min_value=0.0, format="%.2f", key="diesel_s500")
        with row4[2]:
            litros = st.number_input("Litros", min_value=0.0, format="%.2f", key="litros")

        # Linha 5: Valor do Combustível, Despesa Extra, etc.
        row5 = st.columns(3)
        with row5[0]:
            valor = st.number_input("Valor (Preço por Litro)", min_value=0.0, format="%.2f", key="valor")
        with row5[1]:
            despesa_extra = st.number_input("Despesa Extra", min_value=0.0, format="%.2f", key="despesa_extra")
        with row5[2]:
            computed_valor_combustivel = litros * valor
            st.number_input("Valor Combustível", value=computed_valor_combustivel, format="%.2f", key="valor_combustivel", disabled=True)

        # Linha 6: Diária e Valor Total
        row6 = st.columns(2)
        with row6[0]:
            diaria_motorista = st.number_input("Diária Motorista", min_value=0.0, format="%.2f", key="diaria_motorista")
        with row6[1]:
            computed_valor_total = computed_valor_combustivel + despesa_extra + diaria_motorista
            st.number_input("Valor Total", value=computed_valor_total, format="%.2f", key="valor_total", disabled=True)

        # Botão para salvar a viagem
        if st.button("Salvar Viagem"):
            dados = (
                origem,
                destino,
                carro,
                km_saida,
                km_chegada,
                calculated_total_km,
                data_saida,
                data_volta,
                valor,
                motorista,
                diaria_motorista,
                despesa_extra,
                diesel_s10,
                diesel_s500,
                litros,
                computed_valor_combustivel,
                pedagio,
                computed_valor_total
            )
            db.inserir_viagem(dados)
            st.success("Viagem registrada com sucesso!")

            # Limpa os campos do session_state
            keys_to_clear = [
                "select_origem", "km_saida", "data_saida", "diesel_s10", "valor",
                "select_motorista", "select_destino", "km_chegada", "data_volta",
                "diesel_s500", "diaria_motorista", "select_carro", "pedagio",
                "litros", "despesa_extra"
            ]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]

    # Se o usuário for administrador, exibe abas extras
    if user_role == "admin":
        # ======================
        # ABA 2: Tabela de Viagens
        # ======================
        with aba_tabela:
            st.subheader("📋 Viagens Registradas")
            viagens_df = db.obter_registros("viagens")

            if not viagens_df.empty:
                viagens_df["data_saida"] = pd.to_datetime(viagens_df["data_saida"], errors="coerce")

                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    anos = sorted(viagens_df["data_saida"].dt.year.dropna().unique().tolist())
                    anos_str = [str(a) for a in anos]
                    selected_ano = st.selectbox("Ano", ["Todos"] + anos_str, index=0)
                with col2:
                    meses = sorted(viagens_df["data_saida"].dt.month.dropna().unique().tolist())
                    meses_str = [str(m) for m in meses]
                    selected_mes = st.selectbox("Mês", ["Todos"] + meses_str, index=0)
                with col3:
                    origens_list = sorted(viagens_df["origem"].dropna().unique().tolist())
                    selected_origem = st.selectbox("Origem", ["Todos"] + origens_list, index=0)
                with col4:
                    destinos_list = sorted(viagens_df["destino"].dropna().unique().tolist())
                    selected_destino = st.selectbox("Destino", ["Todos"] + destinos_list, index=0)
                with col5:
                    motoristas_list = sorted(viagens_df["motorista"].dropna().unique().tolist())
                    selected_motorista = st.selectbox("Motorista", ["Todos"] + motoristas_list, index=0)

                # Aplicando filtros
                df_filtrado = viagens_df.copy()
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

                # Botão para exportar Excel
                excel_data = to_excel_bytes(df_filtrado)
                st.download_button(
                    label="Exportar para Excel",
                    data=excel_data,
                    file_name="viagens.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                st.dataframe(df_filtrado)
            else:
                st.info("Nenhuma viagem registrada ainda.")

        # =================
        # ABA 3: Gráficos de Viagens
        # =================
        with aba_grafico:
            st.subheader("📊 Gráficos de Viagens")
            viagens_df = db.obter_registros("viagens")
            if not viagens_df.empty:
                grafico_tab1, grafico_tab2, grafico_tab3, grafico_tab4 = st.tabs([
                    "Total KM por Data",
                    "Distribuição dos Custos",
                    "Valor Total x Total KM",
                    "Histograma de Total KM"
                ])

                with grafico_tab1:
                    viagens_df["data_saida"] = pd.to_datetime(viagens_df["data_saida"])
                    df_km = viagens_df.groupby("data_saida", as_index=False).agg({
                        'total_km': 'sum',
                        'valor_total': 'sum'
                    })

                    # Linha de tendência
                    st.line_chart(df_km.set_index("data_saida")[['total_km', 'valor_total']])

                    # Descrição
                    st.write("Este gráfico mostra a evolução do Total de KM percorridos e do Valor Total das viagens ao longo do tempo. Identifique padrões sazonais e a relação entre o KM e os custos.")

                with grafico_tab2:
                    custos = pd.DataFrame({
                        "Categoria": ["Pedágio", "Despesa Extra", "Diária Motorista", "Valor Combustível"],
                        "Valor": [viagens_df["pedagio"].sum(), viagens_df["despesa_extra"].sum(), viagens_df["diaria_motorista"].sum(), viagens_df["valor_combustivel"].sum()]
                    })
                    custos["Percentual"] = (custos["Valor"] / custos["Valor"].sum()) * 100  # Percentual de cada custo

                    chart = alt.Chart(custos).mark_arc(innerRadius=50).encode(
                        theta=alt.Theta(field="Valor", type="quantitative"),
                        color=alt.Color(field="Categoria", type="nominal"),
                        tooltip=[alt.Tooltip(field="Categoria", type="nominal"), alt.Tooltip(field="Valor", type="quantitative"), alt.Tooltip(field="Percentual", type="quantitative")]
                    ).properties(width=400, height=400)

                    st.altair_chart(chart, use_container_width=True)

                    # Descrição
                    st.write("A distribuição dos custos das viagens pode ajudar a identificar as áreas onde os recursos estão sendo mais consumidos. Analise o impacto de cada categoria de custo.")

                with grafico_tab3:
                    chart_scatter = alt.Chart(viagens_df).mark_circle(size=60).encode(
                        x=alt.X("total_km:Q", title="Total KM"),
                        y=alt.Y("valor_total:Q", title="Valor Total"),
                        color=alt.Color("origem:N", legend=alt.Legend(title="Origem")),  # Segmentando por origem
                        size=alt.Size("valor_total:Q", legend=alt.Legend(title="Valor Total")),  # Ajustando o tamanho dos pontos pelo valor total
                        tooltip=["origem", "destino", "total_km", "valor_total"]
                    ).interactive()

                    st.altair_chart(chart_scatter, use_container_width=True)

                    # Descrição
                    st.write("O gráfico de dispersão mostra a relação entre o Total de KM percorridos e o Valor Total das viagens. A segmentação por origem pode revelar padrões de custo e eficiência de cada região.")

                with grafico_tab4:
                    chart_hist = alt.Chart(viagens_df).mark_bar().encode(
                        alt.X("total_km:Q", bin=alt.Bin(maxbins=20), title="Total KM (binning)"),  # Melhorar binning
                        y=alt.Y("count():Q", title="Número de Viagens"),
                        color=alt.Color("total_km:Q", scale=alt.Scale(scheme='greens'))
                    ).properties(width=600, height=400)

                    st.altair_chart(chart_hist, use_container_width=True)

                    # Descrição
                    st.write("Este histograma mostra a distribuição do Total KM percorrido nas viagens. Pode ajudar a identificar os intervalos de distância mais frequentes e onde as viagens mais longas ou curtas predominam.")

    # ==================
    # ABA 4: Cadastros (disponível para ambos os papéis)
    # ==================
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
            menu_cadastro(db, "Carro", "carros")
        with tab2:
            menu_cadastro(db, "Origem", "origens")
        with tab3:
            menu_cadastro(db, "Destino", "destinos")
        with tab4:
            menu_cadastro(db, "Tipo de Óleo", "tipos_oleo")
        with tab5:
            menu_cadastro(db, "Motorista", "motoristas")

def main():
    auth = AuthManager(env_file=".env")
    if auth.login():
        main_app()

if __name__ == "__main__":
    main()
