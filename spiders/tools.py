from datetime import datetime
from grab import Grab
from grab.error import GrabNetworkError, GrabTimeoutError
from models import ExchangeRate


def process_request(url):
    try:
        g = Grab()
        g.go(url)
    except (GrabNetworkError, GrabTimeoutError) as e:
        print('Error', e)
        g = None
    return g


def process_response(bank_id, date, exch_item):
    item = {}
    item['bank_id'] = bank_id
    item['date'] = date
    item['scraping_date'] = datetime.now()

    for cur in ['usd', 'eur']:
        item['currency'] = cur

        if bank_id == 1:
            item['rate'] = exch_item['%s_rate' % cur]
            item['type'] = None
            ExchangeRate.create(item)
        else:
            for type in ['buy', 'sell']:
                item['type'] = type
                item['rate'] = exch_item['%s_rate_%s' % (cur, type)]
                print(item)
                ExchangeRate.create(item)
