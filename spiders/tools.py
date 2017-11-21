from datetime import datetime
from grab import Grab
from grab.error import GrabNetworkError, GrabTimeoutError
from models import ExchangeRate


def get_site_page(url):
    try:
        g = Grab()
        g.go(url)
    except (GrabNetworkError, GrabTimeoutError) as e:
        print('Error', e)
        g = None
    except Exception as e:
        print('Unkown error', e)
        g = None
    return g


def save_data_to_db(exch_item):
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
