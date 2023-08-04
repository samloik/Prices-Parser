
from Products import Products
from SiteParser import SiteParser
from Response import Response

from ProductsElement import ProductsElement
from time import sleep
from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from bs4 import BeautifulSoup


class StockCentrParser(SiteParser): # rename in SeleniumParser

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl)
        self.currentPage = 0
        self.webDriver = SeleniumWebDriver()



    # return ProductFromSite main method
    # def getProductsFromSite(self):


    # return isNextPage = self.checkForNextPage(html)
    def isNextPage(self, response: Response):

        soup = BeautifulSoup(response.html, 'lxml')

        pageNext = soup.find_all(class_='page-next')

        if len(pageNext) > 0:
            logger.info(f'[{self.currentPage}] вызываем следующую страницу')
            self.currentPage += 1
            return True
        else:
            logger.info(f'[{self.currentPage}] это была последняя страница')
            return False


    # return html page with main method
    def getResponseFromSite(self):
        logger.info('Пытаемся получить ответ от сайта')

        url = self.siteUrl + str(self.currentPage)
        response = self.webDriver.getHtmlPage(url)

        # инфо блок
        if response.isResponseOK():
            logger.info(f'Страница {self.currentPage} получена без ошибок')
        else:
            logger.info(f'Страница {self.currentPage} получена c ошибкой')

        return response


    # # return html page with selenium method
    # def getHtmlPageWithSelenium(self):
    #     response = self.webDriver.getHtmlPage(url)
    #
    #     return response


    # return html page with sessions method
    # def getHtmlPageWithSession(self):
    #     pass


    # return Products
    def getProductsFromResponse(self, response: Response):
        products = Products()

        soup = BeautifulSoup(response.html, 'lxml')
        all_products = soup.find_all(class_='shop2-product-item shop-product-item')
        for next in all_products:
            try:
                item_name = next.find(class_="product-name").text
            except Exception as Err:
                logger.error(f'Не удалось найти имя продукта [{Err}]')
                exit(1)
            try:
                item_price = ''.join(next.find(class_="price-current").text.split()[:-1]).replace(',', '.',
                                                                                                 1)  # split()
            except Exception as Err:
                logger.error(f'Не удалось найти цену продукта [{item_name}] [{Err}]')
                exit(1)
            try:
                product_url = 'https://stok-centr.com' + next.find(class_="product-name").find('a').get('href')
            except Exception as Err:
                logger.error(f'Не удалось найти URL продукта [{item_name}] [{Err}]')
                exit(1)

            logger.info(f"[добавление] {item_name=}:{item_price=}:{product_url=}")
            products.append(ProductsElement(item_name, float(item_price), product_url))
        return products


    def sleepWithTimeForNextResponse(self):
        sleep(10)



def main():
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    parser = StockCentrParser("https://stok-centr.com/magazin/folder/sukhiye-smesi/p/")
    products = parser.getProductsFromSite()

    render = DataRenderer()
    print('\n\nproducts')
    render.render(products, DataStrFormat.WIDE)


if __name__ == '__main__':
    main()