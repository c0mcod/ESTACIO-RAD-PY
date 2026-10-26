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
        
        self.configurar_estilos()
        self.criar_layout_principal()
        self.criar_formulario()
        self.criar_botoes()
        self.criar_treeview()
        self.atualizar_grade()

    def configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        COLOR_BG = "#f5f6f8"
        COLOR_PRIMARY = "#2563eb"
        COLOR_PRIMARY_HOVER = "#1d4ed8"
        COLOR_TEXT = "#1e293b"

        self.root.configure(bg=COLOR_BG)

        self.style.configure(".", background=COLOR_BG, foreground=COLOR_TEXT, font=("Segoe UI", 9))

        self.style.configure("TLabelframe", background=COLOR_BG, borderwidth=1, relief="solid")
        self.style.configure("TLabelframe.Label", background=COLOR_BG, foreground=COLOR_TEXT, font=("Segoe UI", 10, "bold"))

        # Botão Primário (Salvar)
        self.style.configure("Primary.TButton", font=("Segoe UI", 9, "bold"), background=COLOR_PRIMARY, foreground="white", borderwidth=0)
        self.style.map("Primary.TButton", background=[("active", COLOR_PRIMARY_HOVER)])

        # Treeview (Tabela)
        self.style.configure("Treeview", font=("Segoe UI", 9), rowheight=26, background="white", fieldbackground="white")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#e2e8f0", foreground=COLOR_TEXT)
        self.style.map("Treeview", background=[("selected", "#dbeafe")], foreground=[("selected", "#1e3a8a")])

    def criar_layout_principal(self):
        header_frame = tk.Frame(self.root, bg="#1e293b", height=50)
        header_frame.pack(side="top", fill="x")
        
        lbl_titulo = tk.Label(
            header_frame, 
            text="Sistema de Agendamento Pet Shop", 
            font=("Segoe UI", 14, "bold"), 
            bg="#1e293b", 
            fg="white"
        )
        lbl_titulo.pack(side="left", padx=20, pady=10)

        # Painel central para formulário e tabela
        self.main_container = tk.Frame(self.root, bg="#f5f6f8")
        self.main_container.pack(side="top", fill="both", expand=True, padx=15, pady=15)

        # Frame da Esquerda (Formulário e Botões)
        self.frame_esquerda = tk.Frame(self.main_container, bg="#f5f6f8")
        self.frame_esquerda.pack(side="left", fill="y", padx=(0, 10))

        # Frame da Direita (Tabela)
        self.frame_direita = ttk.LabelFrame(self.main_container, text=" Agendamentos Cadastrados ", padding=10)
        self.frame_direita.pack(side="right", fill="both", expand=True)

    # ---------- construcao da tela ----------
    def criar_formulario(self):
        # Card principal de dados
        self.form_group = ttk.LabelFrame(self.frame_esquerda, text=" Dados do Agendamento ", padding=12)
        self.form_group.pack(side="top", fill="x", pady=(0, 10))

        # Configuração do grid interno
        self.form_group.columnconfigure(1, weight=1)

        # Componentes do Formulário principal
        ttk.Label(self.form_group, text="Nome do Pet:").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_pet = ttk.Entry(self.form_group)
        self.entry_pet.grid(row=0, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(self.form_group, text="Nome do Tutor:").grid(row=1, column=0, sticky="w", pady=4)
        self.entry_tutor = ttk.Entry(self.form_group)
        self.entry_tutor.grid(row=1, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(self.form_group, text="Telefone:").grid(row=2, column=0, sticky="w", pady=4)
        self.entry_telefone = ttk.Entry(self.form_group)
        self.entry_telefone.grid(row=2, column=1, columnspan=2, sticky="ew", pady=4)

        # Bloco CEP
        ttk.Label(self.form_group, text="CEP:").grid(row=3, column=0, sticky="w", pady=4)
        self.entry_cep = ttk.Entry(self.form_group)
        self.entry_cep.grid(row=3, column=1, sticky="ew", pady=4, padx=(0, 5))
        
        self.btn_buscar_cep = ttk.Button(self.form_group, text="Buscar CEP", command=self.on_buscar_cep)
        self.btn_buscar_cep.grid(row=3, column=2, sticky="e", pady=4)

        # Card agrupador de Endereço
        self.endereco_group = ttk.LabelFrame(self.form_group, text=" Endereço ", padding=8)
        self.endereco_group.grid(row=4, column=0, columnspan=3, sticky="ew", pady=6)
        self.endereco_group.columnconfigure(1, weight=1)

        ttk.Label(self.endereco_group, text="Logradouro:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_logradouro = ttk.Entry(self.endereco_group)
        self.entry_logradouro.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(self.endereco_group, text="Bairro:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_bairro = ttk.Entry(self.endereco_group)
        self.entry_bairro.grid(row=1, column=1, sticky="ew", pady=2)

        ttk.Label(self.endereco_group, text="Cidade/UF:").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_cidade_uf = ttk.Entry(self.endereco_group)
        self.entry_cidade_uf.grid(row=2, column=1, sticky="ew", pady=2)

        ttk.Label(self.endereco_group, text="Número:").grid(row=3, column=0, sticky="w", pady=2)
        self.entry_numero = ttk.Entry(self.endereco_group)
        self.entry_numero.grid(row=3, column=1, sticky="ew", pady=2)

        # Serviços e Agendamento
        ttk.Label(self.form_group, text="Serviço:").grid(row=5, column=0, sticky="w", pady=4)
        self.combo_servico = ttk.Combobox(self.form_group, values=(SERVICOS), state="readonly")
        self.combo_servico.grid(row=5, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(self.form_group, text="Data/Hora:").grid(row=6, column=0, sticky="w", pady=4)
        self.entry_data_hora = ttk.Entry(self.form_group)
        self.entry_data_hora.grid(row=6, column=1, columnspan=2, sticky="ew", pady=4)

    def criar_botoes(self):
        frame_acoes = tk.Frame(self.frame_esquerda, bg="#f5f6f8")
        frame_acoes.pack(side="top", fill="x")

        btn_salvar = ttk.Button(frame_acoes, text="Salvar Agendamento", style="Primary.TButton", command=self.on_salvar)
        btn_salvar.pack(side="top", fill="x", ipady=4, pady=(0, 6))

        frame_secundario = tk.Frame(frame_acoes, bg="#f5f6f8")
        frame_secundario.pack(side="top", fill="x")

        btn_excluir = ttk.Button(frame_secundario, text="Excluir", command=self.on_excluir)
        btn_excluir.pack(side="left", expand=True, fill="x", padx=(0, 3))

        btn_limpar = ttk.Button(frame_secundario, text="Limpar", command=self.limpar_form)
        btn_limpar.pack(side="right", expand=True, fill="x", padx=(3, 0))

    def criar_treeview(self):
        colunas = ("id", "pet", "tutor", "servico", "data_hora")
        titulos = ["ID", "Pet", "Tutor", "Serviço", "Data e Hora"]

        self.tree = ttk.Treeview(self.frame_direita, columns=colunas, show="headings", selectmode="browse")

        for col, titulo in zip(colunas, titulos):
            self.tree.heading(col, text=titulo)

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("pet", width=120)
        self.tree.column("tutor", width=120)
        self.tree.column("servico", width=130)
        self.tree.column("data_hora", width=120, anchor="center")

        # Scrollbar para a Treeview
        scrollbar = ttk.Scrollbar(self.frame_direita, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

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
        if registro is None:
            return

        self.id_selecionado = id_
        self.preencher(self.entry_pet, registro[1])
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

    def campo(self, parent):
        pass
    
if __name__ == "__main__":
    criar_tabela()
    root = tk.Tk()
    App(root)
    root.mainloop()