from ParserAbstract.ParserSite import ParserSite
from ParserAbstract.SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from time import sleep
from ParserAbstract.Response import Response
from selenium.webdriver.common.by import By


class ParserWithSeleniumPaginationSite(ParserSite): # rename to SeleniumParser

    def __init__(self, siteUrl:str, time_to_read_first_page=10, time_to_read_next_page=5):
        super().__init__(siteUrl)
        self.webDriver = SeleniumWebDriver(time_to_read_first_page, time_to_read_next_page)

        self.set_current_page(0)
        self.set_next_page_pause_time(0)


    def set_current_page(self, page):
        self._current_page = page

    def get_current_page(self):
        return self._current_page


    def is_next_page(self, response: Response):
        webElements = self.webDriver.driver.find_elements(By.XPATH, self.next_x_path_button)

        # webElement = WebDriverWait(self.webDriver.driver, self.WAIT_PAUSE_TIM).until(
        #     EC.element_to_be_clickable((By.XPATH, self.next_x_path_button))
        # )

        if len(webElements) > 0:
            logger.info(f'существует следующая страница')
            return True

        logger.info(f'это была последняя страница')
        return False


    def set_next_page(self):
        self.set_current_page( self.get_current_page() + 1)
        logger.info(f"Спим [{self.get_next_page_pause_time()}] секунд")
        sleep(self.get_next_page_pause_time())



    # return html page with main method
    def get_response_from_site(self):
        logger.info('Пытаемся получить ответ от сайта')

        url = self.get_site_url() + str(self.get_current_page())
        response = self.webDriver.get_html_page(url)
        # инфо блок
        if response.is_response_ok():
            logger.info(f'Страница получена без ошибок')
        else:
            logger.info(f'Страница получена c ошибкой')

        return response


