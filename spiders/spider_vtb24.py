# -*- coding: utf-8 -*-
from datetime import date, datetime
from decimal import Decimal
import re

from models import create_tables, Bank
from tools import get_site_page, save_data_to_db, send_message_to_sentry

if __name__ == '__main__':
    bank_id = 4
    bank_name = 'Втб 24'

    create_tables()
    Bank.create(bank_id=bank_id, bank_name=bank_name)

    url = 'https://www.vtb24.ru/ajax/content/'
    post_data = {
        'p':'/',
        'b':'videoSlider,financeAdvices,facilities,personalOffer,searchOffice,currency,fullWidthBanner',
        'v':'0.6687511823600023',
        'm':'default'
    }
    cookies = {
        'name': 'geoAttr',
        'value': 'syktyvkar',
        'domain': 'www.vtb24.ru'
    }
    response = get_site_page(url=url, post=post_data, cookies=cookies)

    if response:
        errors_message = ''
        try:
            jsonobject = response.doc.json
            jsonobject = jsonobject['currency']['items']
        except Exception as e:
            errors_message = 'Not json on the response or inccorect json structure.\n'
            jsonobject = None

        if jsonobject:
            item = {}
            item['bank_id'] = bank_id

            try:
                rate_date = jsonobject[0]['dateActiveFrom']
                rate_date = re.findall(r'\d+', rate_date)[0]
                item['date'] = datetime.fromtimestamp(int(rate_date) / 1000)
            except Exception as e:
                errors_message += 'No rate date on the json or incorrect json structure.\n'

            try:
                for obj in jsonobject:
                    if obj['currencyGroupAbbr'] == 'pp_rubcur_office_cash' and obj['gradation'] == 1:
                        if obj['currencyAbbr'] == 'USD':
                            item['usd_rate_buy'] = Decimal(obj['buy'].replace(',', '.'))
                            item['usd_rate_sell'] = Decimal(obj['sell'].replace(',', '.'))
                        if obj['currencyAbbr'] == 'EUR':
                            item['eur_rate_buy'] = Decimal(obj['buy'].replace(',', '.'))
                            item['eur_rate_sell'] = Decimal(obj['sell'].replace(',', '.'))
            except Exception as e:
                errors_message += 'Error with json structure.\n'
                errors_message += str(e)

            if 'usd_rate_buy' not in item:
                errors_message += 'No usd buy rate on the json.\n'

            if 'usd_rate_sell' not in item:
                errors_message += 'No usd sell rate on the json.\n'

            if 'eur_rate_buy' not in item:
                errors_message += 'No eur buy rate on the json.\n'

            if 'eur_rate_sell' not in item:
                errors_message += 'No eur sell rate on the json.\n'

            if not errors_message:
                save_data_to_db(exch_item=item)
            else:
                errors_message = bank_name + '\n' + errors_message
                send_message_to_sentry(errors_message)
        else:
            errors_message = bank_name + '\n' + errors_message
            send_message_to_sentry(errors_message)
