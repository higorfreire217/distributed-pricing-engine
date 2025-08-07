import requests
import logging
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep


class ExternalAPI:
    @staticmethod
    def get_asset_price(asset_code, date, retries=5, backoff=0.5):
        url = f"https://anbima-api.com/price/{asset_code}?date={date}"
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                logging.warning(f"API error: {e}")
            sleep(backoff * (2**attempt))
        raise Exception(f"API unavailable for {asset_code} on {date}")


class AuditTrail:
    @staticmethod
    def log_operation(op, price, total_value):
        # Persistir log em arquivo ou banco
        logging.info(
            f"AUDIT: Operação {op.id} {op.operation_type} {op.quantity} {op.asset_code} @ {price} valor={total_value}"
        )


class OperationRepository:
    @staticmethod
    def get_pending(fidc, date):
        return Operation.objects.filter(
            fidc=fidc, operation_date=date, status="PENDING"
        )

    @staticmethod
    def save(op):
        op.save()


class FIDCService:
    def __init__(self, fidc):
        self.fidc = fidc
        self.lock = False  # Simples, ideal usar threading.Lock

    def process_operation(self, op, date):
        try:
            price_data = ExternalAPI.get_asset_price(op.asset_code, date)
            if op.operation_type == "BUY":
                total_value = op.quantity * price_data["price"] * (1 + op.tax_rate)
                self.fidc.available_cash -= total_value
            elif op.operation_type == "SELL":
                total_value = op.quantity * price_data["price"] * (1 - op.tax_rate)
                self.fidc.available_cash += total_value
            else:
                raise Exception("Tipo de operação inválido")
            op.execution_price = price_data["price"]
            op.total_value = total_value
            op.status = "EXECUTED"
            OperationRepository.save(op)
            AuditTrail.log_operation(op, price_data["price"], total_value)
            return op
        except Exception as e:
            logging.error(f"Falha ao processar operação {op.id}: {e}")
            # Reenfileirar operação para reprocessamento
            op.status = "FAILED"
            OperationRepository.save(op)
            AuditTrail.log_operation(op, "FAILED", 0)
            return None


def process_fidc_operations(fidc_id, start_date, end_date):
    logging.basicConfig(filename="audit.log", level=logging.INFO)
    fidc = FIDC.objects.get(id=fidc_id)
    service = FIDCService(fidc)
    operations = []
    failed_ops = []
    dates = [
        start_date + timedelta(days=day)
        for day in range((end_date - start_date).days + 1)
    ]
    # Coleta todas operações pendentes
    all_ops = []
    for date in dates:
        daily_ops = OperationRepository.get_pending(fidc, date)
        all_ops.extend([(op, date) for op in daily_ops])
    # Processa em paralelo
    with ThreadPoolExecutor(max_workers=16) as executor:
        future_to_op = {
            executor.submit(service.process_operation, op, date): op
            for op, date in all_ops
        }
        for future in as_completed(future_to_op):
            result = future.result()
            if result:
                operations.append(result)
            else:
                failed_ops.append(future_to_op[future])
    # Reprocessa falhas (1 retry)
    if failed_ops:
        for op in failed_ops:
            service.process_operation(op, op.operation_date)
    fidc.save()
    send_operations_report(operations, fidc.manager_email)
    return len(operations)
