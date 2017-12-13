# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal

from .models import Bank
from .tools import save_data_to_db, send_message_to_sentry
from .response_handlers import get_site_page


def run_spider():
    bank_id = 3
    bank_name = 'Сбербанк'
    url = 'http://www.sberbank.ru/portalserver/proxy/?pipe=shortCachePipe&url=http://localhost/rates-web/rateService/rate/current%3FregionId%3D11%26currencyCode%3D840%26currencyCode%3D978%26rateCategory%3Dbase%26rateCategory%3Dbeznal%26rateCategory%3Dcards'

    Bank.create(bank_id=bank_id, bank_name=bank_name)

    response = get_site_page(url)

    if response:
        errors_message = ''

        try:
            json_object = response.doc.json
            json_object = json_object['base']
        except Exception as e:
            errors_message = 'Not json on the response or incorrect json structure.\n'
            json_object = None

        if json_object:
            item = {'bank_id': bank_id}

            try:
                rate_date = json_object['978']['0']['activeFrom']
                item['date'] = datetime.fromtimestamp(
                    rate_date / 1000
                ).replace(hour=0, minute=0, second=0, microsecond=0)
            except Exception as e:
                errors_message += 'No rate date on the json or incorrect json structure.\n'

            try:
                item['usd_rate_buy'] = Decimal(str(json_object['840']['0']['buyValue']))
            except Exception as e:
                errors_message += 'No usd buy rate on the json or incorrect json structure.\n'

            try:
                item['usd_rate_sell'] = Decimal(str(json_object['840']['0']['sellValue']))
            except Exception as e:
                errors_message += 'No usd sell rate on the json or incorrect json structure.\n'

            try:
                item['eur_rate_buy'] = Decimal(str(json_object['978']['0']['buyValue']))
            except Exception as e:
                errors_message += 'No eur buy rate on the json or incorrect json structure.\n'

            try:
                item['eur_rate_sell'] = Decimal(str(json_object['978']['0']['sellValue']))
            except Exception as e:
                errors_message += 'No eur sell rate on the json or incorrect json structure.\n'

            if not errors_message:
                save_data_to_db(exch_item=item)
            else:
                errors_message = bank_name + '\n' + errors_message
                send_message_to_sentry(errors_message)
        else:
            errors_message = bank_name + '\n' + errors_message
            send_message_to_sentry(errors_message)
