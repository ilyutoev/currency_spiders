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
