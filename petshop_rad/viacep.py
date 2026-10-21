"""Carlos - Consulta de CEP na API ViaCEP."""
import requests

from logger import registrar_log


def buscar_cep(cep: str):
    """Retorna dict com logradouro, bairro, localidade, uf; ou None se falhar.

    Quem chama (main.py) mostra o messagebox quando vier None.
    """

    cep_limpo = str(cep).replace("-", "").replace(".", "").strip()
    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"

    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            dados = response.json()
            
            if "erro" in dados:
                return {"erro": "CEP não encontrado na base de dados."}
                
            return dados
        else:
            return {"erro": f"Erro no servidor ViaCEP. Status: {response.status_code}"}
            
    except requests.exceptions.RequestException as e:
        return {"erro": f"Falha na conexão: {e}"}

