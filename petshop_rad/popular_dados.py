"""Guilherme - Gera dados ficticios com Faker para testes (nao faz parte do app)."""
from faker import Faker

from database import criar_tabela, inserir

fake = Faker("pt_BR")
SERVICOS = []


def popular(qtd=10):
    criar_tabela()

    pass


if __name__ == "__main__":
    popular()
