from datetime import date
from spiders.common_spider import run_spider
from spiders.response_handlers import cb_response_scraping, sevnb_response_scraping, sberbank_response_scraping


if __name__ == '__main__':

    run_spider(
        bank_id=1,
        bank_name='Центробанк',
        scraping_function=cb_response_scraping,
        request_url='http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(date.today().strftime('%d/%m/%Y')),
        request_post=None,
        request_cookies=None
    )

    run_spider(
        bank_id=2,
        bank_name='Северный Народный Банк',
        scraping_function=sevnb_response_scraping,
        request_url='http://www.sevnb.ru/',
        request_post=None,
        request_cookies=None
    )

    run_spider(
        bank_id=3,
        bank_name='Сбербанк',
        scraping_function=sberbank_response_scraping,
        request_url='http://www.sberbank.ru/portalserver/proxy/?pipe=shortCachePipe&'
                    'url=http://localhost/rates-web/rateService/rate/current%3FregionId%3D11%26currencyCode%3D840%26'
                    'currencyCode%3D978%26rateCategory%3Dbase%26rateCategory%3Dbeznal%26rateCategory%3Dcards',
        request_post=None,
        request_cookies=None
    )


    # spider_vtb24.run_spider()
