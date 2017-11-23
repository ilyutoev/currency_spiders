from datetime import datetime
from grab import Grab
from raven import Client
from models import ExchangeRate
import settings


def get_site_page(url, post=None, cookies=None):
    try:
        g = Grab()
        if cookies:
            g.cookies.set(**cookies)
        if post:
            g.go(url, post=post)
        else:
            g.go(url)
    except Exception as e:
        send_message_to_sentry(str(e))
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


def send_message_to_sentry(msg):
    client = Client(settings.SENTRY_PROJECT_URL)
    client.captureMessage(msg)
    # client.captureException()
