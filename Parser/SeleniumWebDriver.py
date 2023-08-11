from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import platform
from loguru import logger
from Response import Response


from time import sleep

class SeleniumWebDriver:

    def __init__(self, time_to_read=5):
        self.driver, self.options = self.anonymizeWebDriver()
        self.TIME_TO_READ_PAGE = time_to_read      # задержка (секунд) после запроса страницы


    def anonymizeWebDriver(self):

        DRIVER_LOCATION, BINARY_LOCATION = self.getDriverLocation()

        service = Service(DRIVER_LOCATION)
        # service = Service(Service(ChromeDriverManager().install())) - не работает

        options = webdriver.ChromeOptions()

        if BINARY_LOCATION:
            options.binary_location = BINARY_LOCATION

            # options.add_argument('--disable-gpu')  # Only included in Linux version
            # options.add_argument('--no-sandbox')  # Only included in Linux version

        # options.add_argument('--headless')    # - C headless не работает
        options.add_argument('--disable-blink-features=AutomationControlled')  # первое !!!

        #
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])   # дополнительно
        # options.add_experimental_option('useAutomationExtension', False)            # дополнительно
        #

        driver = webdriver.Chrome(service=service, options=options)
        # driver = webdriver.Chrome(options=options)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {  # второе !!!
            'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            '''
        })

        driver.maximize_window()

        return driver, options


    def getDriverLocation(self):
        current_os = platform.system()
        if current_os == "Windows":
            DRIVER_LOCATION = 'C:\PycharmProjects\Price-monitoring-project\chromedriver.exe'
            BINARY_LOCATION = None
        else: # Linux
            DRIVER_LOCATION = '/usr/bin/chromedriver'
            BINARY_LOCATION = '/usr/bin/google-chrome-stable'
        return DRIVER_LOCATION, BINARY_LOCATION


    def getHtmlPage(self, url):
        html = ""
        try:
            self.driver.get(url)
            sleep(self.TIME_TO_READ_PAGE)   # TODO отрегулировать параметр времени
            html = self.driver.page_source
            response = Response("200", html, None)
        except Exception as Err:
            logger.error(Err)
            response = Response("BAD", None, str(Err))

        return response


def main():
    logger.add("loger.log", backtrace=True, diagnose=True, level='INFO')

    web = SeleniumWebDriver()

    res = web.getHtmlPage('https://google.com')
    print(res.html)

    sleep(5)

if __name__ == '__main__':
    main()
