# -*- coding: utf-8 -*-
from datetime import date, datetime
from decimal import Decimal

from models import Bank
from tools import save_data_to_db, send_message_to_sentry
from response_handlers import get_site_page

if __name__ == '__main__':
    bank_id = 1
    bank_name = 'Центробанк'
    today = date.today()
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(today.strftime('%d/%m/%Y'))

    Bank.create(bank_id=bank_id, bank_name=bank_name)

    response = get_site_page(url)

    if response:
        errors_message = ''
        item = {}
        item['bank_id'] = bank_id

        if response.doc('//valcurs').exists():
            rate_date = response.doc.select('//valcurs').attr('date')
            item['date'] = datetime.strptime(rate_date, '%d.%m.%Y')
        else:
            errors_message += 'No rate date on the page.\n'

        if response.doc('//valute[@id="R01235"]/value').exists():
            item['usd_rate'] = Decimal(response.doc.select('//valute[@id="R01235"]/value').text().replace(',', '.'))
        else:
            errors_message += 'No usd rate on the page.\n'

        if response.doc('//valute[@id="R01239"]/value').exists():
            item['eur_rate'] = Decimal(response.doc.select('//valute[@id="R01239"]/value').text().replace(',', '.'))
        else:
            errors_message += 'No eur rate on the page.\n'

        if not errors_message:
            save_data_to_db(exch_item=item)
        else:
            errors_message = bank_name + '\n' + errors_message
            send_message_to_sentry(errors_message)
