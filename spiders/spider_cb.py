# -*- coding: utf-8 -*-
from datetime import date, datetime
from decimal import Decimal

from models import create_tables, Bank
from tools import process_request, process_response


if __name__ == '__main__':
    create_tables()
    bank_id = 1
    Bank.create(bank_id=bank_id, bank_name="Центробанк")

    today = date.today()
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}/{}/{}'.format(today.day, today.month, today.year)

    response = process_request(url)

    if response:
        if response.doc('//valcurs').exists():
            rate_date = response.doc.select('//valcurs').attr('date')
            rate_date = datetime.strptime(rate_date, '%d.%m.%Y')
        else:
            print('No rate date on the page')

        item = {}
        if response.doc('//valute[@id="R01235"]/value').exists():
            item['usd_rate'] = Decimal(response.doc.select('//valute[@id="R01235"]/value').text().replace(',', '.'))
        else:
            print('No usd rate on the page')

        if response.doc('//valute[@id="R01239"]/value').exists():
            item['eur_rate'] = Decimal(response.doc.select('//valute[@id="R01239"]/value').text().replace(',', '.'))
        else:
            print('No eur rate on the page')

        process_response(bank_id=bank_id, date=rate_date, exch_item=item)
