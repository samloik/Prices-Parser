
from Products import Products
# from ParserSite import ParserSite
from ParserAbstract.Response import Response
from ProductsElement import ProductsElement
# from time import sleep
# from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from bs4 import BeautifulSoup
from ParserAbstract.ParserWithSeleniumDinamicSite import ParserWithSeleniumDinamicSite
# from ParserWithSession import ParserWithSession


from ParserAbstract.SeleniumNextPageTypes import SeleniumNextPageTypes

class ParserMirInstrumentaSeleniumDinamic(ParserWithSeleniumDinamicSite): # rename to SeleniumParser

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl)

        # self.next_x_path_button = '/html/body/div[1]/div/div/div[2]/main/article/section/div[2]/div/[last()]'
        self.next_x_path_button = "//div[contains(@class, 'arrow next')]"
        self.next_x_path_stop_content = "//div[contains(@class, 'arrow next disabled')]"
        self.selenium_next_page_types = SeleniumNextPageTypes.NEXT_BUTTON_TO_STOP_ELEMENT
        self.setNextPagePauseTime(5)


    # return Products
    def getProductsFromResponse(self, response: Response):
        products = Products()

        soup = BeautifulSoup(response.html, 'lxml')
        all_products = soup.find_all(class_='horizontal-item noauth catalog__list-item horizontal')
        logger.info(f'Получили от html страницы [{len(all_products)}] элементов')
        for next in all_products:
            try:
                # item_name = next.find(class_="product-name").text
                item_name = next.find('a', {'itemprop' : 'name'}).text
                # logger.error(f'{len(item_name)=} {item_name}=')
                # sleep(10)
                # exit(0)
            except Exception as Err:
                logger.error(f'Не удалось найти имя продукта [{Err}]')
                exit(1)
            try:
                item_price = 0
            except Exception as Err:
                logger.error(f'Не удалось найти цену продукта [{item_name}] [{Err}]')
                exit(1)
            try:
                product_url = 'https://instrument.ru' + next.find('div', {'class' : 'name'}).find('a').get('href')
            except Exception as Err:
                logger.error(f'Не удалось найти URL продукта [{item_name}] [{Err}]')
                exit(1)

            logger.info(f"[добавление] {item_name=}:{item_price=}:{product_url=}")
            products.append(ProductsElement(item_name, float(item_price), product_url))
        return products


    # def sleepWithTimeForNextResponse(self):
    #     sleep(10)



def main():
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    # parser = ParserStockCentrWithSelenium("https://stok-centr.com/magazin/folder/sukhiye-smesi/p/")
    # parser = ParserMirInstrumentaSelenium("https://instrument.ru/web/catalog/filter/clear/apply/?sort=&page_size=%7B%7D&page=1&action=0&section_id=935&token=")
    # parser = ParserMirInstrumentaSelenium("https://instrument.ru/web/catalog/filter/clear/apply/?sort=&page_size=%7B%7D&action=0&section_id=935&token=&page=")
    parser = ParserMirInstrumentaSeleniumDinamic("https://instrument.ru/catalog/slesarnyy-instrument/nabory-instrumenta/")
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
    products_utils.saveProductsToFile(products, "ParserMirInstrumentaSelenium_save_file.txt")


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


