# Этот файл сущетвует как начальные для разработки ParserWithSession
# после удачных тестов - его можно удалить



from ProductsElements.Products import Products
from ParserAbstract.ParserSite import ParserSite
from ParserAbstract.Response import Response

from ProductsElements.ProductsElement import ProductsElement
from time import sleep
from ParserAbstract.SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from bs4 import BeautifulSoup


class ParserStockCentrWithSelenium3(ParserSite): # rename to SeleniumParser

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl)
        self.currentPage = 0
        self.webDriver = SeleniumWebDriver()

    # return ProductFromSite main method
    # def getProductsFromSite(self):


    # return isNextPage = self.checkForNextPage(html)
    def is_next_page(self, response: Response):

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
    def get_response_from_site(self):
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
    def get_products_from_response(self, response: Response):
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


    def sleep_with_time_for_next_response(self):
        sleep(10)



def main():
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    parser = ParserStockCentrWithSelenium3("https://stok-centr.com/magazin/folder/sukhiye-smesi/p/")
    products = parser.get_products_from_site()

    render = DataRenderer()
    print('\n\nproducts')
    render.render(products, DataStrFormat.WIDE)

    # from DataRenderer import DataRenderer
    # from Products import Products
    # from DataStrFormat import DataStrFormat
    from Utils.ProductsUtils import ProductsUtils

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    products_utils = ProductsUtils()
    products_utils.save_products_to_file(products, "stock_centr_save_file.txt")


def main2():
    from DataRenderer import DataRenderer
    # from Products import Products
    from DataStrFormat import DataStrFormat
    from Utils.ProductsUtils import ProductsUtils
    from UnitsTypes import UnitsTypes

    logger.remove()

    products_utils = ProductsUtils()
    products = products_utils.load_products_from_file("stock_centr_save_file.txt")

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)
    print(len(products))
    products_utils.save_products_to_file(products, "cleaned_stock_centr_save_file.txt")

    stop_list = [
        "латекс", "гипс", "замазка", "шпакрил", "керамзит", "мастика", "мел", "добавка", "жаростой",
        "шпатлевка", "шпатлёвк", "декоратив", "огнеупор", "наливной", "глино"
        # "клей"
    ]

    cleaned_by_stop_list_products = products_utils.get_cleaned_products_by_stop_list(products, stop_list)

    print('Очистка по стоп словам')

    render.render(cleaned_by_stop_list_products, DataStrFormat.WIDE)
    print(len(cleaned_by_stop_list_products))

    print('Очистка по отсутвию единицы измерения (кг!, литр):')

    cleaned_by_units_type = products_utils.get_cleaned_products_by_units_types(cleaned_by_stop_list_products,
                                                                          [UnitsTypes.KG, UnitsTypes.LITR])

    render.render(cleaned_by_units_type, DataStrFormat.WIDE)
    print(len(cleaned_by_units_type))

    print()

    el = products_utils.convert_price_to_price_for_unit(cleaned_by_units_type, [UnitsTypes.KG, UnitsTypes.LITR])

    print('Цена за единицу:')

    render.render(el, DataStrFormat.WIDE)
    print(len(el))


def main3():
    from DataRenderer import DataRenderer
    # from Products import Products
    from Utils.ProductsUtils import ProductsUtils
    from ProductsElements.ElementName import ElementName
    from UnitsTypes import UnitsTypes

    products_utils = ProductsUtils()
    products = products_utils.load_products_from_file("cleaned_stock_centr_save_file.txt")
    # products = products_utils.loadProductsFromFile("stock_centr_save_file.txt")

    logger.remove()

    render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)
    print(len(products))

    for name in products.products.keys():
        element_name = ElementName(name, [UnitsTypes.KG, UnitsTypes.LITR])

        values_from_name = element_name.get_value_of_units_in_name()
        if  values_from_name != "":
            # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
            print(f'[+] {name:>100} | {values_from_name} {element_name.units_types}')
        else:
            print(f'[-] {name:>100} | Null  {elementName.units_types}')



if __name__ == '__main__':
    main2()


