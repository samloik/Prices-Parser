
from Products import Products
# from ParserSite import ParserSite
from ParserAbstract.Response import Response
from ProductsElements.ProductsElement import ProductsElement
# from time import sleep
# from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from bs4 import BeautifulSoup
from ParserAbstract.ParserWithSeleniumDinamicSite import ParserWithSeleniumDinamicSite
# from ParserWithSession import ParserWithSession


from ParserAbstract.SeleniumNextPageTypes import SeleniumNextPageTypes

class ParserMirUpakovkiWithSeleniumDinamic(ParserWithSeleniumDinamicSite): # rename to SeleniumParser

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl)

        # self.next_x_path_button = '/html/body/div[1]/div/div/div[2]/main/article/section/div[2]/div/[last()]'
        # self.next_x_path_button = "/html/body/div[3]/div[1]/div[1]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[3]/div[5]/div[2]"
        # self.next_x_path_button = "/html/body/div[3]/div/div[1]/div/div/div[2]/div/div/div[2]/div/div[3]/div[2]/div[2]"
        self.next_x_path_button = "//*[@id='show-more-catalog-items']/div[2]"
        self.next_x_path_stop_content = None
        self.selenium_next_page_types = SeleniumNextPageTypes.NEXT_BUTTON_ABSENT
        self.set_next_page_pause_time(3)


    # return Products
    def get_products_from_response(self, response: Response):
        products = Products()

        soup = BeautifulSoup(response.html, 'lxml')
        all_products = soup.find_all('div', {'class': "product-item-container"})
        logger.info(f'Получили от html страницы [{len(all_products)}] элементов')
        for next in all_products:
            try:
                # item_name = next.find(class_="product-name").text
                item_name = next.find('div', {'class': "product-item-title"}).find('a').get('title')
                # logger.error(f'{len(item_name)=} {item_name}=')
                # sleep(10)
                # exit(0)
            except Exception as Err:
                logger.error(f'Не удалось найти имя продукта [{Err}]')
                exit(1)
            try:
                # pr = next.find('span', {'class': "product-item-price-current"})
                item_price = next.find('span', {'class': "product-item-price-current"}).text
                item_price = item_price.replace('р.', '').replace('\n', '').replace('\t', '').replace(' ', '')
                # logger.error(f'{len(item_price)=} {item_price=} ')
                # sleep(10)
                # exit(0)
            except Exception as Err:
                # TODO
                #  Продумать нужны ли элементы без цены в списке?
                logger.info(f'Не удалось найти цену продукта [{item_name}] [{Err}]')
                logger.error(f'Элемент [{item_name}] не попадает в список')
                continue
            try:
                product_url = 'https://khv.mirupak.ru' + next.find('div', {'class': "product-item-title"}).find('a').get('href')
            except Exception as Err:
                logger.error(f'Не удалось найти URL продукта [{item_name}] [{Err}]')
                exit(1)

            logger.info(f"[добавление] {item_name=}:{item_price=}:{product_url=}")
            products.append(ProductsElement(item_name, float(item_price), product_url))
        # sleep(10)
        # exit(0)
        return products


    # def sleepWithTimeForNextResponse(self):
    #     sleep(10)



def test():
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    # parser = ParserMirUpakovkiWithSeleniumDinamic("https://khv.mirupak.ru/catalog/khv/posuda_odnorazovaya_2/")
    parser = ParserMirUpakovkiWithSeleniumDinamic(
        "https://khv.mirupak.ru/catalog/khv/pakety_bez_risunka_i_meshki/pakety_fasovochnye/pakety_fasovochnye_pvd_1/"
    )
    products = parser.get_products_from_site()

    render = DataRenderer()
    print('\n\nproducts')
    render.render(products, DataStrFormat.WIDE)

    # from DataRenderer import DataRenderer
    # from Products import Products
    # from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils

    # render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)

    products_utils = ProductsUtils()
    products_utils.save_products_to_file(products, "ParserMirUpakovkiWithSeleniumDinamic_save_file.txt")


def test_1_5():
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    # parser = ParserMirUpakovkiWithSeleniumDinamic("https://khv.mirupak.ru/catalog/khv/posuda_odnorazovaya_2/")
    parser = ParserMirUpakovkiWithSeleniumDinamic(
        "https://khv.mirupak.ru/catalog/khv/pakety_bez_risunka_i_meshki/meshki_/"
    )
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
    products_utils.save_products_to_file(products, "ParserMirUpakovkiWithSeleniumDinamic_save_file.txt")



def test2():
    from DataRenderer import DataRenderer
    # from Products import Products
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils
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


def test3():
    from DataRenderer import DataRenderer
    # from Products import Products
    from ProductsUtils import ProductsUtils
    from ProductsElements.ElementName import ElementName
    from UnitsTypes import UnitsTypes

    products_utils = ProductsUtils()
    products = products_utils.load_products_from_file("ParserMirUpakovkiWithSeleniumDinamic_save_file.txt")
    # products = products_utils.loadProductsFromFile("stock_centr_save_file.txt")

    # logger.remove()

    render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)
    print(len(products))

    for name in products.products.keys():
        element_name = ElementName(name, [UnitsTypes.SHTUK])

        values_from_name = element_name.get_value_of_units_in_name()
        if  values_from_name != "":
            # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
            print(f'[+] {name:>100} | {values_from_name} {element_name.get_units_types()}')
        else:
            print(f'[-] {name:>100} | Null  {element_name.get_units_types()}')



if __name__ == '__main__':
    test_1_5()


