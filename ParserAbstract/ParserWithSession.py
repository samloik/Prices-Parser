
from Products import Products
from ParserAbstract.ParserSite import ParserSite
from ParserAbstract.Response import Response

from ProductsElement import ProductsElement
from time import sleep
# from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from bs4 import BeautifulSoup
import requests


class ParserWithSession(ParserSite): # rename to SeleniumParser

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl)
        self.currentPage = 0
        self.session = requests.Session()
        # self.NEXT_PAGE_PAUSE_TIME = 0
        self.setNextPagePauseTime(0)

        self.maxResponseNumber = 5
        self.currentResponseNumber = 0
        self.NEXT_RESPONSE_PAUSE_TIME = 1


    # # return isNextPage = self.checkForNextPage(html)
    # def isNextPage(self, response: Response):
    #
    #     soup = BeautifulSoup(response.html, 'lxml')
    #
    #     pageNext = soup.find_all(class_='page-next')
    #
    #     if len(pageNext) > 0:
    #         logger.info(f'[{self.currentPage}] вызываем следующую страницу')
    #         self.currentPage += 1
    #         return True
    #     else:
    #         logger.info(f'[{self.currentPage}] это была последняя страница')
    #         return False

    def setNextPagePauseTime(self, time):
        self.NEXT_PAGE_PAUSE_TIME = time


    def setNextPage(self):
        self.currentPage += 1


    def getHtmlPage(self, url):
        html = ""
        try:
            res = self.session.get(url)
            html = res.content
            sleep(self.NEXT_PAGE_PAUSE_TIME)   # TODO отрегулировать параметр времени
            # response = Response("200", html, None)
            response = Response( str(res.status_code), html, None)
        except Exception as Err:
            logger.error(Err)
            response = Response( str(res.status_code), None, str(Err))

        return response


    # return html page with main method
    def getResponseFromSite(self):
        self.dropResponseNumber()
        while True:
            response = self.getResponseFromSiteWithSession()
            if response.isResponseOK():
                break
            self.sleepWithTimeForNextResponse()
            if self.isMaxResponseNumber():
                # TODO: продумать дальнейшую логику
                # записать html
                logger.error(
                    f'[Error:] Максимальное количество попыток [{self.maxResponseNumber}] получить ответ от сайта достигнуто')
                logger.info(f'[Error:] [{response=}]')
                exit(1)
            else:
                logger.warning(f'[!] Неверный ответ от сервера: попытка номер [{self.currentResponseNumber}]')
                logger.info(f'[!] [{response=}]')
        return response



    # return html page with main method
    def getResponseFromSiteWithSession(self):
        logger.info('Пытаемся получить ответ от сайта')

        url = self.siteUrl + str(self.currentPage)
        response = self.getHtmlPage(url)

        # инфо блок
        if response.isResponseOK():
            logger.info(f'Страница {self.currentPage} получена без ошибок')
        else:
            logger.warning(f'Страница {self.currentPage} получена c ошибкой')

        return response

    def dropResponseNumber(self):
        self.curentResponseNumber = 0


    def isMaxResponseNumber(self):
        if self.maxResponseNumber > self.currentResponseNumber:
            self.currentResponseNumber += 1
            return True
        else:
            return False

    def sleepWithTimeForNextResponse(self):
        logger.warning(f'Спим [{self.NEXT_RESPONSE_PAUSE_TIME}] секунд')
        sleep(self.NEXT_RESPONSE_PAUSE_TIME)


    # # return html page with selenium method
    # def getHtmlPageWithSelenium(self):
    #     response = self.webDriver.getHtmlPage(url)
    #
    #     return response


    # return html page with sessions method
    # def getHtmlPageWithSession(self):
    #     pass

    #
    # # return Products
    # def getProductsFromResponse(self, response: Response):
    #     products = Products()
    #
    #     soup = BeautifulSoup(response.html, 'lxml')
    #     all_products = soup.find_all(class_='shop2-product-item shop-product-item')
    #     for next in all_products:
    #         try:
    #             item_name = next.find(class_="product-name").text
    #         except Exception as Err:
    #             logger.error(f'Не удалось найти имя продукта [{Err}]')
    #             exit(1)
    #         try:
    #             item_price = ''.join(next.find(class_="price-current").text.split()[:-1]).replace(',', '.',
    #                                                                                              1)  # split()
    #         except Exception as Err:
    #             logger.error(f'Не удалось найти цену продукта [{item_name}] [{Err}]')
    #             exit(1)
    #         try:
    #             product_url = 'https://stok-centr.com' + next.find(class_="product-name").find('a').get('href')
    #         except Exception as Err:
    #             logger.error(f'Не удалось найти URL продукта [{item_name}] [{Err}]')
    #             exit(1)
    #
    #         logger.info(f"[добавление] {item_name=}:{item_price=}:{product_url=}")
    #         products.append(ProductsElement(item_name, float(item_price), product_url))
    #     return products


    def sleepWithTimeForNextResponse(self):
        sleep(self.NEXT_RESPONSE_PAUSE_TIME)


