
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

    _current_response_number: int
    _max_response_number: int
    _next_response_pause_time: int
    _current_page:int

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl)
        self.session = requests.Session()
        self.set_current_page(0)                # установка номера начальной страницы
        self.set_next_page_pause_time(0)        # время паузы перед переходом на след. страницу
        self.set_curent_response_number(0)      # установка начального номера повторного запроса
        self.set_next_response_pause_time(2)    # время пайзы перед повторным запросом
        self.set_max_response_number(5)         # максимальное количество повторных запросов

        # self.NEXT_PAGE_PAUSE_TIME = 0
        # self._max_response_number = 5
        # self._current_response_number = 0
        # self.NEXT_RESPONSE_PAUSE_TIME = 1

    def set_current_page(self, current_page):
        self._current_page = current_page

    def get_current_page(self):
        return self._current_page

    def set_max_response_number(self, max_response_number):
        # установить максимальное количетсво повторныйх запросов
        self._max_response_number = max_response_number

    def get_max_response_number(self):
        return self._max_response_number

    def set_curent_response_number(self, number):
        self._current_response_number = number

    def get_current_response_number(self):
        return self._current_response_number

    def set_next_response_pause_time(self, pause_time):
        self._next_response_pause_time = pause_time
        # self.NEXT_RESPONSE_PAUSE_TIME = pause_time

    def get_next_pesponse_pause_time(self):
        return self._next_response_pause_time

    def set_next_page_pause_time(self, time):
        # устанавливаем время паузы перед переключением страницы
        self.NEXT_PAGE_PAUSE_TIME = time

    def get_next_page_pause_time(self):
        return self.NEXT_PAGE_PAUSE_TIME


    def set_next_page(self):
        self.set_current_page(self.get_current_page() + 1)


    def get_html_page(self, url):
        html = ""
        try:
            res = self.session.get(url)
            html = res.content
            sleep(self.get_next_page_pause_time())   # TODO отрегулировать параметр времени
            # response = Response("200", html, None)
            response = Response( str(res.status_code), html, None)
        except Exception as Err:
            logger.error(Err)
            response = Response( str(res.status_code), None, str(Err))

        return response


    # return html page with main method
    def get_response_from_site(self):
        self.drop_response_number()
        while True:
            response = self.get_response_from_site_with_session()
            if response.is_response_ok():
                break
            self.sleep_with_time_for_next_response()
            if self.is_max_response_number():
                # TODO: продумать дальнейшую логику
                # записать html
                logger.error(
                    f'[Error:] Максимальное количество попыток [{self.get_max_response_number()}] получить ответ от сайта достигнуто')
                logger.info(f'[Error:] [{response=}]')
                exit(1)
            else:
                logger.warning(f'[!] Неверный ответ от сервера: попытка номер [{self.get_current_response_number()}]')
                logger.info(f'[!] [{response=}]')
        return response



    # return html page with main method
    def get_response_from_site_with_session(self):

        url = self.get_site_url() + str(self.get_current_page())

        logger.info(f'Пытаемся получить ответ от сайта [{url}]')

        response = self.get_html_page(url)

        # инфо блок
        if response.is_response_ok():
            logger.info(f'Страница [{self.get_current_page()}] получена без ошибок')
        else:
            logger.warning(f'Страница [{self.get_current_page()}] получена c ошибкой [{srt(response)=}]')

        return response

    def drop_response_number(self):
        self.set_curent_response_number(0)


    def is_max_response_number(self):
        current_response_number = self.get_current_response_number()
        if self.get_max_response_number() > current_response_number:
            self.set_curent_response_number(  current_response_number + 1)
            return True
        else:
            return False


    def sleep_with_time_for_next_response(self):
        logger.warning(f'Спим [{self.get_next_pesponse_pause_time()}] секунд перед следующим запросом')
        sleep(self.get_next_pesponse_pause_time())


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

