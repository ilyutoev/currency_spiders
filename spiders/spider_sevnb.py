# -*- coding: utf-8 -*-
from datetime import datetime

from .models import Bank
from .tools import save_data_to_db, send_message_to_sentry
from .response_handlers import get_site_page, get_exchange_block_from_html, get_currency_rate_from_exchange_block


def run_spider():
    bank_id = 2
    bank_name = 'Северный Народный Банк'
    url = 'http://www.sevnb.ru/'

    Bank.create(bank_id=bank_id, bank_name=bank_name)

    response = get_site_page(url)

    if response:
        errors_message = ''

        exchange_block, errors_message = get_exchange_block_from_html(
            html_response=response,
            xpath='//div[@class="block exchange"]',
            errors_string=errors_message
        )

        if exchange_block:
            item = {'bank_id': bank_id}

            if exchange_block.select('.//th[@class="ex-title"]').exists():
                rate_date = exchange_block.select('.//th[@class="ex-title"]').text().split(' ')[-1]
                item['date'] = datetime.strptime(rate_date, '%d.%m.%Y')
            else:
                errors_message += 'No rate date on the page.\n'

            item['usd_rate_buy'], errors_message = get_currency_rate_from_exchange_block(
                html_response=exchange_block,
                xpath='.//tr[contains(td/@class,"ex-usd")]/td[2]',
                errors_string=errors_message,
                currency='usd buy'
            )

            item['usd_rate_sell'], errors_message = get_currency_rate_from_exchange_block(
                html_response=exchange_block,
                xpath='.//tr[contains(td/@class,"ex-usd")]/td[3]',
                errors_string=errors_message,
                currency='usd sell'
            )

            item['eur_rate_buy'], errors_message = get_currency_rate_from_exchange_block(
                html_response=exchange_block,
                xpath='.//tr[contains(td/@class,"ex-eur")]/td[2]',
                errors_string=errors_message,
                currency='eur buy'
            )

            item['eur_rate_sell'], errors_message = get_currency_rate_from_exchange_block(
                html_response=exchange_block,
                xpath='.//tr[contains(td/@class,"ex-eur")]/td[3]',
                errors_string=errors_message,
                currency='eur sell'
            )

            if not errors_message:
                save_data_to_db(exch_item=item)
            else:
                errors_message = bank_name + '\n' + errors_message
                send_message_to_sentry(errors_message)
        else:
            errors_message = bank_name + '\n' + errors_message
            send_message_to_sentry(errors_message)
