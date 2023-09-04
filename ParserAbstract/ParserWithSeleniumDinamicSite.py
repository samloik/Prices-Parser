from ParserAbstract.ParserSite import ParserSite
from ParserAbstract.SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from time import sleep
from ParserAbstract.Response import Response
from selenium.webdriver.common.by import By

from ParserAbstract.SeleniumNextPageTypes import SeleniumNextPageTypes

class ParserWithSeleniumDinamicSite(ParserSite): # rename to SeleniumParser

    def __init__(self, site_url:str, time_to_read_first_page=10, time_to_read_next_page=0):
        super().__init__(site_url)
        # self.currentPage = 0
        self.webDriver = SeleniumWebDriver(time_to_read_first_page, time_to_read_next_page)
        self.set_next_page_pause_time(5)

        self.isFirstReadingPage = True
        self.next_x_path_button = None
        self.next_x_path_stop_content = None
        # self.WAIT_PAUSE_TIME = 10
        self.selenium_next_page_types = SeleniumNextPageTypes.NEXT_BUTTON_ABSENT



    def is_next_page(self, response: Response):
        webElements = self.webDriver.driver.find_elements(By.XPATH, self.next_x_path_button)


        # webElement = WebDriverWait(self.webDriver.driver, self.WAIT_PAUSE_TIME).until(
        #     EC.element_to_be_clickable((By.XPATH, self.next_x_path_button))
        # )

        if len(webElements) > 0:
            if self.selenium_next_page_types == SeleniumNextPageTypes.NEXT_BUTTON_TO_STOP_ELEMENT:
                stopElements = self.webDriver.driver.find_elements(By.XPATH, self.next_x_path_stop_content)

                if len(stopElements) == 0:
                    logger.info(f'существует следующая страница')
                    return True
                else:
                    logger.info(f'Кнопка далее заблокирована {stopElements[0]=}')
            elif self.selenium_next_page_types == SeleniumNextPageTypes.NEXT_BUTTON_ABSENT:
                return True

        logger.info(f'это была последняя страница')
        return False



    def set_next_page(self):

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
                # webElements[0].click()

                # реализация нажатия кнопки с помощью JavaScript
                # logger.error(f"{self.next_x_path_button=}")
                script = (
                    """
                    function getElementByXpath(path) {
                      return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    }
                    getElementByXpath(`%s`).click();
                    """
                    % self.next_x_path_button
                )
                # logger.error(f"{script=}")
                self.webDriver.driver.execute_script(script)
            except Exception as Err:
                logger.error(Err)
                logger.info(f'{len(webElements)=} {webElements[0].get_property("disabled")=}')
                logger.info(f'{webElements[0].is_enabled()=}')
                exit(1)
            logger.info(f'нажимаем кнопку далее и спим [{self.get_next_page_pause_time()}] секунд')
            sleep(self.get_next_page_pause_time())
        else:
            logger.error(f'нет кнопки далее на странице')
        # # # # TODO и тут полазил
        # sleep(15)
        # exit(0)

    # def set_next_page_pause_time(self, time):
    #     self.NEXT_PAGE_PAUSE_TIME_TO_CLICK = time


    # return html page with main method
    def get_response_from_site(self):

        if self.isFirstReadingPage:
            logger.info('Пытаемся получить ответ от сайта')

            # url = self.siteUrl + str(self.currentPage)
            url = self.get_site_url()
            response = self.webDriver.get_html_page(url)
            self.isFirstReadingPage = False

            # инфо блок
            if response.is_response_ok():
                logger.info(f'Страница получена без ошибок')
            else:
                logger.info(f'Страница получена c ошибкой')

        else:
            # TODO залип тут пока
            # self.clickNextPageButton()
            html = self.webDriver.driver.page_source
            response = Response("200", html, None)

        return response


    # def sleep_with_time_for_next_response(self):
    #     sec = 10
    #     logger.info(f"[sleepWithTimeForNextResponse] Спим [{sec}] секунд")
    #     sleep(sec)
