"""Guilherme - Banco de dados SQLite e funcoes do CRUD.

Contrato combinado (nao mudar assinaturas sem avisar):
    inserir(...)   -> int  (id criado)
    listar()       -> list[tuple]
    atualizar(...) -> None
    excluir(id)    -> None

por favor, manter as assinaturas pra não ter surpresas na integração da interface
"""
import sqlite3

from logger import registrar_log

DB_NAME = "agendamentos.db"  # Caminho relativo para funcionar em qualquer SO


def conectar():
    return sqlite3.connect(DB_NAME)


def _limpar_string(valor):
    """Utilitário interno para evitar erros de strip() em valores nulos."""
    if isinstance(valor, str):
        return valor.strip()
    return valor if valor is not None else ""

def criar_tabela():
    try:
        # O uso do 'with' gerencia o ciclo de vida da conexão, fechando-a automaticamente
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agendamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pet TEXT NOT NULL,
                    tutor TEXT NOT NULL,
                    telefone TEXT,
                    cep TEXT,
                    logradouro TEXT,
                    bairro TEXT,
                    cidade_uf TEXT,
                    numero TEXT,
                    servico TEXT,
                    data_hora TEXT
                )
            """)
            conn.commit()
        registrar_log("INFO", "Tabela 'agendamentos' verificada/criada com sucesso.")
    except sqlite3.Error as e:
        registrar_log("ERRO_DB", f"Falha ao criar tabela: {e}")

def inserir(pet, tutor, telefone, cep, logradouro, bairro,
            cidade_uf, numero, servico, data_hora) -> int:
    #Realiza a limpeza e padronização dos dados antes da inserí-los no banco
    pet = _limpar_string(pet)
    tutor = _limpar_string(tutor)
    telefone = _limpar_string(telefone).replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    cep = _limpar_string(cep).replace("-", "")
    logradouro = _limpar_string(logradouro)
    bairro = _limpar_string(bairro)
    cidade_uf = _limpar_string(cidade_uf)
    numero = _limpar_string(numero)
    servico = _limpar_string(servico)
    data_hora = _limpar_string(data_hora)

    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO agendamentos 
                (pet, tutor, telefone, cep, logradouro, bairro, cidade_uf, numero, servico, data_hora)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (pet, tutor, telefone, cep, logradouro, bairro, cidade_uf, numero, servico, data_hora))
            conn.commit()
            id_gerado = cursor.lastrowid
            
        registrar_log("INSERT", f"Agendamento ID {id_gerado} criado (Pet: {pet}, Tutor: {tutor}).")
        return id_gerado
    except sqlite3.Error as e:
        registrar_log("ERRO_DB", f"Erro no INSERT: {e}")
        return -1


def listar() -> list:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM agendamentos")
            linhas = cursor.fetchall()
            
        registrar_log("SELECT", f"Listagem executada. {len(linhas)} registros encontrados.")
        return linhas
    except sqlite3.Error as e:
        registrar_log("ERRO_DB", f"Erro no SELECT: {e}")
        return []


def atualizar(id, pet, tutor, telefone, cep, logradouro, bairro,
              cidade_uf, numero, servico, data_hora) -> None:

    pet = _limpar_string(pet)
    tutor = _limpar_string(tutor)
    telefone = _limpar_string(telefone).replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    cep = _limpar_string(cep).replace("-", "")
    logradouro = _limpar_string(logradouro)
    bairro = _limpar_string(bairro)
    cidade_uf = _limpar_string(cidade_uf)
    numero = _limpar_string(numero)
    servico = _limpar_string(servico)
    data_hora = _limpar_string(data_hora)

    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE agendamentos 
                SET pet=?, tutor=?, telefone=?, cep=?, logradouro=?, bairro=?, cidade_uf=?, numero=?, servico=?, data_hora=?
                WHERE id=?
            """, (pet, tutor, telefone, cep, logradouro, bairro, cidade_uf, numero, servico, data_hora, id))
            conn.commit()
            
        registrar_log("UPDATE", f"Agendamento ID {id} atualizado com sucesso.")
    except sqlite3.Error as e:
        registrar_log("ERRO_DB", f"Erro no UPDATE do ID {id}: {e}")


def excluir(id) -> None:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM agendamentos WHERE id=?", (id,))
            conn.commit()
            
        registrar_log("DELETE", f"Agendamento ID {id} excluído do banco.")
    except sqlite3.Error as e:
        registrar_log("ERRO_DB", f"Erro no DELETE do ID {id}: {e}")