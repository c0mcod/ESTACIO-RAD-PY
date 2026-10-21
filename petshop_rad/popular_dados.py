"""Guilherme - Gera dados ficticios com Faker para testes (nao faz parte do app)."""
import faker
from faker import Faker

from database import criar_tabela, inserir
from logger import registrar_log

fake = Faker("pt_BR")
SERVICOS = ["Banho", "Tosa", "Banho e Tosa", "Consulta Veterinária", "Vacinação", "Corte de Unha"]


def popular(qtd=10):
    try:
        criar_tabela()
        print(f"Iniciando a geração de {qtd} registros de teste...")
        
        for _ in range(qtd):
            # Gerando dados fictícios padronizados para o Brasil
            pet = fake.first_name()  # Usando o primeiro nome de pessoa como nome de pet
            tutor = fake.name()
            telefone = fake.cellphone_number()
            cep = fake.postcode()
            logradouro = fake.street_name()
            bairro = fake.bairro()
            cidade_uf = f"{fake.city()} / {fake.estado_sigla()}"
            numero = fake.building_number()
            servico = fake.random_element(elements=SERVICOS)
            # Data fictícia nos próximos 30 dias, formatada
            data_hora = fake.future_datetime(end_date="+30d").strftime("%d/%m/%Y %H:%M")
            
            # A própria função inserir vai cuidar da limpeza, log e abertura/fechamento do banco
            inserir(pet, tutor, telefone, cep, logradouro, bairro, cidade_uf, numero, servico, data_hora)
            # Registro de log para cada inserção, detalhando os dados gerados
            registrar_log("INFO", f"Agendamento fictício criado: Pet={pet}, Tutor={tutor}, Serviço={servico}, Data/Hora={data_hora}")
            
        print(f"Concluído! {qtd} agendamentos foram criados em 'agendamentos.db'.")
    except Exception as e:
        erro_msg = f"Falha inesperada ao popular dados: {e}"
        print(erro_msg)
        # Opcional: registrar esse erro catastrófico no seu log de auditoria
        registrar_log("ERRO_SCRIPT", erro_msg)

if __name__ == "__main__":
    popular()
