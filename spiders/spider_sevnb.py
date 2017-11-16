# -*- coding: utf-8 -*-
from models import create_tables, Bank, ExchangeRate
from datetime import date, datetime
from grab import Grab


create_tables()
bank_id = 2
Bank.create(bank_id=bank_id, bank_name="Северный Народный Банк")

g = Grab()
url = 'http://www.sevnb.ru/'
try:
    g.go(url)
except Exception as e:
    pass
    # TODO обработка ошибок

exchange_block = g.doc.select('//div[@class="block exchange"]')
rate_date = exchange_block.select('.//th[@class="ex-title"]').text().split(' ')[-1]

usd_item = {'currency': 'u'}
usd_item['bank_id'] = bank_id
usd_item['type'] = 'b'
usd_item['date'] = datetime.strptime(rate_date, '%d.%m.%Y')
usd_item['rate'] = float(exchange_block.select('.//tr[contains(td/@class,"ex-usd")]/td[2]').text())
usd_item['scraping_date'] = datetime.now()
ExchangeRate.create(usd_item)

usd_item['type'] = 's'
usd_item['rate'] = float(exchange_block.select('.//tr[contains(td/@class,"ex-usd")]/td[3]').text())
ExchangeRate.create(usd_item)


eur_item = {'currency': 'e'}
eur_item['bank_id'] = bank_id
eur_item['type'] = 'b'
eur_item['date'] = datetime.strptime(rate_date, '%d.%m.%Y')
eur_item['rate'] = float(exchange_block.select('.//tr[contains(td/@class,"ex-eur")]/td[2]').text())
eur_item['scraping_date'] = datetime.now()
ExchangeRate.create(eur_item)

eur_item['type'] = 's'
eur_item['rate'] = float(exchange_block.select('.//tr[contains(td/@class,"ex-eur")]/td[3]').text())
ExchangeRate.create(eur_item)
