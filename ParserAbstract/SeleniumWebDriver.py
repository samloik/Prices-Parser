# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
import platform
from loguru import logger
from ParserAbstract.Response import Response

import undetected_chromedriver as uc  # pip install undetected-chromedriver

from time import sleep

class SeleniumWebDriver:

    def __init__(self, time_to_read_first_page=10, time_to_read_next_page=5):
        self.driver, self.options = self.anonymize_web_driver()
        self.TIME_TO_READ_FIRST_PAGE = time_to_read_first_page    # задержка (секунд) для прогрузки первой стариницы
        self.TIME_TO_READ_NEXT_PAGE = time_to_read_next_page      # задержка (секунд) после запроса страницы
        self.is_first_page_to_load = True


    @staticmethod
    def anonymize_web_driver():

        # driver = uc.Chrome()
        #
        # from session not created: This version of ChromeDriver only supports Chrome version 117
        # Current browser version is 116.0.5845.188
        #
        driver = uc.Chrome(version_main=121)

        # driver.get("https://proxy6.net/privacy")
        # driver.get("https://habarovsk.leroymerlin.ru/catalogue/suhie-smesi-i-gruntovki/?page=2")
        # sleep(100)
        # exit(0)
        driver.maximize_window()

        # https://piprogramming.org/articles/How-to-make-Selenium-undetectable-and-stealth--7-Ways-to-hide-your-Bot-Automation-from-Detection-0000000017.html

        return driver, None

    #
    # def anonymizeWebDriver2(self):
    #
    # https://piprogramming.org/articles/How-to-make-Selenium-undetectable-and-stealth--7-Ways-to-hide-your-Bot-Automation-from-Detection-0000000017.html
    #
    #     DRIVER_LOCATION, BINARY_LOCATION = self.getDriverLocation()
    #
    #     service = Service(DRIVER_LOCATION)
    #     # service = Service(Service(ChromeDriverManager().install())) - не работает
    #
    #     options = webdriver.ChromeOptions()
    #
    #     if BINARY_LOCATION:
    #         options.binary_location = BINARY_LOCATION
    #
    #         # options.add_argument('--disable-gpu')  # Only included in Linux version
    #         # options.add_argument('--no-sandbox')  # Only included in Linux version
    #
    #     # options.add_argument('--headless')    # - C headless не работает
    #     options.add_argument('--disable-blink-features=AutomationControlled')  # первое !!!
    #
    #     #
    #     # options.add_experimental_option('excludeSwitches', ['enable-automation'])   # дополнительно
    #     # options.add_experimental_option('useAutomationExtension', False)            # дополнительно
    #     #
    #
    #     driver = webdriver.Chrome(service=service, options=options)
    #     # driver = webdriver.Chrome(options=options)
    #
    #     driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {  # второе !!!
    #         'source': '''
    #             delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
    #             delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
    #             delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    #         '''
    #     })
    #
    #     driver.maximize_window()
    #
    #     return driver, options


    # def get_driver_location(self):
    #     current_os = platform.system()
    #     if current_os == "Windows":
    #         DRIVER_LOCATION = 'C:\PycharmProjects\Price-monitoring-project\chromedriver.exe'
    #         BINARY_LOCATION = None
    #     else: # Linux
    #         DRIVER_LOCATION = '/usr/bin/chromedriver'
    #         BINARY_LOCATION = '/usr/bin/google-chrome-stable'
    #     return DRIVER_LOCATION, BINARY_LOCATION


    def get_html_page(self, url):
        html = ""
        try:
            self.driver.get(url)
            if self.is_first_page_to_load:
                self.is_first_page_to_load = False
                logger.info(f'Ждем загрузки первой страницы [{self.TIME_TO_READ_FIRST_PAGE}] секунд')
                sleep(self.TIME_TO_READ_FIRST_PAGE)
            else:
                logger.info(f'Ждем загрузки следующей страницы [{self.TIME_TO_READ_NEXT_PAGE}] секунд')
                sleep(self.TIME_TO_READ_NEXT_PAGE)   # TODO отрегулировать параметр времени
            html = self.driver.page_source
            response = Response("200", html, None)
        except Exception as Err:
            logger.error(Err)
            response = Response("BAD", None, str(Err))

        return response

    def __del__(self):
        # убираем сообщение об ошибке так:
        #     time.sleep(0.1)
        # OSError: [WinError 6] Неверный дескриптор
        # https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/955
        try:
            self.driver.close()
            sleep(0.1)
            # self.driver.quit()
            # sleep(1)
        except Exception as Err:
            pass



def test():
    # logger.add("loger.log", backtrace=True, diagnose=True, level='INFO', rotation="2 day" )

    web = SeleniumWebDriver(0,0)

    res = web.get_html_page('https://google.com')
    print(res.html[:1000])

    sleep(5)

if __name__ == '__main__':
    test()
