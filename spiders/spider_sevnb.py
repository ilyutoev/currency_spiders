# -*- coding: utf-8 -*-
from datetime import date, datetime
from decimal import Decimal

from models import create_tables, Bank
from tools import process_request, process_response


if __name__ == '__main__':
    create_tables()
    bank_id = 2
    Bank.create(bank_id=bank_id, bank_name="Северный Народный Банк")

    url = 'http://www.sevnb.ru/'

    response = process_request(url)

    if response:
        if response.doc('//div[@class="block exchange"]').exists():
            exchange_block = response.doc.select('//div[@class="block exchange"]')
        else:
            exchange_block = None
            print('No exchange block on the page')

        if exchange_block:
            if exchange_block.select('.//th[@class="ex-title"]').exists():
                rate_date = exchange_block.select('.//th[@class="ex-title"]').text().split(' ')[-1]
                rate_date = datetime.strptime(rate_date, '%d.%m.%Y')
            else:
                print('No rate date on the page')

            item = {}
            if exchange_block.select('.//tr[contains(td/@class,"ex-usd")]/td[2]').exists():
                item['usd_rate_buy'] = Decimal(exchange_block.select('.//tr[contains(td/@class,"ex-usd")]/td[2]').text())
            else:
                print('No usd buy rate on the page')

            if exchange_block.select('.//tr[contains(td/@class,"ex-usd")]/td[3]').exists():
                item['usd_rate_sell'] = Decimal(exchange_block.select('.//tr[contains(td/@class,"ex-usd")]/td[3]').text())
            else:
                print('No usd sell rate on the page')

            if exchange_block.select('.//tr[contains(td/@class,"ex-eur")]/td[2]').exists():
                item['eur_rate_buy'] = Decimal(exchange_block.select('.//tr[contains(td/@class,"ex-eur")]/td[2]').text())
            else:
                print('No eur buy rate on the page')

            if exchange_block.select('.//tr[contains(td/@class,"ex-eur")]/td[2]').exists():
                item['eur_rate_sell'] = Decimal(exchange_block.select('.//tr[contains(td/@class,"ex-eur")]/td[3]').text())
            else:
                print('No eur sell rate on the page')

            process_response(bank_id=bank_id, date=rate_date, exch_item=item)
