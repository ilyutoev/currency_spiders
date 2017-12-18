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

    def data_prepare(self, bank_id, scraping_function, response_file, bank_name=None):
        with open(os.path.join(self.path, response_file), 'rb') as html_response:
            grab_object = Grab(html_response.read())
            item, errors = scraping_function(grab_object, bank_id, bank_name)
            return item

    def test_cb_response_scraping(self):
        test_item = {
            'bank_id': 1,
            'eur_rate': Decimal('69.4298'),
            'usd_rate': Decimal('58.8987'),
            'date': datetime.datetime(2017, 12, 16, 0, 0)
        }

        item = self.data_prepare(
            bank_id=1,
            scraping_function=cb_response_scraping,
            response_file='centrobank.html'
        )

        self.assertEqual(test_item, item)

    def test_sevnb_response_scraping(self):
        test_item = {
            'bank_id': 2,
            'eur_rate_buy': Decimal('68.85'),
            'eur_rate_sell': Decimal('69.75'),
            'usd_rate_buy': Decimal('58.50'),
            'usd_rate_sell': Decimal('59.20'),
            'date': datetime.datetime(2017, 12, 18, 0, 0)
        }

        item = self.data_prepare(
            bank_id=2,
            scraping_function=sevnb_response_scraping,
            response_file='sevnb.html'
        )

        self.assertEqual(test_item, item)

    def test_sberbank_response_scraping(self):
        test_item = {
            'bank_id': 3,
            'eur_rate_buy': Decimal('67.81'),
            'eur_rate_sell': Decimal('71.31'),
            'usd_rate_buy': Decimal('57.19'),
            'usd_rate_sell': Decimal('60.31'),
            'date': datetime.datetime(2017, 12, 15, 0, 0)
        }

        item = self.data_prepare(
            bank_id=3,
            scraping_function=sberbank_response_scraping,
            response_file='sberbank.html'
        )

        self.assertEqual(test_item, item)

    def test_vtb24_response_scraping(self):
        test_item = {
            'bank_id': 4,
            'eur_rate_buy': Decimal('68.4500'),
            'eur_rate_sell': Decimal('69.8500'),
            'usd_rate_buy': Decimal('58.2000'),
            'usd_rate_sell': Decimal('59.4000'),
            'date': datetime.datetime(2017, 12, 18, 0, 0)
        }

        item = self.data_prepare(
            bank_id=4,
            scraping_function=vtb24_response_scraping,
            response_file='vtb24.html'
        )

        self.assertEqual(test_item, item)


if __name__ == '__main__':
    unittest.main()
