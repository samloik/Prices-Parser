
from Products import Products
from ParserAbstract.Response import Response

from ProductsElement import ProductsElement
# from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from bs4 import BeautifulSoup
from ParserAbstract.ParserWithSession import ParserWithSession



class ParserStockCentrWithSession(ParserWithSession):

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl)
        self.currentPage = 0
        self.setNextPagePauseTime(0)

        # self.session = requests.Session()


    # return isNextPage = self.checkForNextPage(html)
    def isNextPage(self, response: Response):

        soup = BeautifulSoup(response.html, 'lxml')

        pageNext = soup.find_all(class_='page-next')

        if len(pageNext) > 0:
            logger.info(f'[{self.currentPage}] вызываем следующую страницу')
            return True
        else:
            logger.info(f'[{self.currentPage}] это была последняя страница')
            return False


    # def getHtmlPage(self, url):
    #     html = ""
    #     try:
    #         res = self.session.get(url)
    #         html = res.content
    #         sleep(self.TIME_TO_READ_PAGE)   # TODO отрегулировать параметр времени
    #         # response = Response("200", html, None)
    #         response = Response( str(res.status_code), html, None)
    #     except Exception as Err:
    #         logger.error(Err)
    #         response = Response( str(res.status_code), None, str(Err))
    #
    #     return response

    # # return html page with main method
    # def getResponseFromSite(self):
    #     logger.info('Пытаемся получить ответ от сайта')
    #
    #     url = self.siteUrl + str(self.currentPage)
    #     response = self.getHtmlPage(url)
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


    # def sleepWithTimeForNextResponse(self):
    #     sleep()



def main():
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    parser = ParserStockCentrWithSession("https://stok-centr.com/magazin/folder/sukhiye-smesi/p/")
    products = parser.getProductsFromSite()

    render = DataRenderer()
    print('\n\nproducts')
    render.render(products, DataStrFormat.WIDE)

    # from DataRenderer import DataRenderer
    # from Products import Products
    # from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    products_utils = ProductsUtils()
    products_utils.saveProductsToFile(products, "stock_centr_with_session_save_file2.txt")


def main2():
    from DataRenderer import DataRenderer
    # from Products import Products
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils
    from UnitsTypes import UnitsTypes

    logger.remove()

    products_utils = ProductsUtils()
    products = products_utils.loadProductsFromFile("stock_centr_save_file.txt")

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)
    print(len(products))
    products_utils.saveProductsToFile(products, "cleaned_stock_centr_save_file.txt")

    stop_list = [
        "латекс", "гипс", "замазка", "шпакрил", "керамзит", "мастика", "мел", "добавка", "жаростой",
        "шпатлевка", "шпатлёвк", "декоратив", "огнеупор", "наливной", "глино"
        # "клей"
    ]

    cleaned_by_stop_list_products = products_utils.getCleanedProductsByStopList(products, stop_list)

    print('Очистка по стоп словам')

    render.render(cleaned_by_stop_list_products, DataStrFormat.WIDE)
    print(len(cleaned_by_stop_list_products))

    print('Очистка по отсутвию единицы измерения (кг!, литр):')

    cleaned_by_units_type = products_utils.getCleanedProductsByUnitsTypes(cleaned_by_stop_list_products,
                                                                          [UnitsTypes.KG, UnitsTypes.LITR])

    render.render(cleaned_by_units_type, DataStrFormat.WIDE)
    print(len(cleaned_by_units_type))

    print()

    el = products_utils.converPriceToPriceForUnit(cleaned_by_units_type, [UnitsTypes.KG, UnitsTypes.LITR])

    print('Цена за единицу:')

    render.render(el, DataStrFormat.WIDE)
    print(len(el))


def main3():
    from DataRenderer import DataRenderer
    # from Products import Products
    from ProductsUtils import ProductsUtils
    from ElementName import ElementName
    from UnitsTypes import UnitsTypes

    products_utils = ProductsUtils()
    products = products_utils.loadProductsFromFile("cleaned_stock_centr_save_file.txt")
    # products = products_utils.loadProductsFromFile("stock_centr_save_file.txt")

    logger.remove()

    render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)
    print(len(products))

    for name in products.products.keys():
        element_name = ElementName(name, [UnitsTypes.KG, UnitsTypes.LITR])

        values_from_name = element_name.getValueOfUnitsInName()
        if  values_from_name != "":
            # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
            print(f'[+] {name:>100} | {values_from_name} {element_name.units_types}')
        else:
            print(f'[-] {name:>100} | Null  {elementName.units_types}')



if __name__ == '__main__':
    main()

