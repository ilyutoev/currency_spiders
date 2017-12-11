# -*- coding: utf-8 -*-
from datetime import date

from .models import Bank
from .tools import save_data_to_db, send_message_to_sentry
from .response_handlers import get_site_page, cb_response_scraping


def run_spider():
    bank_id = 1
    bank_name = 'Центробанк'
    Bank.create(bank_id=bank_id, bank_name=bank_name)

    today = date.today()
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(today.strftime('%d/%m/%Y'))
    response = get_site_page(url)

    item, errors_message = cb_response_scraping(response, bank_id, bank_name)

    if not errors_message:
        save_data_to_db(exch_item=item)
    else:
        send_message_to_sentry(errors_message)
