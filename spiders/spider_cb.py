# -*- coding: utf-8 -*-
from models import create_tables, Bank, ExchangeRate
from datetime import date, datetime
from grab import Grab


create_tables()
bank_id = 1
Bank.create(bank_id=bank_id, bank_name="Центробанк")

today = date.today()
url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}/{}/{}'.format(today.day, today.month, today.year)
g = Grab()

try:
    g.go(url)
except Exception as e:
    pass
    # TODO обработка ошибок

usd_item = {'currency': 'u'}
usd_item['bank_id'] = bank_id
rate_date = g.doc.select('//valcurs').attr('date')
usd_item['date'] = datetime.strptime(rate_date, '%d.%m.%Y')
usd_item['rate'] = float(g.doc.select('//valute[@id="R01235"]/value').text().replace(',', '.'))
usd_item['scraping_date'] = datetime.now()
ExchangeRate.create(usd_item)

eur_item = {'currency': 'e'}
eur_item['bank_id'] = bank_id
eur_item['date'] = datetime.strptime(rate_date, '%d.%m.%Y')
eur_item['rate'] = float(g.doc.select('//valute[@id="R01239"]/value').text().replace(',', '.'))
eur_item['scraping_date'] = datetime.now()
ExchangeRate.create(eur_item)

