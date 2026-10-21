"""Guilherme - Log de auditoria em arquivo .txt."""
from datetime import datetime

LOG_FILE = "log_agendamentos.txt"


def registrar_log(acao: str, mensagem: str) -> None:
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha_log = f"[{data_hora}] {acao}: {mensagem}\n"

    try:
        with open(LOG_FILE, "a") as arquivo_log:
            arquivo_log.write(linha_log)
    except Exception as e:
        print(f"Erro ao registrar log: {e}")
