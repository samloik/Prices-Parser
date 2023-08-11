from ParserSite import ParserSite
from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from ProductsElement import ProductsElement
from time import sleep
from Response import Response
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ParserWithSeleniumDinamicSite(ParserSite): # rename to SeleniumParser

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl)
        # self.currentPage = 0
        self.webDriver = SeleniumWebDriver()

        self.isFirstReadingPage = True
        self.next_x_path_button = None
        self.NEXT_PAGE_PAUSE_TIME = 5
        self.WAIT_PAUSE_TIME = 10

    # return ProductFromSite main method
    # def getProductsFromSite(self):



    def isNextPage(self, response: Response):
        webElements = self.webDriver.driver.find_elements(By.XPATH, self.next_x_path_button)


        # webElement = WebDriverWait(self.webDriver.driver, self.WAIT_PAUSE_TIM).until(
        #     EC.element_to_be_clickable((By.XPATH, self.next_x_path_button))
        # )

        if len(webElements) > 0:
            # wt = WebDriverWait(self.webDriver.driver, 6)
            isEnabled = webElements[0].is_enabled()

            if isEnabled:
                logger.info(f'существует следующая страница')
                return True
            else:
                logger.error(f'Кнопка далее заблокирована {isEnabled=}')

        logger.info(f'это была последняя страница')
        return False



    def isNextPage2(self, response: Response):
        webElements = self.webDriver.driver.find_elements(By.XPATH, self.next_x_path_button)

        # webElement = WebDriverWait(self.webDriver.driver, self.WAIT_PAUSE_TIM).until(
        #     EC.element_to_be_clickable((By.XPATH, self.next_x_path_button))
        # )

        if len(webElements) > 0:
            isEnabled = webElements[0].is_enabled()

            if isEnabled:
                logger.info(f'существует следующая страница')
                return True
            else:
                logger.error(f'Кнопка далее заблокирована {isEnabled=}')

        logger.info(f'это была последняя страница')
        return False


    def setNextPage(self):

        #  SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        # last_height = self.webDriver.driver.execute_script("return document.body.scrollHeight") #- 1080

        # print(f'{last_height=}')
        # Scroll down to bottom
        # self.webDriver.driver.execute_script(f"window.scrollTo(0, {last_height-1620});")
        # Wait to load page
        # sleep(SCROLL_PAUSE_TIME)
        webElements = self.webDriver.driver.find_elements(By.XPATH, self.next_x_path_button)
        if len(webElements) > 0:
            # logger.error(f'{len(webElement)=}')
            try:
                webElements[0].click()
            except Exception as Err:
                logger.error(Err)
                logger.info(f'{len(webElements)=} {webElements[0].get_property("disabled")=}')
                logger.info(f'{webElements[0].is_enabled()=}')
                exit(0)
            logger.info(f'нажимаем кнопку далее и спим [{self.NEXT_PAGE_PAUSE_TIME}] секунд')
            sleep(self.NEXT_PAGE_PAUSE_TIME)
        else:
            logger.error(f'нет кнопки далее на странице')
        # # # # TODO и тут полазил
        # sleep(15)
        # exit(0)




    # return html page with main method
    def getResponseFromSite(self):

        if self.isFirstReadingPage:
            logger.info('Пытаемся получить ответ от сайта')

            # url = self.siteUrl + str(self.currentPage)
            url = self.siteUrl
            response = self.webDriver.getHtmlPage(url)
            self.isFirstReadingPage = False

            # инфо блок
            if response.isResponseOK():
                logger.info(f'Страница получена без ошибок')
            else:
                logger.info(f'Страница получена c ошибкой')

        else:
            # TODO залип тут пока
            # self.clickNextPageButton()
            html = self.webDriver.driver.page_source
            response = Response("200", html, None)

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
        sec = 10
        logger.info(f"Спим [{sec}] секунд")
        sleep(sec)
