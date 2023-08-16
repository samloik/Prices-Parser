
from Products import Products
from ParserAbstract.Response import Response
from time import sleep
from loguru import logger

from ProductsElement import ProductsElement # TODO: после тестов удалить

class ParserSite:
    _products: Products
    _site_url: str

    def __init__(self, site_url:str):
        self.set_products(Products())
        self.set_site_url(site_url)
        # self.maxResponseNumber = 5
        # self.currentResponseNumber = 0


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

    # # return ProductFromSite main method
    # def getProductsFromSite2(self):
    #     self.products.clearProducts()
    #     isNextPage = True
    #     while isNextPage:
    #         self.dropResponseNumber()
    #         while True:
    #             response = self.getResponseFromSite()
    #             if response.isResponseOK():
    #                 break
    #             self.sleepWithTimeForNextResponse()
    #             if self.isMaxResponseNumber():
    #                 # TODO: продумать дальнейшую логику
    #                 # записать html
    #                 logger.error(f'[Error:] Максимальное количество попыток [{self.maxResponseNumber}] получить ответ от сайта достигнуто')
    #                 logger.info( f'[Error:] [{response}]')
    #                 exit(1)
    #             else:
    #                 logger.info(f'[!] Неверный ответ от сервера: попытка номер [{self.currentResponseNumber}]')
    #                 logger.info(f'[!] [{response}]')
    #         products = self.getProductsFromResponse(response)
    #         self.products += products
    #         logger.warning(f'[LEN] {len(self.products.products)=}')
    #         isNextPage = self.isNextPage(response)
    #     return self.products

    # return isNextPage = self.isNextPage(html) and page++
    def is_next_page(self, response):
        pass


    def set_sext_page(self):
        pass

    # return Response page with main method
    def get_response_from_site(self):
        pass
        # return self.getHtmlPageWithSelenium()


    # # return html page with selenium method
    # def getHtmlPageWithSelenium(self):
    #     pass
    #     # return Response("200", "") # TODO: после тестов удалить
    #
    #
    # # return html page with sessions method
    # def getHtmlPageWithSession(self):
    #     pass


    # return Products
    def get_products_from_response(self, response: Response):
        pass


    # def sleepWithTimeForNextResponse(self):
    #     sleep(2)


    # def dropResponseNumber(self):
    #     self.curentResponseNumber = 0
    #
    #
    # def isMaxResponseNumber(self):
    #     if self.maxResponseNumber > self.currentResponseNumber:
    #         self.currentResponseNumber += 1
    #         return True
    #     else:
    #         return False

