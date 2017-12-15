from decimal import Decimal
from datetime import datetime
from grab import Grab
from .tools import send_message_to_sentry


def get_site_page(url, post=None, cookies=None):
    try:
        g = Grab()
        if cookies:
            g.cookies.set(**cookies)
        if post:
            g.go(url, post=post)
        else:
            g.go(url)
    except Exception as e:
        send_message_to_sentry(str(e))
        g = None
    return g


def get_exchange_block_from_html(html_response, xpath, errors_string):
    if html_response.doc.select(xpath).exists():
        html_exchange_block = html_response.doc.select(xpath)
    else:
        html_exchange_block = None
        errors_string += 'No exchange block on the page.\n'
    return html_exchange_block, errors_string


def get_currency_rate_from_html(html_response, xpath, errors_string, currency):
    if html_response.doc.select(xpath).exists():
        currency_rate = Decimal(html_response.doc.select(xpath).text().replace(',', '.'))
    else:
        currency_rate = None
        errors_string += 'No {} rate on the page.\n'.format(currency)

    return currency_rate, errors_string


def get_currency_rate_from_exchange_block(html_response, xpath, errors_string, currency):
    if html_response.select(xpath).exists():
        currency_rate = Decimal(html_response.select(xpath).text().replace(',', '.'))
    else:
        currency_rate = None
        errors_string += 'No {} rate on the page.\n'.format(currency)

    return currency_rate, errors_string


def cb_response_scraping(response, bank_id, bank_name):
    errors_message = ''

    if response:
        item = {'bank_id': bank_id}

        if response.doc('//valcurs').exists():
            rate_date = response.doc.select('//valcurs').attr('date')
            item['date'] = datetime.strptime(rate_date, '%d.%m.%Y')
        else:
            errors_message += 'No rate date on the page.\n'

        item['usd_rate'], errors_message = get_currency_rate_from_html(
            html_response=response,
            xpath='//valute[@id="R01235"]/value',
            errors_string=errors_message,
            currency='usd'
        )

        item['eur_rate'], errors_message = get_currency_rate_from_html(
            html_response=response,
            xpath='//valute[@id="R01239"]/value',
            errors_string=errors_message,
            currency='eur'
        )
    else:
        item = None
        errors_message = 'No response.'

    if errors_message:
        errors_message = bank_name + '\n' + errors_message

    return item, errors_message


def sevnb_response_scraping(response, bank_id, bank_name):
    errors_message = ''

    if response:
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
        else:
            item = None
            errors_message += 'No exchange block.\n'
    else:
        item = None
        errors_message = 'No response.\n'

    if errors_message:
        errors_message = bank_name + '\n' + errors_message

    return item, errors_message


def sberbank_response_scraping(response, bank_id, bank_name):
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

    else:
        item = None
        errors_message = 'No json response.\n'

    if errors_message:
        errors_message = bank_name + '\n' + errors_message

    return item, errors_message
