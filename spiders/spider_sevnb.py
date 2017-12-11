# -*- coding: utf-8 -*-
from .models import Bank
from .tools import save_data_to_db, send_message_to_sentry
from .response_handlers import get_site_page, sevnb_response_scraping


def run_spider():
    bank_id = 2
    bank_name = 'Северный Народный Банк'
    Bank.create(bank_id=bank_id, bank_name=bank_name)

    url = 'http://www.sevnb.ru/'
    response = get_site_page(url)

    item, errors_message = sevnb_response_scraping(response, bank_id, bank_name)

    if not errors_message:
        save_data_to_db(exch_item=item)
    else:
        send_message_to_sentry(errors_message)
