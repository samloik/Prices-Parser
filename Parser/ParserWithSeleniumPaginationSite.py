from ParserSite import ParserSite
from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from ProductsElement import ProductsElement
from time import sleep
from Response import Response
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ParserWithSeleniumPaginationSite(ParserSite): # rename to SeleniumParser

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl)
        self.webDriver = SeleniumWebDriver()

        self.currentPage = 0
        self.NEXT_PAGE_PAUSE_TIME = 5
        # self.isFirstReadingPage = True
        # self.next_x_path_button = None
        # self.WAIT_PAUSE_TIME = 10

    # return ProductFromSite main method
    # def getProductsFromSite(self):


    def isNextPage(self, response: Response):
        webElements = self.webDriver.driver.find_elements(By.XPATH, self.next_x_path_button)

        # webElement = WebDriverWait(self.webDriver.driver, self.WAIT_PAUSE_TIM).until(
        #     EC.element_to_be_clickable((By.XPATH, self.next_x_path_button))
        # )

        if len(webElements) > 0:
            logger.info(f'существует следующая страница')
            return True

        logger.info(f'это была последняя страница')
        return False


    def setNextPage(self):
        self.currentPage += 1




    # return html page with main method
    def getResponseFromSite(self):

        logger.info('Пытаемся получить ответ от сайта')

        url = self.siteUrl + str(self.currentPage)
        # url = self.siteUrl
        response = self.webDriver.getHtmlPage(url)
        self.isFirstReadingPage = False

        # инфо блок
        if response.isResponseOK():
            logger.info(f'Страница получена без ошибок')
        else:
            logger.info(f'Страница получена c ошибкой')

        return response


    # # TODO: старый метод работает не всегда правильно - на удаление после тетстов нового метода
    # def getResponseFromSite2(self):
    #     logger.info('Пытаемся получить ответ от сайта')
    #
    #     url = self.siteUrl + str(self.currentPage)
    #     response = self.webDriver.getHtmlPage(url)
    #
    #     # инфо блок
    #     if response.isResponseOK():
    #         logger.info(f'Страница {self.currentPage} получена без ошибок')
    #     else:
    #         logger.info(f'Страница {self.currentPage} получена c ошибкой')
    #
    #     return response


    # # return html page with selenium method
    # def getHtmlPageWithSelenium(self):
    #     response = self.webDriver.getHtmlPage(url)
    #
    #     return response


    # return html page with sessions method
    # def getHtmlPageWithSession(self):
    #     pass


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
        logger.info(f"Спим [{self.NEXT_PAGE_PAUSE_TIME}] секунд")
        sleep(self.NEXT_PAGE_PAUSE_TIME)
