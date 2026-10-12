"""Guilherme - Banco de dados SQLite e funcoes do CRUD.

Contrato combinado (nao mudar assinaturas sem avisar):
    inserir(...)   -> int  (id criado)
    listar()       -> list[tuple]
    atualizar(...) -> None
    excluir(id)    -> None

por favor, manter as assinaturas pra não ter surpresas na integração da interface
"""
import sqlite3

DB_NAME = "agendamentos.db"  # caminho relativo, funciona em qualquer PC


def conectar():
    pass


def criar_tabela():

    pass


def inserir(pet, tutor, telefone, cep, logradouro, bairro,
            cidade_uf, numero, servico, data_hora) -> int:

    pass


def listar() -> list:

    return []


def atualizar(id, pet, tutor, telefone, cep, logradouro, bairro,
              cidade_uf, numero, servico, data_hora) -> None:

    pass


def excluir(id) -> None:

    pass
