from datetime import date
from spiders.common_spider import run_spider
from spiders.response_handlers import cb_response_scraping
from spiders import spider_cb, spider_sevnb, spider_sberbank, spider_vtb24


if __name__ == '__main__':

    run_spider(
        bank_id=1,
        bank_name='Центробанк',
        scraping_function=cb_response_scraping,
        request_url='http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(date.today().strftime('%d/%m/%Y')),
        request_post=None,
        request_cookies=None
    )

    # spider_sevnb.run_spider()
    # spider_sberbank.run_spider()
    # spider_vtb24.run_spider()
