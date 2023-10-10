
from ProductsElements.Products import Products
# from ParserSite import ParserSite
from ParserAbstract.Response import Response
from ProductsElements.ProductsElementWithContent import ProductsElementWithContent
# from time import sleep
# from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from bs4 import BeautifulSoup
from ParserAbstract.ParserWithSeleniumDinamicSite import ParserWithSeleniumDinamicSite
# from ParserWithSession import ParserWithSession

from ParserAbstract.SeleniumNextPageTypes import SeleniumNextPageTypes

def get_price_string_from_string(string:str):
    if not isinstance(string, str) and len(string)==0:
        return 'None - не удалочь найти цену'
    if not  string[0].isdigit():
        return string
    new_string = string.replace('\xa0', '').replace('₽', '')
    return new_string

class ParserAvitoWithSeleniumDinamic(ParserWithSeleniumDinamicSite): # rename to SeleniumParser

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl)

        self.next_x_path_button = "//*[@id='app']/div/div[3]/div/div[2]/div[3]/div[3]/div[3]/nav/ul/li[6]/a/svg"
        self.next_x_path_stop_content = None
        self.selenium_next_page_types = SeleniumNextPageTypes.NEXT_BUTTON_ABSENT
        self.set_next_page_pause_time(3)


    # return Products
    def get_products_from_response(self, response: Response):
        products = Products()

        soup = BeautifulSoup(response.html, 'lxml')
        all_products = soup.find_all('div', {'data-marker': "item"})
        logger.info(f'Получили от html страницы [{len(all_products)}] элементов')
        for next in all_products:
            try:
                # item_name = next.find(class_="product-name").text
                item_name = next.find('h3', {'class': "styles-module-root-TWVKW styles-module-root-_KFFt styles-module-size_l-_oGDF styles-module-size_l-hruVE styles-module-ellipsis-LKWy3 styles-module-weight_bold-Kpd5F stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-header-l-qvNIS"}).text
                # logger.error(f'{len(item_name)=} {item_name=}')
                # sleep(10)
                # exit(0)
            except Exception as Err:
                logger.error(f'Не удалось найти имя продукта [{Err}]')
                exit(1)
            try:
                # pr = next.find('span', {'class': "product-item-price-current"})
                item_price = next.find('strong', {'class': "styles-module-root-LIAav"}).find('span').text
                item_price = float(get_price_string_from_string(item_price))
                # item_price = item_price.replace('р.', '').replace('\n', '').replace('\t', '').replace(' ', '')
                # logger.error(f'{len(item_price)=} {item_price=} ')
                # item_price2 = item_price.text
                # logger.error(f'{len(item_price2)=} {item_price2=} ')
                # sleep(10)
                # exit(0)
            except Exception as Err:
                # TODO
                #  Продумать нужны ли элементы без цены в списке?
                logger.info(f'Не удалось найти цену продукта [{item_name}] [{Err}]')
                logger.error(f'Элемент [{item_name}] не попадает в список')
                continue
            try:
                product_url = 'https://www.avito.ru' + next.find('div', {'class': "iva-item-title-py3i_"}).find('a').get('href')
            except Exception as Err:
                logger.error(f'Не удалось найти URL продукта [{item_name}] [{Err}]')
                exit(1)

            content = ''
            try:
                content = next.find('div', {'class': "iva-item-descriptionStep-C0ty1"}).find('p')
                # logger.error(f'{len(content)=} {content=} ')
                content2 = content.text.replace('\xa0','')
                # logger.error(f'{len(content2)=} {content2=} ')
                # sleep(10)
                # exit(0)
                content = content2
            except Exception as Err:
                logger.error(f'Не удалось найти URL продукта [{item_name}] [{Err}]')
                exit(1)

            logger.info(f"[добавление] {item_name=}:{item_price=}:{product_url=} {content=}")
            products.append(
                ProductsElementWithContent(
                    item_name, float(item_price), product_url, {'text': content}
                )
            )
            # sleep(10)
            # exit(0)
        return products


    # def sleepWithTimeForNextResponse(self):
    #     sleep(10)



def xtest():
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    # parser = ParserMirUpakovkiWithSeleniumDinamic("https://khv.mirupak.ru/catalog/khv/posuda_odnorazovaya_2/")
    parser = ParserAvitoWithSeleniumDinamic(
        "https://www.avito.ru/komsomolsk-na-amure/noutbuki?cd=1&p=1"
    )
    products = parser.get_products_from_site()

    render = DataRenderer()
    print('\n\nproducts')
    render.render(products, DataStrFormat.WIDE)

    # from DataRenderer import DataRenderer
    # from Products import Products
    # from DataStrFormat import DataStrFormat
    from Utils.ProductsUtils import ProductsUtils

    # render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)

    products_utils = ProductsUtils()
    products_utils.save_products_to_file(products, "ParserAvitoWithSeleniumDinamic_noutbooki_save_file.txt")


