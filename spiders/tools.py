from datetime import datetime
from raven import Client
from .models import ExchangeRate
from .settings import SENTRY_PROJECT_URL


def save_data_to_db(exch_item):
    """
    Get exchange item and create two db lines for Centrobank:
        usd
        eur

    and four db lines for other banks:
        usd sell
        usd buy
        eur sell
        eur buy.
    """

    item = {}
    item['bank_id'] = exch_item['bank_id']
    item['date'] = exch_item['date']
    item['scraping_date'] = datetime.now()

    for cur in ['usd', 'eur']:
        item['currency'] = cur

        if item['bank_id'] == 1:
            item['rate'] = exch_item['%s_rate' % cur]
            item['type'] = None
            ExchangeRate.create(item)
        else:
            for type in ['buy', 'sell']:
                item['type'] = type
                item['rate'] = exch_item['%s_rate_%s' % (cur, type)]
                ExchangeRate.create(item)


def send_message_to_sentry(msg):
    client = Client(SENTRY_PROJECT_URL)
    client.captureMessage(msg)

