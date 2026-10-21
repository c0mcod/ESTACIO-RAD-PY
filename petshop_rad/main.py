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

        # ---------- labels ----------
        tk.Label(self.root, text="Nome do pet:").grid(row=0,column=0,padx=5,pady=5)
        tk.Label(self.root, text="Nome do tutor:").grid(row=1,column=0,padx=5,pady=5)
        tk.Label(self.root, text="Telefone:").grid(row=2,column=0,padx=5,pady=5)
        tk.Label(self.root, text="CEP:").grid(row=3,column=0,padx=5,pady=5)
        tk.Label(self.root, text="Serviços").grid(row=9, column=0, padx=5, pady=5)

        # ---------- labels do CEP ----------
        tk.Label(self.root, text="Logradouro").grid(row=5, column=0, padx=5, pady=5)
        tk.Label(self.root, text="Bairro").grid(row=6, column=0, padx=5, pady=5)
        tk.Label(self.root, text="cidade/UF").grid(row=7, column=0, padx=5, pady=5)
        tk.Label(self.root, text="Número").grid(row=8, column=0, padx=5, pady=5)

        # ---------- campos ----------
        self.entry_cep = tk.Entry(self.root)
        self.entry_pet = tk.Entry(self.root)
        self.entry_tutor = tk.Entry(self.root)
        self.entry_telefone = tk.Entry(self.root)
        # ---------- campos do CEP ----------
        self.entry_logradouro = tk.Entry(self.root)
        self.entry_bairro = tk.Entry(self.root)
        self.entry_cidade_UF = tk.Entry(self.root)
        self.entry_numero = tk.Entry(self.root)

        # ---------- grid de campos ----------
        self.entry_pet.grid(row=0, column=1, padx=5, pady=5)
        self.entry_tutor.grid(row=1, column=1, padx=5, pady=5)
        self.entry_telefone.grid(row=2, column=1, padx=5, pady=5)
        self.entry_cep.grid(row=3,column=1,padx=5,pady=5)

        # ---------- grid dos capos de CEP ----------
        self.entry_logradouro.grid(row=5, column=1, padx=5, pady=5)
        self.entry_bairro.grid(row=6, column=1, padx=5, pady=5)
        self.entry_cidade_UF.grid(row=7, column=1, padx=5, pady=5)
        self.entry_numero.grid(row=8, column=1, padx=5, pady=5)

        # ---------- combobox para os serviços ----------
        self.combo_servico = ttk.Combobox(self.root, values=["Consulta", "Vacinação", "Banho e Tosa"], state="readonly")

        self.combo_servico.grid(row=9, column=1, padx=5, pady=5)

    def criar_botoes(self):
        tk.Button(self.root, text="Buscar CEP", command=self.on_buscar_cep).grid(row=3,column=3,padx=5,pady=6)


    def criar_treeview(self):

        pass

    # ---------- acoes ----------
    def on_buscar_cep(self):
        url = "https://viacep.com.br/ws/{}/json/"
        dados = buscar_cep(self.entry_cep.get())
        
        if dados is None:
            messagebox.showwarning("Aviso", "CEP não encontrado.")
            return
        
        self.preencher(self.entry_logradouro, dados["logradouro"])
        self.preencher(self.entry_bairro, dados["bairro"])
        self.preencher(self.entry_cidade_UF, dados["localidade"] + "/" + dados["uf"])
        
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

    def preencher(self, entry, texto):
        entry.delete(0, "end")
        entry.insert(0, texto)

if __name__ == "__main__":
    criar_tabela()
    root = tk.Tk()
    App(root)
    root.mainloop()