# def test_1_5():
#     from DataRenderer import DataRenderer
#     from DataStrFormat import DataStrFormat
#
#     # parser = ParserMirUpakovkiWithSeleniumDinamic("https://khv.mirupak.ru/catalog/khv/posuda_odnorazovaya_2/")
#     parser = ParserMirUpakovkiWithSeleniumDinamic(
#         "https://khv.mirupak.ru/catalog/khv/pakety_bez_risunka_i_meshki/meshki_/"
#     )
#     products = parser.get_products_from_site()
#
#     render = DataRenderer()
#     print('\n\nproducts')
#     render.render(products, DataStrFormat.WIDE)
#
#     # from DataRenderer import DataRenderer
#     # from Products import Products
#     # from DataStrFormat import DataStrFormat
#     from ProductsUtils import ProductsUtils
#
#     render = DataRenderer()
#     render.render(products, DataStrFormat.WIDE)
#
#     products_utils = ProductsUtils()
#     products_utils.save_products_to_file(products, "ParserMirUpakovkiWithSeleniumDinamic_save_file.txt")
#
#
#
# def test2():
#     from DataRenderer import DataRenderer
#     # from Products import Products
#     from DataStrFormat import DataStrFormat
#     from ProductsUtils import ProductsUtils
#     from UnitsTypes import UnitsTypes
#
#     logger.remove()
#
#     products_utils = ProductsUtils()
#     products = products_utils.load_products_from_file("stock_centr_save_file.txt")
#
#     render = DataRenderer()
#     render.render(products, DataStrFormat.WIDE)
#     print(len(products))
#     products_utils.save_products_to_file(products, "cleaned_stock_centr_save_file.txt")
#
#     stop_list = [
#         "латекс", "гипс", "замазка", "шпакрил", "керамзит", "мастика", "мел", "добавка", "жаростой",
#         "шпатлевка", "шпатлёвк", "декоратив", "огнеупор", "наливной", "глино"
#         # "клей"
#     ]
#
#     cleaned_by_stop_list_products = products_utils.get_cleaned_products_by_stop_list(products, stop_list)
#
#     print('Очистка по стоп словам')
#
#     render.render(cleaned_by_stop_list_products, DataStrFormat.WIDE)
#     print(len(cleaned_by_stop_list_products))
#
#     print('Очистка по отсутвию единицы измерения (кг!, литр):')
#
#     cleaned_by_units_type = products_utils.get_cleaned_products_by_units_types(cleaned_by_stop_list_products,
#                                                                           [UnitsTypes.KG, UnitsTypes.LITR])
#
#     render.render(cleaned_by_units_type, DataStrFormat.WIDE)
#     print(len(cleaned_by_units_type))
#
#     print()
#
#     el = products_utils.convert_price_to_price_for_unit(cleaned_by_units_type, [UnitsTypes.KG, UnitsTypes.LITR])
#
#     print('Цена за единицу:')
#
#     render.render(el, DataStrFormat.WIDE)
#     print(len(el))
#
#
# def test3():
#     from DataRenderer import DataRenderer
#     # from Products import Products
#     from ProductsUtils import ProductsUtils
#     from ProductsElements.ElementName import ElementName
#     from UnitsTypes import UnitsTypes
#
#     products_utils = ProductsUtils()
#     products = products_utils.load_products_from_file("ParserMirUpakovkiWithSeleniumDinamic_save_file.txt")
#     # products = products_utils.loadProductsFromFile("stock_centr_save_file.txt")
#
#     # logger.remove()
#
#     render = DataRenderer()
#     # render.render(products, DataStrFormat.WIDE)
#     print(len(products))
#
#     for name in products.products.keys():
#         element_name = ElementName(name, [UnitsTypes.SHTUK])
#
#         values_from_name = element_name.get_value_of_units_in_name()
#         if  values_from_name != "":
#             # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
#             print(f'[+] {name:>100} | {values_from_name} {element_name.get_units_types()}')
#         else:
#             print(f'[-] {name:>100} | Null  {element_name.get_units_types()}')



if __name__ == '__main__':
    # print(get_price_string_from_string('10\xa0000\xa0₽'))
    xtest()
