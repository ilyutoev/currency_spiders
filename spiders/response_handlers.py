from decimal import Decimal
from grab import Grab
from tools import send_message_to_sentry


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
    if html_response.doc(xpath).exists():
        html_exchange_block = html_response.doc.select(xpath)
    else:
        html_exchange_block = None
        errors_string += 'No exchange block on the page.\n'
    return html_exchange_block, errors_string


def get_currency_rate_from_html(html_response, xpath, errors_string, currency):
    if html_response.select(xpath).exists():
        currency_rate = Decimal(html_response.select(xpath).text())
    else:
        currency_rate = None
        errors_string += 'No {} rate on the page.\n'.format(currency)

    return currency_rate, errors_string