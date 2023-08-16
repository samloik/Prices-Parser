
from Products import Products
from ParserAbstract.Response import Response
from time import sleep
from loguru import logger

from ProductsElement import ProductsElement # TODO: после тестов удалить

class ParserSite:
    _products: Products
    _site_url: str

    _next_response_pause_time: float


    def __init__(self, site_url:str):
        self.set_products(Products())
        self.set_site_url(site_url)
        self.set_next_page_pause_time(0)        # время паузы перед переходом на след. страницу

        # self.maxResponseNumber = 5
        # self.currentResponseNumber = 0

    def set_next_page_pause_time(self, time=0):
        # устанавливаем время паузы перед переключением страницы
        self._next_page_pause_time = time

    def get_next_page_pause_time(self):
        return self._next_page_pause_time


    def set_site_url(self, site_url):
        self._site_url = site_url

    def get_site_url(self):
        return self._site_url

    def get_products(self):
        return self._products

    def set_products(self, products: Products):
        self._products = products

    def __len__(self):
        return len(self.get_products())


    # return ProductFromSite main method
    def get_products_from_site(self):
        # self.get_products().clear_products()
        all_products = self.get_products()
        all_products.clear_products()
        is_next_page = True
        while is_next_page:
            response = self.get_response_from_site()
            products = self.get_products_from_response(response)
            # get_producs = self.get_products()
            all_products += products
            # logger.warning(f'[LEN] {len(self.products.products)=}')
            logger.warning(f'[LEN] {len(products)=}')
            is_next_page = self.is_next_page(response)
            if is_next_page:
                self.set_next_page()
        return all_products


    def is_next_page(self, response):
        pass


    def set_sext_page(self):
        pass

    # return Response page with main method
    def get_response_from_site(self):
        pass
        # return self.getHtmlPageWithSelenium()



    # return Products
    def get_products_from_response(self, response: Response):
        pass



