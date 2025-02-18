# src/utils/cep.py
import requests

def consulta_cep(cep):
    """
    Consulta o CEP utilizando a API ViaCEP e retorna somente os campos:
    cep, logradouro, complemento, bairro, localidade e uf.
    """
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "erro" not in data:
            # Define os campos que queremos retornar
            keys_desejadas = ["cep", "logradouro", "complemento", "bairro", "localidade", "uf"]
            dados_filtrados = {key: data.get(key) for key in keys_desejadas}
            return dados_filtrados
    return None
