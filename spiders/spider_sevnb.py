# -*- coding: utf-8 -*-
from datetime import date, datetime
from decimal import Decimal

from models import Bank
from tools import get_site_page, save_data_to_db, send_message_to_sentry

if __name__ == '__main__':
    bank_id = 2
    bank_name = 'Северный Народный Банк'
    url = 'http://www.sevnb.ru/'

    Bank.create(bank_id=bank_id, bank_name=bank_name)

    response = get_site_page(url)

    if response:
        errors_message = ''

        if response.doc('//div[@class="block exchange"]').exists():
            exchange_block = response.doc.select('//div[@class="block exchange"]')
        else:
            exchange_block = None
            errors_message += 'No exchange block on the page.\n'

        if exchange_block:
            item = {}
            item['bank_id'] = bank_id

            if exchange_block.select('.//th[@class="ex-title"]').exists():
                rate_date = exchange_block.select('.//th[@class="ex-title"]').text().split(' ')[-1]
                item['date'] = datetime.strptime(rate_date, '%d.%m.%Y')
            else:
                errors_message += 'No rate date on the page.\n'

            if exchange_block.select('.//tr[contains(td/@class,"ex-usd")]/td[2]').exists():
                item['usd_rate_buy'] = Decimal(
                    exchange_block.select('.//tr[contains(td/@class,"ex-usd")]/td[2]').text())
            else:
                errors_message += 'No usd buy rate on the page.\n'

            if exchange_block.select('.//tr[contains(td/@class,"ex-usd")]/td[3]').exists():
                item['usd_rate_sell'] = Decimal(
                    exchange_block.select('.//tr[contains(td/@class,"ex-usd")]/td[3]').text())
            else:
                errors_message += 'No usd sell rate on the page.\n'

            if exchange_block.select('.//tr[contains(td/@class,"ex-eur")]/td[2]').exists():
                item['eur_rate_buy'] = Decimal(
                    exchange_block.select('.//tr[contains(td/@class,"ex-eur")]/td[2]').text())
            else:
                errors_message += 'No eur buy rate on the page.\n'

            if exchange_block.select('.//tr[contains(td/@class,"ex-eur")]/td[2]').exists():
                item['eur_rate_sell'] = Decimal(
                    exchange_block.select('.//tr[contains(td/@class,"ex-eur")]/td[3]').text())
            else:
                errors_message += 'No eur sell rate on the page.\n'

            if not errors_message:
                save_data_to_db(exch_item=item)
            else:
                errors_message = bank_name + '\n' + errors_message
                send_message_to_sentry(errors_message)
        else:
            errors_message = bank_name + '\n' + errors_message
            send_message_to_sentry(errors_message)
