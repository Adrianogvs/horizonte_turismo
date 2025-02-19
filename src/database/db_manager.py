import sqlite3
import pandas as pd

class DBManager:
    def __init__(self, db_path="viagens.db"):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """
        Cria as tabelas necessárias se elas não existirem.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabela de endereços
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enderecos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cep TEXT,
                logradouro TEXT,
                complemento TEXT,
                bairro TEXT,
                localidade TEXT,
                uf TEXT,
                numero TEXT
            )
        ''')

        # Tabela de origens (referenciando enderecos)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS origens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endereco_id INTEGER,
                FOREIGN KEY(endereco_id) REFERENCES enderecos(id)
            )
        ''')

        # Tabela de destinos (referenciando enderecos)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS destinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endereco_id INTEGER,
                FOREIGN KEY(endereco_id) REFERENCES enderecos(id)
            )
        ''')

        # Tabela de carros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE
            )
        ''')

        # Tabela de tipos de óleo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tipos_oleo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE
            )
        ''')

        # Tabela de motoristas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS motoristas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE
            )
        ''')

        # Tabela de viagens (usa FK para origens e destinos)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS viagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origem_id INTEGER,
                destino_id INTEGER,
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
                valor_total REAL,
                FOREIGN KEY(origem_id) REFERENCES origens(id),
                FOREIGN KEY(destino_id) REFERENCES destinos(id)
            )
        ''')

        conn.commit()
        conn.close()

    # --------------------------------------------------
    # Métodos para Endereços, Origens e Destinos
    # --------------------------------------------------

    def inserir_endereco(self, cep, logradouro, complemento, bairro, localidade, uf, numero):
        """
        Insere um registro na tabela 'enderecos' e retorna o ID gerado.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO enderecos (cep, logradouro, complemento, bairro, localidade, uf, numero)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (cep, logradouro, complemento, bairro, localidade, uf, numero))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    def inserir_origem(self, endereco_id):
        """
        Insere um registro na tabela 'origens', referenciando o endereço.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO origens (endereco_id) VALUES (?)', (endereco_id,))
        conn.commit()
        origem_id = cursor.lastrowid
        conn.close()
        return origem_id

    def inserir_destino(self, endereco_id):
        """
        Insere um registro na tabela 'destinos', referenciando o endereço.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO destinos (endereco_id) VALUES (?)', (endereco_id,))
        conn.commit()
        destino_id = cursor.lastrowid
        conn.close()
        return destino_id

    def obter_origens(self):
        """
        Retorna as origens com os dados do endereço (join entre origens e enderecos).
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.id AS origem_id,
                   e.id AS endereco_id,
                   e.cep, e.logradouro, e.complemento,
                   e.bairro, e.localidade, e.uf, e.numero
            FROM origens o
            JOIN enderecos e ON o.endereco_id = e.id
        ''')
        rows = cursor.fetchall()
        conn.close()
        columns = ["origem_id", "endereco_id", "cep", "logradouro", "complemento",
                   "bairro", "localidade", "uf", "numero"]
        return [dict(zip(columns, row)) for row in rows]

    def obter_destinos(self):
        """
        Retorna os destinos com os dados do endereço (join entre destinos e enderecos).
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT d.id AS destino_id,
                   e.id AS endereco_id,
                   e.cep, e.logradouro, e.complemento,
                   e.bairro, e.localidade, e.uf, e.numero
            FROM destinos d
            JOIN enderecos e ON d.endereco_id = e.id
        ''')
        rows = cursor.fetchall()
        conn.close()
        columns = ["destino_id", "endereco_id", "cep", "logradouro", "complemento",
                   "bairro", "localidade", "uf", "numero"]
        return [dict(zip(columns, row)) for row in rows]

    # --------------------------------------------------
    # Métodos para Carros, Motoristas e Tipos de Óleo
    # --------------------------------------------------

    def inserir_carro(self, nome):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO carros (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()

    def inserir_motorista(self, nome):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO motoristas (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()

    def inserir_tipo_oleo(self, nome):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tipos_oleo (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()

    def obter_carros(self):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql('SELECT * FROM carros', conn)
        conn.close()
        return df

    def obter_motoristas(self):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql('SELECT * FROM motoristas', conn)
        conn.close()
        return df

    def obter_tipos_oleo(self):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql('SELECT * FROM tipos_oleo', conn)
        conn.close()
        return df

    # --------------------------------------------------
    # Método para excluir registro (evita erro ao excluir)
    # --------------------------------------------------

    def excluir_registro(self, tabela, registro_id):
        """
        Exclui um registro de 'tabela' pelo campo ID (chamado 'id').
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {tabela} WHERE id = ?", (registro_id,))
        conn.commit()
        conn.close()

    # --------------------------------------------------
    # Métodos para Viagens
    # --------------------------------------------------

    def inserir_viagem(self, origem_id, destino_id, carro, km_saida, km_chegada, total_km,
                       data_saida, data_volta, valor, motorista, diaria_motorista, despesa_extra,
                       diesel_s10, diesel_s500, litros, valor_combustivel, pedagio, valor_total):
        """
        Insere um registro na tabela 'viagens', referenciando as origens e destinos.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO viagens (
                origem_id, destino_id, carro,
                km_saida, km_chegada, total_km,
                data_saida, data_volta, valor,
                motorista, diaria_motorista, despesa_extra,
                diesel_s10, diesel_s500, litros,
                valor_combustivel, pedagio, valor_total
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (origem_id, destino_id, carro, km_saida, km_chegada, total_km,
              data_saida, data_volta, valor, motorista, diaria_motorista,
              despesa_extra, diesel_s10, diesel_s500, litros, valor_combustivel,
              pedagio, valor_total))
        conn.commit()
        conn.close()

    def obter_viagens(self):
        """
        Retorna todas as viagens cadastradas (sem JOIN).
        """
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql('SELECT * FROM viagens', conn)
        conn.close()
        return df

    def obter_viagens_completo(self):
        """
        Retorna todas as viagens com os dados de endereço concatenados em duas colunas:
        'origem' e 'destino'.
        """
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT 
                v.*,
                (e1.cep || ' ' || e1.logradouro || ' ' || COALESCE(e1.complemento, '') || ' ' ||
                 e1.bairro || ' ' || e1.localidade || ' ' || e1.uf || ' ' || e1.numero) AS origem,
                (e2.cep || ' ' || e2.logradouro || ' ' || COALESCE(e2.complemento, '') || ' ' ||
                 e2.bairro || ' ' || e2.localidade || ' ' || e2.uf || ' ' || e2.numero) AS destino
            FROM viagens v
            LEFT JOIN origens o ON v.origem_id = o.id
            LEFT JOIN enderecos e1 ON o.endereco_id = e1.id
            LEFT JOIN destinos d ON v.destino_id = d.id
            LEFT JOIN enderecos e2 ON d.endereco_id = e2.id
        '''
        df = pd.read_sql(query, conn)
        conn.close()
        return df
