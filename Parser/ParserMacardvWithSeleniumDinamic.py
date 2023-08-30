
from Products import Products
# from ParserSite import ParserSite
from ParserAbstract.Response import Response
# from ProductsElement import ProductsElement
from ParserProductComparison.ProductsElementAvto import ProductsElementAvto
from time import sleep
# from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from bs4 import BeautifulSoup
from ParserAbstract.ParserWithSeleniumDinamicSite import ParserWithSeleniumDinamicSite
# from ParserWithSession import ParserWithSession

from ParserAbstract.SeleniumNextPageTypes import SeleniumNextPageTypes

class ParserMacardvWithSeleniumDinamic(ParserWithSeleniumDinamicSite): # rename to SeleniumParser

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl, 10, 3)

        self.next_x_path_button = "//*[@id='show-more-catalog-items']/div[2]" # все на одной странице
        self.next_x_path_stop_content = None
        self.selenium_next_page_types = SeleniumNextPageTypes.NEXT_BUTTON_ABSENT
        # self.set_next = self.set_next_page_pause_time(5)

    # return Products
    def get_products_from_response(self, response: Response):
        products = Products()

        soup = BeautifulSoup(response.html, 'lxml')

        all_products = soup.find_all('tr')[2:] #, {'class': "product-card__main"})
        logger.info(f'Получили от html страницы [{len(all_products)}] элементов')
        # exit(0)
        for next in all_products:
            # поиск значения значение наименование
            try:
                item_name2 = next.find('td', {'class': "resultDescription"})
                item_name = item_name2.text.replace('\n','').replace('\t','')  #.strip()
                # logger.error(f'{len(item_name2)=} {item_name2=}')
                # logger.error(f'{len(item_name)=} {item_name=}')
                # item_name3 = next.find('td', {'data-label':"Доп. информация"})
                # item_name4 = item_name3.text.replace('\n','').replace('\t','')  #.strip()
                # logger.error(f'{len(item_name3)=} {item_name3=}')
                # logger.error(f'{len(item_name4)=} {item_name4=} {repr(item_name4)=}')
                # item_name = item_name + '|' + item_name4
                # logger.info(f'{len(item_name)=} {item_name=}')
                # sleep(10)
                # exit(0)

            except Exception as Err:
                logger.error(f'Не удалось найти имя продукта [{Err}]')
                exit(1)
            # поиск значения значение цена
            try:
                item_price2 = next.find('td', { 'class': "resultPrice"}).text
                item_price = item_price2.replace('\n','').replace('\t','').replace('руб.', '').replace(' ','')
                # logger.error(f'{len(item_price2)=} {item_price2=} {repr(item_price2)=} ')
                # logger.error(f'{len(item_price)=} {item_price=} ')
                # sleep(10)
                # exit(0)
            except Exception as Err:
                # TODO
                #  Продумать нужны ли элементы без цены в списке?
                logger.info(f'Не удалось найти цену продукта [{item_name}] [{Err}]')
                logger.error(f'Элемент [{item_name}] не попадает в список')
                continue
            # поиск значения url
            try:
                # url2 = next.find('div', {'class': "product-card__title"})
                # url = ''
                product_url = ''
            except Exception as Err:
                logger.error(f'Не удалось найти URL продукта [{item_name}] [{Err}]')
                exit(1)

            # поиск значения Код
            try:
                item_name2 = next.find('div', {'class': "brand"})
                kod = item_name2.text.strip()
                # logger.error(f'{len(item_name2)=} {item_name2=}')
                # logger.error(f'{len(kod)=} {kod=}')
                # sleep(10)
                # exit(0)
            except Exception as Err:
                logger.error(f'Не удалось найти Код [{Err}]')
                exit(1)
            # поиск значения Артикул
            try:
                # item_name2 = next.find('div', {'title': "Артикул"})
                articul = ''
                # logger.error(f'{len(item_name2)=} {item_name2=}')
                # logger.error(f'{len(articul)=} {articul=}')
                # sleep(10)
                # exit(0)
            except Exception as Err:
                logger.error(f'Не удалось найти Артикул [{Err}]')
                exit(1)

            # поиск значения Бренд
            try:
                item_name2 = next.find('a', {'class': "open-abcp-modal-info"})
                brend = item_name2.text.strip()
                # logger.error(f'{len(item_name2)=} {item_name2=}')
                # logger.error(f'{len(brend)=} {brend=}')
                # sleep(10)
                # exit(0)
            except Exception as Err:
                logger.error(f'Не удалось найти Бренд [{Err}]')
                exit(1)

            # поиск значения Адрес
            try:
                item_name2 = next.find('td', {'data-label': "Доп. информация"})
                adress = item_name2.text.strip()
                # logger.error(f'{len(item_name2)=} {item_name2=}')
                # logger.error(f'{len(adress)=} {adress=}')

                # sleep(10)
                # exit(0)
                if not len(adress):
                    continue
            except Exception as Err:
                logger.error(f'Не удалось найти Адрес [{Err}]')
                exit(1)

            # поиск значения Количество
            try:
                item_name2 = next.find('input', {'name': "quantity"})
                # logger.error(f'{len(item_name2)=} {item_name2=}')
                quantity = item_name2['data-wrong-multiplicityvalue-all']
                quantity = quantity.replace('Возможно заказать только всю партию (','').replace(' шт.)','')
                # logger.error(f'{len(quantity)=} {quantity=}')
                # sleep(10)
                # exit(0)
            except Exception as Err:
                logger.error(f'Не удалось найти Количество [{Err}]')
                exit(1)


            new_item_name = f"{kod}|{articul}|{brend}|{item_name}"
            logger.info(f"[добавление] {kod}|{articul}|{brend}|{item_name}|{item_price=}|{product_url=}")
            # products.append(ProductsElement(new_item_name, float(item_price), product_url))
            products.append(ProductsElementAvto(
                name = item_name,
                price = item_price,
                url = product_url,
                kod = kod,
                article = articul,
                brend = brend,
                adress = adress,
                quantity = quantity
            ))
            # sleep(10)
            # exit(0)
        return products


    # def sleepWithTimeForNextResponse(self):
    #     sleep(10)



def test():
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat


    parser = ParserMacardvWithSeleniumDinamic(
        "https://macardv.ru/search?pcode=%D0%B0%D0%BA%D0%BA%D1%83%D0%BC%D1%83%D0%BB%D1%8F%D1%82%D0%BE%D1%80"
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
    products_utils.save_products_to_file(products, "ParserMacardvWithSeleniumDinamic_save_file.txt")


def test2():
    from DataRenderer import DataRenderer
    # from Products import Products
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils
    from UnitsTypes import UnitsTypes

    logger.remove()

    products_utils = ProductsUtils()
    products = products_utils.load_products_from_file("ParserMacardvWithSeleniumDinamic_save_file_save_file.txt")

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)
    print(len(products))
    products_utils.save_products_to_file(products, "cleaned_ParserMacardvWithSeleniumDinamic_stock_centr_save_file.txt")

    stop_list = [
        "клеммы", "Крепление"
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
    from ElementName import ElementName
    from UnitsTypes import UnitsTypes

    products_utils = ProductsUtils()
    products = products_utils.load_products_from_file("ParserMacardvWithSeleniumDinamic_save_file.txt")
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
            print(f'[+] {name:>100} | {values_from_name} {element_name.units_types}')
        else:
            print(f'[-] {name:>100} | Null  {element_name.units_types}')



if __name__ == '__main__':
    test()


