"""Carlos - Interface tkinter (tela unica). Arquivo que roda o sistema.

Executar:  python main.py
"""
import tkinter as tk
from tkinter import ttk, messagebox

from database import criar_tabela, inserir, listar, atualizar, excluir
from viacep import buscar_cep


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Agendamento Pet Shop")
        self.id_selecionado = None 
        self.criar_formulario()
        self.criar_botoes()
        self.criar_treeview()
        self.atualizar_grade()

    # ---------- construcao da tela ----------
    def criar_formulario(self):

        pass

    def criar_botoes(self):

        pass

    def criar_treeview(self):

        pass

    # ---------- acoes ----------
    def on_buscar_cep(self):

        pass

    def on_salvar(self):

        pass

    def on_excluir(self):

        pass

    def on_selecionar(self, event):

        pass

    # ---------- utilitarios ----------
    def atualizar_grade(self):

        pass

    def limpar_form(self):

        pass


if __name__ == "__main__":
    criar_tabela()
    root = tk.Tk()
    App(root)
    root.mainloop()
