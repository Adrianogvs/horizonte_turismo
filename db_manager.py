import sqlite3
import pandas as pd

class DBManager:
    def __init__(self, db_path="viagens.db"):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """
        Cria as tabelas necessárias, caso ainda não existam.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS viagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origem TEXT, 
                destino TEXT, 
                carro TEXT,
                km_saida REAL, 
                km_chegada REAL, 
                total_km REAL,
                data_saida TEXT, 
                data_volta TEXT, 
                valor REAL,
                motorista TEXT, 
                diaria_motorista REAL,
                despesa_extra REAL,
                diesel_s10 REAL, 
                diesel_s500 REAL, 
                litros REAL,
                valor_combustivel REAL,
                pedagio REAL, 
                valor_total REAL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS origens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS destinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tipos_oleo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS motoristas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE
            )
        ''')

        conn.commit()
        conn.close()

    def obter_registros(self, tabela):
        """
        Retorna um DataFrame com os registros da tabela especificada.
        Se a tabela for de cadastro e estiver vazia, retorna colunas ["id", "nome"].
        """
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql(f"SELECT * FROM {tabela}", conn)
        conn.close()

        if tabela != "viagens" and df.empty:
            df = pd.DataFrame(columns=["id", "nome"])
        return df

    def inserir_registro(self, tabela, nome):
        """
        Insere um novo registro (nome) na tabela especificada.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {tabela} (nome) VALUES (?)", (nome,))
        conn.commit()
        conn.close()

    def excluir_registro(self, tabela, registro_id):
        """
        Exclui um registro da tabela com base no ID.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {tabela} WHERE id = ?", (registro_id,))
        conn.commit()
        conn.close()

    def inserir_viagem(self, dados):
        """
        Insere uma nova linha na tabela 'viagens'.
        'dados' deve ser uma tupla com todos os campos na ordem do INSERT.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO viagens (
                origem, destino, carro, 
                km_saida, km_chegada, total_km,
                data_saida, data_volta, valor,
                motorista, diaria_motorista, despesa_extra,
                diesel_s10, diesel_s500, litros,
                valor_combustivel, pedagio, valor_total
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', dados)
        conn.commit()
        conn.close()