from .models import Bank, save_data_to_db
from .response_handlers import get_site_page
from .logging_handlers import send_message_to_sentry


def run_spider(bank_id, bank_name, scraping_function, request_url, request_post, request_cookies):
    Bank.create(bank_id=bank_id, bank_name=bank_name)

    response = get_site_page(request_url, request_post, request_cookies)

    item, errors_message = scraping_function(response, bank_id, bank_name)

    if not errors_message:
        save_data_to_db(exch_item=item)
    else:
        send_message_to_sentry(errors_message)
