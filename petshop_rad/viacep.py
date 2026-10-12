"""Carlos - Consulta de CEP na API ViaCEP."""
import requests

from logger import registrar_log


def buscar_cep(cep: str):
    """Retorna dict com logradouro, bairro, localidade, uf; ou None se falhar.

    Quem chama (main.py) mostra o messagebox quando vier None.
    """

    return None
