import unittest
import os
from decimal import Decimal
import datetime
from grab import Grab
from spiders.response_handlers import cb_response_scraping,sberbank_response_scraping, vtb24_response_scraping,\
    sevnb_response_scraping


class ResponseScrapingTestCase(unittest.TestCase):
    def setUp(self):
        self.path = 'test_cases'

    def test_cb_response_scraping(self):
        bank_id = 1
        bank_name = 'Центробанк'
        response_path = 'centrobank.html'
        test_item = {
            'bank_id': 1,
            'eur_rate': Decimal('69.4298'),
            'usd_rate': Decimal('58.8987'),
            'date': datetime.datetime(2017, 12, 16, 0, 0)
        }

        with open(os.path.join(self.path, response_path), 'rb') as html_response:
            grab_object = Grab(html_response.read())
            item, errors = cb_response_scraping(grab_object, bank_id, bank_name)

        self.assertEqual(test_item, item)

    def test_sevnb_response_scraping(self):
        bank_id = 2
        bank_name = 'Северный Народный Банк'
        response_path = 'sevnb.html'
        test_item = {
            'bank_id': 2,
            'eur_rate_buy': Decimal('68.85'),
            'eur_rate_sell': Decimal('69.75'),
            'usd_rate_buy': Decimal('58.50'),
            'usd_rate_sell': Decimal('59.20'),
            'date': datetime.datetime(2017, 12, 18, 0, 0)
        }

        with open(os.path.join(self.path, response_path), 'rb') as html_response:
            grab_object = Grab(html_response.read())
            item, errors = sevnb_response_scraping(grab_object, bank_id, bank_name)

        self.assertEqual(test_item, item)

    def test_sberbank_response_scraping(self):
        bank_id = 3
        bank_name = 'Сбербанк'
        response_path = 'sberbank.html'
        test_item = {
            'bank_id': 3,
            'eur_rate_buy': Decimal('67.81'),
            'eur_rate_sell': Decimal('71.31'),
            'usd_rate_buy': Decimal('57.19'),
            'usd_rate_sell': Decimal('60.31'),
            'date': datetime.datetime(2017, 12, 15, 0, 0)
        }

        with open(os.path.join(self.path, response_path), 'rb') as html_response:
            grab_object = Grab(html_response.read())
            item, errors = sberbank_response_scraping(grab_object, bank_id, bank_name)

        self.assertEqual(test_item, item)

    def test_vtb24_response_scraping(self):
        bank_id = 4
        bank_name = 'Втб 24'
        response_path = 'vtb24.html'
        test_item = {
            'bank_id': 4,
            'eur_rate_buy': Decimal('68.4500'),
            'eur_rate_sell': Decimal('69.8500'),
            'usd_rate_buy': Decimal('58.2000'),
            'usd_rate_sell': Decimal('59.4000'),
            'date': datetime.datetime(2017, 12, 18, 0, 0)
        }

        with open(os.path.join(self.path, response_path), 'rb') as html_response:
            grab_object = Grab(html_response.read())
            item, errors = vtb24_response_scraping(grab_object, bank_id, bank_name)

        self.assertEqual(test_item, item)


if __name__ == '__main__':
    unittest.main()
