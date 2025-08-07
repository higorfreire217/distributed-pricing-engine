from datetime import timedelta
import requests
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed


# Simula o envio de um relatório por email
def send_operations_report(operations, manager_email):
    logging.info(
        f"Relatório enviado para {manager_email} com {len(operations)} operações."
    )
    pass


# Vamos implementar o código para processar operações de compra e venda de ativos em um FIDC (Fundo de Investimento em Direitos Creditórios).
# Os dados como ainda não podem ser persistidos em um banco de dados real, vamos simular o comportamento com classes e métodos.
class FIDC:
    def __init__(self, id, available_cash, manager_email):
        self.id = id
        self.available_cash = available_cash
        self.manager_email = manager_email

    def save(self):
        # Simula o salvamento do FIDC no banco de dados
        # Não vamos implementar nada aqui por enquanto
        pass


# Essa parte do código refatorada é super importante, pois ela permite que extendamos o sistema no futuro.
class Operation:
    def __init__(self, fidc, asset_code, quantity, tax_rate, date):
        self.fidc = fidc
        self.operation_type = None
        self.asset_code = asset_code
        self.quantity = quantity
        self.tax_rate = tax_rate
        self.execution_price = None
        self.total_value = None
        self.status = "PENDING"
        self.operation_date = date
        self.process_trys = 0

    def save(self):
        # Simula o salvamento da operação no banco de dados
        pass


# BuyOperation e SellOperation herdam de Operation
# e implementam o método execute de forma específica para cada tipo de operação.
# Isso segue o princípio de responsabilidade única e o princípio aberto/fechado.
class BuyOperation(Operation):
    def __init__(self, fidc, asset_code, quantity, tax_rate, date):
        super().__init__(fidc, asset_code, quantity, tax_rate, date)
        self.operation_type = "BUY"

    def execute(self, price_data):
        total_value = self.quantity * price_data * (1 + self.tax_rate)
        self.fidc.available_cash -= total_value
        self.execution_price = price_data
        self.total_value = total_value

        # Caso seja possível executar a operação, atualizamos o status.
        # Caso contrário, mantemos como PENDING para tentar novamente depois.
        try:
            self.save()
            self.status = "EXECUTED"
        except Exception as e:
            self.status = "PENDING"
            self.process_trys += 1
            return f"Buy operation failed: {e}"
        return f"Buy operation executed: {self.quantity} {self.asset_code} @ {self.execution_price}"


class SellOperation(Operation):
    def __init__(self, fidc, asset_code, quantity, tax_rate, date):
        super().__init__(fidc, asset_code, quantity, tax_rate, date)
        self.operation_type = "SELL"

    def execute(self, price_data):
        total_value = self.quantity * price_data * (1 - self.tax_rate)
        self.fidc.available_cash += total_value
        self.execution_price = price_data
        self.total_value = total_value

        # Mesma lógica de salvamento e atualização de status da BuyOperation
        try:
            self.save()
            self.status = "EXECUTED"
        except Exception as e:
            self.status = "PENDING"
            self.process_trys += 1
            return f"Sell operation failed: {e}"
        return f"Sell operation executed: {self.quantity} {self.asset_code} @ {self.execution_price}"


# Essa classe permite que manipulemos uma coleção de operações de forma mais organizada.
# Permitindo filtros e buscas mais complexas no futuro.
class OperationsManager:
    def __init__(self, operations):
        self.operations = operations

    def filter(self, **kwargs):
        result = self.operations
        for key, value in kwargs.items():
            result = [op for op in result if getattr(op, key) == value]
        return result


# Essa classe simula um banco de dados de operações.
# Em um sistema real, isso seria substituído por consultas a um banco de dados usando um repositório ou ORM.
class Operations:
    objects = OperationsManager(
        [
            BuyOperation(FIDC(1, 1000000, "manager1@example.com"), "ABC123", 100, 0.01),
            BuyOperation(
                FIDC(2, 2000000, "manager2@example.com"), "DEF456", 200, 0.015
            ),
            BuyOperation(
                FIDC(3, 1500000, "manager3@example.com"), "GHI789", 150, 0.012
            ),
            BuyOperation(
                FIDC(4, 1200000, "manager4@example.com"), "JKL012", 120, 0.013
            ),
            SellOperation(FIDC(1, 1000000, "manager1@example.com"), "ABC123", 50, 0.01),
            SellOperation(
                FIDC(2, 2000000, "manager2@example.com"), "DEF456", 60, 0.015
            ),
            SellOperation(
                FIDC(3, 1500000, "manager3@example.com"), "GHI789", 70, 0.012
            ),
        ]
    )


# Função principal para processar operações
# Foi manterida simples para facilitar a leitura e entendimento do fluxo original.
def process_fidc_operations(fidc_id, start_date, end_date):

    # Sempre que fazemos requisições externas, devemos tratar possíveis falhas.
    # Isso evita que o sistema quebre por conta de um problema fora do nosso controle.
    # Vamos segregar a lógica de busca de preços em uma função separada.
    # Isso vai permitir que executemos operações de forma concorrente.
    def process_operation(op, current_date):
        # Verifica se a operação já foi processada 3 vezes sem sucesso.
        if op.process_trys >= 3:
            logging.error(f"Operação {op.id} falhou 3 vezes, não será mais processada.")
            op.status = "FAILED"
            return None, None

        # Busca o preço do ativo na data atual.
        try:
            asset_price = requests.get(
                f"https://anbima-api.com/price/{op.asset_code}?date={current_date}"
            )
            if asset_price.status_code == 200:
                price_data = asset_price.json()
                result = op.execute(price_data)
                logging.info(result)
                return op, price_data
        except Exception as e:
            logging.error(
                f"Erro ao buscar preço do ativo {op.asset_code} na data {current_date}: {e}"
            )
        return None, None

    fidc = FIDC.objects.get(id=fidc_id)
    operations = []

    # Busca todas as operações do período, mantida como no código original.
    for day in range((end_date - start_date).days + 1):
        current_date = start_date + timedelta(days=day)
        daily_ops = Operations.objects.filter(
            fidc=fidc, operation_date=current_date, status="PENDING"
        )

        # Aqui usamos ThreadPoolExecutor para processar as operações de forma concorrente.
        # Poderiamos usar outras abordagens para processamento assincrono como o uso de serviços de mensagería ou filas (RabbitMQ, Kafka, etc.)
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(process_operation, op, current_date) for op in daily_ops
            ]
            for future in as_completed(futures):
                op, price_data = future.result()
                if op and price_data:
                    # Log para auditoria
                    logging.info(
                        f"Operação {op.id} executada: {op.operation_type} {op.quantity} {op.asset_code} @ {price_data['price']}"
                    )
                    operations.append(op)
                    fidc.save()

    # Envia relatório por email
    send_operations_report(operations, fidc.manager_email)
    return len(operations)
