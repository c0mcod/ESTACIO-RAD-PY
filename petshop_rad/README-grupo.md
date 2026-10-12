# Pet Shop RAD

Mini sistema de agendamento veterinario / pet shop (tkinter + SQLite + ViaCEP).

## Como rodar

Dentro da pasta `petshop_rad`:

    python -m venv venv

Ativar o ambiente virtual:

    # Windows (PowerShell)
    venv\Scripts\Activate.ps1
    # Windows (CMD)
    venv\Scripts\activate.bat
    # Linux/Mac
    source venv/bin/activate

Instalar dependencias e executar:

    pip install -r requirements.txt
    python main.py

## Divisao de tarefas
- Guilherme: `database.py`, `logger.py`, `popular_dados.py`
- Carlos: `main.py`, `viacep.py`, relatorio RAD

## Regras(pfv vamos seguir)
- Nao alterar assinaturas das funcoes sem avisar o outro.
- Ordem dos campos em `inserir` e `atualizar`: pet, tutor, telefone, cep,
  logradouro, bairro, cidade_uf, numero, servico, data_hora.
- Cada um edita apenas os seus arquivos.

## Cuidados com o venv
1. Cada um cria o seu proprio `venv` na propria maquina (nao compartilhar a pasta).
2. Nao subir o `venv/` no Git (ja esta no `.gitignore`).
3. Nao incluir o `venv/` no zip da entrega.
4. Ao instalar uma biblioteca nova, atualizar o `requirements.txt`
   (`pip freeze > requirements.txt` ou editar na mao).
5. PowerShell bloqueando a ativacao? Rode
   `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` ou use o CMD.


## Entrega (SAVA)
Arquivo `Nome_Sobrenome_RAD.zip` contendo:
- codigo-fonte (.py)
- `agendamentos.db`
- relatorio RAD (.pdf, 1 a 2 paginas)
- `log_agendamentos.txt`