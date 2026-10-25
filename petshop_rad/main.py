"""Carlos - Interface tkinter (tela unica). Arquivo que roda o sistema.

Executar:  python main.py
"""
import tkinter as tk
from tkinter import ttk, messagebox

from database import criar_tabela, inserir, listar, atualizar, excluir
from viacep import buscar_cep
from popular_dados import SERVICOS

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
        tk.Label(self.root, text="Data/Hora").grid(row=10,column=0,padx=5, pady=5)

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
        self.entry_data_hora = tk.Entry(self.root)
        # ---------- campos do CEP ----------
        self.entry_logradouro = tk.Entry(self.root)
        self.entry_bairro = tk.Entry(self.root)
        self.entry_cidade_uf = tk.Entry(self.root)
        self.entry_numero = tk.Entry(self.root)

        # ---------- grid de campos ----------
        self.entry_pet.grid(row=0, column=1, padx=5, pady=5)
        self.entry_tutor.grid(row=1, column=1, padx=5, pady=5)
        self.entry_telefone.grid(row=2, column=1, padx=5, pady=5)
        self.entry_cep.grid(row=3,column=1,padx=5,pady=5)

        # ---------- grid dos capos de CEP ----------
        self.entry_logradouro.grid(row=5, column=1, padx=5, pady=5)
        self.entry_bairro.grid(row=6, column=1, padx=5, pady=5)
        self.entry_cidade_uf.grid(row=7, column=1, padx=5, pady=5)
        self.entry_numero.grid(row=8, column=1, padx=5, pady=5)
        self.entry_data_hora.grid(row=10, column=1, padx=5, pady=5)

        # ---------- combobox para os serviços ----------
        self.combo_servico = ttk.Combobox(self.root, values=(SERVICOS), state="readonly", width=18)

        self.combo_servico.grid(row=9, column=1, padx=5, pady=5)

    def criar_botoes(self):
        tk.Button(self.root, text="Buscar CEP", command=self.on_buscar_cep).grid(row=3,column=2,padx=5,pady=5)
        tk.Button(self.root, text="Salvar", command=self.on_salvar).grid(row=11, column=0, padx=5,pady=5)
        tk.Button(self.root, text="Excluir", command=self.on_excluir).grid(row=11, column=1, padx=5,pady=5)
        tk.Button(self.root, text="Limpar", command=self.limpar_form).grid(row=11, column=2, padx=5,pady=5)

    def criar_treeview(self):
        colunas = ("id", "pet", "tutor", "servico", "data_hora")
        titulos = ["ID", "Pet", "Tutor", "Serviço", "Data e Hora"]

        self.tree = ttk.Treeview(self.root, columns=colunas, show="headings", height=8)

        for col, titulo in zip(colunas, titulos):
            self.tree.heading(col, text=titulo)

        self.tree.column("id", width=40)
        self.tree.grid(row=0, column=4, rowspan=11, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_selecionar)    

    # ---------- acoes ----------
    def on_buscar_cep(self):
        dados = buscar_cep(self.entry_cep.get())
    
        if "erro" in dados:
            messagebox.showwarning("Aviso", dados["erro"])
            return
    
        self.preencher(self.entry_logradouro, dados["logradouro"])
        self.preencher(self.entry_bairro, dados["bairro"])
        self.preencher(self.entry_cidade_uf, dados["localidade"] + "/" + dados["uf"])

    def on_salvar(self):
        pet = self.entry_pet.get().strip()
        tutor = self.entry_tutor.get().strip()
        telefone = self.entry_telefone.get().strip().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        cep = self.entry_cep.get().strip().replace("-", "").replace(".", "")
        logradouro = self.entry_logradouro.get().strip()
        bairro = self.entry_bairro.get().strip()
        cidade_uf = self.entry_cidade_uf.get().strip()
        numero = self.entry_numero.get().strip()
        servico = self.combo_servico.get().strip()
        data_hora = self.entry_data_hora.get().strip()

        # 2) validar
        if not pet or not tutor or not servico or not data_hora:
            messagebox.showwarning("Aviso", "Preencha pet, tutor, serviço e data/hora.")
            return

        # 3) criar ou atualizar
        if self.id_selecionado is None:
            inserir(pet, tutor, telefone, cep, logradouro, bairro, cidade_uf, numero, servico, data_hora)
        else:
            atualizar(self.id_selecionado, pet, tutor, telefone, cep, logradouro, bairro, cidade_uf, numero, servico, data_hora)

        self.atualizar_grade()
        self.limpar_form()

    def on_excluir(self):
        if self.id_selecionado is None:
            messagebox.showwarning("Aviso", "Selecione um agendamento na tabela.")
            return
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este agendamento?"):
            excluir(self.id_selecionado)
            self.atualizar_grade()
            self.limpar_form()

    def on_selecionar(self, event):
        sel = self.tree.selection()

        if not sel:
            return
        
        id_ = int(self.tree.item(sel[0], "values")[0])

        registro = next((r for r in listar() if r[0] == id_), None)
        if registro  is None:
            return

        self.id_selecionado = id_
        self.preencher(self.entry_pet,registro[1])
        self.preencher(self.entry_tutor, registro[2])
        self.preencher(self.entry_telefone, registro[3])
        self.preencher(self.entry_cep, registro[4])
        self.preencher(self.entry_logradouro, registro[5])
        self.preencher(self.entry_bairro, registro[6])
        self.preencher(self.entry_cidade_uf, registro[7])
        self.preencher(self.entry_numero, registro[8])
        self.preencher(self.combo_servico, registro[9])
        self.preencher(self.entry_data_hora, registro[10])

    # ---------- utilitarios ----------
    def atualizar_grade(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in listar():
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[9], r[10]))

    def limpar_form(self):
        entries = (self.entry_pet, self.entry_tutor, self.entry_telefone,
                   self.entry_cep, self.entry_logradouro, self.entry_bairro,
                   self.entry_cidade_uf, self.entry_numero, self.entry_data_hora)
        for entry in entries:
            entry.delete(0, "end")
    
        self.combo_servico.set("")
        self.id_selecionado = None
        self.tree.selection_remove(self.tree.selection())
        self.entry_pet.focus()

    def preencher(self, entry, texto):
        entry.delete(0, "end")
        entry.insert(0, texto)

if __name__ == "__main__":
    criar_tabela()
    root = tk.Tk()
    App(root)
    root.mainloop()
