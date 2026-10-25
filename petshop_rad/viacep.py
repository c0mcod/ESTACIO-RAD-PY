"""Carlos - Consulta de CEP na API ViaCEP."""
import requests

from logger import registrar_log


def buscar_cep(cep: str) -> dict:
    """Sempre devolve um dict. Se algo falhar, ele tem a chave "erro"."""
    cep_limpo = str(cep).strip().replace("-", "").replace(".", "")

    if not (cep_limpo.isdigit() and len(cep_limpo) == 8):
        return {"erro": "CEP inválido. Digite os 8 números."}

    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=5)
        response.raise_for_status() 
        dados = response.json()
    except requests.exceptions.RequestException as e:
        registrar_log("CONSULTA CEP", f'Falha ao consultar o CEP "{cep_limpo}" ({e}).')
        return {"erro": "Não foi possível consultar o ViaCEP. Verifique sua conexão."}

    if "erro" in dados:
        registrar_log("CONSULTA CEP", f'CEP "{cep_limpo}" não encontrado.')
        return {"erro": "CEP não encontrado."}

    registrar_log("CONSULTA CEP",
                  f'CEP "{dados["cep"]}" consultado com sucesso ({dados["localidade"]}/{dados["uf"]}).')
    return dados
