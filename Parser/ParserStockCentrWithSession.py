
from Products import Products
from ParserAbstract.Response import Response

from ProductsElements.ProductsElement import ProductsElement
# from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from bs4 import BeautifulSoup
from ParserAbstract.ParserWithSession import ParserWithSession



class ParserStockCentrWithSession(ParserWithSession):

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl)
        # self.set_current_page(0)
        # self.set_next_page_pause_time(0)



    # return isNextPage = self.checkForNextPage(html)
    def is_next_page(self, response: Response):

        soup = BeautifulSoup(response.html, 'lxml')

        page_next = soup.find_all(class_='page-next')

        if len(page_next) > 0:
            logger.info(f'[{self.get_current_page()}] вызываем следующую страницу')
            return True
        else:
            logger.info(f'[{self.get_current_page()}] это была последняя страница')
            return False


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


    # def sleepWithTimeForNextResponse(self):
    #     sleep()



def test():
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    parser = ParserStockCentrWithSession("https://stok-centr.com/magazin/folder/sukhiye-smesi/p/")
    products = parser.get_products_from_site()

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
    products_utils.save_products_to_file(products, "stock_centr_with_session_save_file2.txt")


def test2():
    from DataRenderer import DataRenderer
    # from Products import Products
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils
    from UnitsTypes import UnitsTypes

    # logger.remove()

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

    print('перерасчет цены в цену за кг')

    render.render(el, DataStrFormat.WIDE)
    print(len(el))

    products = products_utils.save_products_to_file(el, "cleaned_stock_centr_save_file.txt")


def test3():
    from DataRenderer import DataRenderer
    # from Products import Products
    from ProductsUtils import ProductsUtils
    from ProductsElements.ElementName import ElementName
    from UnitsTypes import UnitsTypes

    products_utils = ProductsUtils()
    products = products_utils.load_products_from_file("cleaned_stock_centr_save_file.txt")
    # products = products_utils.loadProductsFromFile("stock_centr_save_file.txt")

    # logger.remove()

    render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)
    print(len(products))

    for name in products.keys():
        element_name = ElementName(name, [UnitsTypes.KG, UnitsTypes.LITR])

        values_from_name = element_name.get_value_of_units_in_name()
        if  values_from_name != "":
            # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
            print(f'[+] {name:>100} | {values_from_name} {element_name.units_types}')
        else:
            print(f'[-] {name:>100} | Null  {element_name.units_types}')


def test4():
    from DataRenderer import DataRenderer
    # from Products import Products
    from ProductsUtils import ProductsUtils
    from ProductsElements.ElementName import ElementName

    products_utils = ProductsUtils()
    products = products_utils.load_products_from_file("cleaned_stock_centr_save_file.txt")
    # products = products_utils.loadProductsFromFile("stock_centr_save_file.txt")

    # logger.remove()

    render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)
    print(len(products))

    for name in products.keys():
        element_name = ElementName(name, [])

        values_from_name = element_name.get_value_of_units_in_name()
        if  values_from_name != "":
            # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
            print(f'[+] {name:>100} | {values_from_name} {element_name.units_types}')
        else:
            print(f'[-] {name:>100} | Null  {element_name.units_types}')


if __name__ == '__main__':
    test()
    test2()
    test3()
    test4()


