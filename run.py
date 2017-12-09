from spiders import spider_cb, spider_sevnb, spider_sberbank, spider_vtb24

if __name__ == '__main__':
    spider_cb.run_spider()
    spider_sevnb.run_spider()
    spider_sberbank.run_spider()
    spider_vtb24.run_spider()
