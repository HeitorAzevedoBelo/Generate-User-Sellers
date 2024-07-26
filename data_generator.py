import json
import random
import logging
from math import trunc
from datetime import datetime, timedelta
from typing import List, Dict, Union
from colorama import Fore, Style

class DataGenerator:
    def __init__(self, config: dict):
        """
        Inicializa a classe DataGenerator com as configurações fornecidas.

        Parâmetros:
        config (dict): Dicionário de configuração carregado do arquivo config.json.
        """
        self.sellers = config["SELLERS"]
        self.mcc_dict = config["MCC_DICT"]
        self.transaction_types = config["TRANSACTION_TYPES"]

    def create_number(self, length: int = 1, type_r: str = 'str') -> Union[str, int, float]:
        """
        Gera um número aleatório.

        Parâmetros:
        length (int): O comprimento do número a ser gerado.
        type_r (str): Tipo de número a ser gerado ('str' para string, 'decimal' para decimal).

        Retorno:
        str ou int ou float: Número gerado como string, inteiro ou decimal.
        """
        logging.info(f'Creating number of length {length} and type {type_r}')
        if type_r == 'decimal':
            return random.randint(10, 200) + round(random.random(), 2)
        number = ''.join(str(trunc(random.random() * 10)) for _ in range(length))
        return number if type_r == 'str' else int(number)

    def generate_random_datetime(self, days: int) -> datetime:
        """
        Gera uma data e hora aleatória dentro de um intervalo de dias.

        Parâmetros:
        days (int): O número de dias para trás a partir de hoje para o intervalo.

        Retorno:
        datetime: Data e hora geradas.
        """
        logging.info(f'Generating random datetime within {days} days range')
        now = datetime.now()
        past_date = now - timedelta(days=days)
        random_timestamp = random.randint(int(past_date.timestamp()), int(now.timestamp()))
        return datetime.fromtimestamp(random_timestamp)

    def generate_transactions(self, n: int) -> List[Dict]:
        """
        Gera uma lista de transações aleatórias.

        Parâmetros:
        n (int): O número de transações a serem geradas.

        Retorno:
        list: Lista de dicionários representando transações.
        """
        logging.info(f'Generating {n} transactions')
        transactions = []
        for _ in range(n):
            pos_seller = random.randint(0, len(self.sellers) - 1)
            mcc = random.randint(0, len(self.mcc_dict) - 1)
            transaction = {
                'transactionId': self.create_number(18),
                'seller_id': self.sellers[pos_seller],
                'seller_name': f'SELLER{pos_seller}',
                'mcc': self.mcc_dict[mcc]['mcc'],
                'mccCategory': self.mcc_dict[mcc]['category'],
                'value': self.create_number(type_r='decimal'),
                'date': self.generate_random_datetime(60),
                'type': self.transaction_types[random.randint(0, len(self.transaction_types) - 1)]
            }
            transactions.append(transaction)
        return transactions

    def generate_user(self) -> Dict:
        """
        Gera um usuário aleatório com transações.

        Retorno:
        dict: Dicionário representando um usuário.
        """
        logging.info('Generating user')
        seller_id = self.create_number(6)
        self.sellers.append(seller_id)
        user = {
            'consumer_id': self.create_number(18),
            'age': random.randint(16, 99),
            'exact_distance': random.randint(1000, 10000),
            'score': random.randint(100, 1000),
            'seller_id': seller_id,
            'transactions': self.generate_transactions(random.randint(0, 4))
        }
        return user

    @staticmethod
    def json_serial(obj):
        """
        Serializa objetos não padrão para JSON.

        Parâmetros:
        obj: O objeto a ser serializado.

        Retorno:
        str: Representação do objeto em formato ISO 8601.

        Lança:
        TypeError: Se o objeto não for serializável.
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f'Type {obj.__class__.__name__} not serializable')

    @staticmethod
    def pretty_print_user(user: Dict):
        """
        Imprime um usuário de forma bonita.

        Parâmetros:
        user (dict): O dicionário representando um usuário.
        """
        def custom_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f'Type {obj.__class__.__name__} not serializable')
        
        user_json = json.dumps(user, indent=4, ensure_ascii=False, default=custom_serializer)
        print(Fore.CYAN + user_json + Style.RESET_ALL)
