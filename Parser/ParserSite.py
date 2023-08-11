
from Products import Products
from Response import Response
from time import sleep
from loguru import logger

from ProductsElement import ProductsElement # TODO: после тестов удалить

class ParserSite:
    products: Products
    siteUrl: str

    def __init__(self, siteUrl:str):
        self.products = Products()
        self.siteUrl = siteUrl
        # self.maxResponseNumber = 5
        # self.currentResponseNumber = 0


    # return ProductFromSite main method
    def getProductsFromSite(self):
        self.products.clearProducts()
        isNextPage = True
        while isNextPage:
            response = self.getResponseFromSite()
            products = self.getProductsFromResponse(response)
            self.products += products
            logger.warning(f'[LEN] {len(self.products.products)=}')
            isNextPage = self.isNextPage(response)
            self.setNextPage()
        return self.products

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
    def isNextPage(self, response):
        pass


    def setNextPage(self):
        pass

    # return Response page with main method
    def getResponseFromSite(self):
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
    def getProductsFromResponse(self, response: Response):
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

