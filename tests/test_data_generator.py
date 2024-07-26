import unittest
from data_generator import DataGenerator
from datetime import datetime
import json

class TestDataGenerator(unittest.TestCase):

    def setUp(self):
        self.config = {
            "SELLERS": ["221512"],
            "MCC_DICT": [
                {'mcc': 5422, 'category': 'AÇOUGUEIRO'},
                {'mcc': 5462, 'category': 'PADARIA'},
                {'mcc': 5499, 'category': 'LOJA DE ALIMENTOS'}
            ],
            "TRANSACTION_TYPES": ['QRCODE', 'PIX', 'CARD']
        }
        self.generator = DataGenerator(self.config)

    def test_create_number_str(self):
        number = self.generator.create_number(length=6, type_r='str')
        self.assertEqual(len(number), 6)
        self.assertTrue(number.isdigit())

    def test_create_number_decimal(self):
        number = self.generator.create_number(type_r='decimal')
        self.assertIsInstance(number, float)

    def test_generate_random_datetime(self):
        random_date = self.generator.generate_random_datetime(60)
        self.assertIsInstance(random_date, datetime)

    def test_generate_transactions(self):
        transactions = self.generator.generate_transactions(5)
        self.assertEqual(len(transactions), 5)

    def test_generate_user(self):
        user = self.generator.generate_user()
        self.assertIn('consumer_id', user)
        self.assertIn('transactions', user)

    def test_json_serial(self):
        now = datetime.now()
        serial = self.generator.json_serial(now)
        self.assertEqual(serial, now.isoformat())

    def test_pretty_print_user(self):
        user = self.generator.generate_user()
        try:
            self.generator.pretty_print_user(user)
        except Exception as e:
            self.fail(f"pretty_print_user raised {e}")

if __name__ == "__main__":
    unittest.main()
