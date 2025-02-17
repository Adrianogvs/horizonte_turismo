import sqlite3

# Conecta ao banco
conn = sqlite3.connect('viagens.db')
cursor = conn.cursor()

# Executa um SELECT simples
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
rows = cursor.fetchall()

# Exibe as linhas retornadas
for row in rows:
    print(row)

conn.close()
