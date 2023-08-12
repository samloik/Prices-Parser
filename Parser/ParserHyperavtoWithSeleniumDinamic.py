
from Products import Products
# from ParserSite import ParserSite
from Response import Response
from ProductsElement import ProductsElement
# from time import sleep
# from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from bs4 import BeautifulSoup
from ParserWithSeleniumDinamicSite import ParserWithSeleniumDinamicSite
# from ParserWithSession import ParserWithSession


from time import sleep

from SeleniumNextPageTypes import SeleniumNextPageTypes

class ParserHyperavtoWithSeleniumDinamic(ParserWithSeleniumDinamicSite):

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl)

        btn_text = '\n                                Показать еще 30\n                                '
        self.next_x_path_button = f"//*[contains(text(), '{btn_text}')]"
        self.next_x_path_stop_content = None
        self.selenium_next_page_types = SeleniumNextPageTypes.NEXT_BUTTON_ABSENT
        self.setNextPagePauseTime(10)
    # return ProductFromSite main method
    # def getProductsFromSite(self):


    # # return isNextPage = self.checkForNextPage(html)
    # def isNextPage(self, response: Response):
    #
    #     soup = BeautifulSoup(response.html, 'lxml')
    #
    #     page_next = soup.find_all('div', attrs={'class': 'pagination__list'})
    #     print(f' {len(page_next)} {page_next=}')
    #     sleep(100)
    #     exit(0)
    #
    #     if len(page_next) > 0:
    #         logger.info(f'[{self.currentPage}] вызываем следующую страницу')
    #         self.currentPage += 1
    #         return True
    #     else:
    #         logger.info(f'[{self.currentPage}] это была последняя страница')
    #         return False


    # # return html page with main method
    # def getResponseFromSite(self):
    #     logger.info('Пытаемся получить ответ от сайта')
    #
    #     url = self.siteUrl + str(self.currentPage)
    #     response = self.webDriver.getHtmlPage(url)
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

        #
        # btns = [a for a in soup.find_all('button')]
        # logger.error(f'{len(btns)=}{btns=}')
        # # btns = btns.find('a').get('href')
        # logger.error(f'[{btns[49]=}]')
        # logger.error(f'[{btns[0].__dir__()=}]')
        # for x, btn in enumerate(btns):
        #     logger.info(f'[{x:02}] {repr(btn.text)}')
        #
        # exit(0)



        all_products = soup.find_all('div', {'class': "product-card__main"})
        logger.info(f'Получили от html страницы [{len(all_products)}] элементов')
        # exit(0)
        for next in all_products:
            # поиск значения значение наименование
            try:
                item_name2 = next.find('div', {'class': "product-card__title"})
                item_name = item_name2.find('a').text.replace('\n','').strip()
                # logger.error(f'{len(item_name2)=} {item_name2=}')
                # logger.error(f'{len(item_name)=} {item_name=}')
                # sleep(10)
                # exit(0)
            except Exception as Err:
                logger.error(f'Не удалось найти имя продукта [{Err}]')
                exit(1)
            # поиск значения значение цена
            try:
                item_price2 = next.find('span', {
                    'class': [
                        "price price_big price_green",
                        "price_big price_green",
                        "product-price-new__price product-price-new__price_main"
                    ]
                }).text
                item_price = item_price2.replace('\xa0', '').replace('\n', '').replace('₽', '').replace(' ', '').replace(',','.').replace('\u2009','')
                # logger.error(f'{len(item_price2)=} {item_price2=} ')
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
                url2 = next.find('div', {'class': "product-card__title"})
                url = url2.find('a').get('href')
                product_url = 'https://hyperauto.ru' + url
            except Exception as Err:
                logger.error(f'Не удалось найти URL продукта [{item_name}] [{Err}]')
                exit(1)

            # поиск значения Код
            try:
                item_name2 = next.find('div', {'class': "dotted-list__item-value"})
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
                item_name2 = next.find('div', {'title': "Артикул"})
                articul = item_name2.text.replace('\nАртикул\n', '').strip()
                # logger.error(f'{len(item_name2)=} {item_name2=}')
                # logger.error(f'{len(articul)=} {articul=}')
                # sleep(10)
                # exit(0)
            except Exception as Err:
                logger.error(f'Не удалось найти Код [{Err}]')
                exit(1)

            # поиск значения Бренд
            try:
                item_name2 = next.find('div', {'title': "Бренд"})
                brend = item_name2.text.replace('\nБренд\n', '').strip()
                # logger.error(f'{len(item_name2)=} {item_name2=}')
                # logger.error(f'{len(brend)=} {brend=}')
                # sleep(10)
                # exit(0)
            except Exception as Err:
                logger.error(f'Не удалось найти Код [{Err}]')
                exit(1)


            new_item_name = f"{kod}|{articul}|{brend}|{item_name}"
            logger.info(f"[добавление] {new_item_name=}:{item_price=}:{product_url=}")
            products.append(ProductsElement(new_item_name, float(item_price), product_url))
        # sleep(10)
        # exit(0)
        return products


    # def sleepWithTimeForNextResponse(self):
    #     sleep(10)



def main():
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils

    # parser = ParserHyperavtoWithSeleniumDinamic(
    #     "https://hyperauto.ru/komsomolsk/search/%D0%B0%D0%BA%D0%BA%D1%83%D0%BC%D1%83%D0%BB%D1%8F%D1%82%D0%BE%D1%80/"
    # )
    # parser = ParserHyperavtoWithSeleniumDinamic(
    #     "https://hyperauto.ru/oem/amortizator-podveski-toyota-4852049155/"
    # )
    # parser = ParserHyperavtoWithSeleniumDinamic(
    #     "https://hyperauto.ru/komsomolsk/search/%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%B0/"
    # )
    # https://hyperauto.ru/komsomolsk/search/%D0%B0%D0%BC%D0%BE%D1%80%D1%82%D0%B8%D0%B7%D0%B0%D1%82%D0%BE%D1%80/
    parser = ParserHyperavtoWithSeleniumDinamic(
        "https://hyperauto.ru/komsomolsk/search/%D0%B0%D0%BC%D0%BE%D1%80%D1%82%D0%B8%D0%B7%D0%B0%D1%82%D0%BE%D1%80/"
    )


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
    products_utils.saveProductsToFile(products, "ParserHyperavtoWithSeleniumDinamic_save_file.txt")


def main2():
    from DataRenderer import DataRenderer
    # from Products import Products
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils
    from ElementName import ElementName
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
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils
    from ElementName import ElementName
    from UnitsTypes import UnitsTypes

    products_utils = ProductsUtils()
    products = products_utils.loadProductsFromFile("ParserMirUpakovkiWithSeleniumDinamic_save_file.txt")
    # products = products_utils.loadProductsFromFile("stock_centr_save_file.txt")

    # logger.remove()

    render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)
    print(len(products))

    for name in products.products.keys():
        element_name = ElementName(name, [UnitsTypes.SHTUK])

        values_from_name = element_name.getValueOfUnitsInName()
        if  values_from_name != "":
            # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
            print(f'[+] {name:>100} | {values_from_name} {element_name.units_types}')
        else:
            print(f'[-] {name:>100} | Null  {element_name.units_types}')



if __name__ == '__main__':
    main()


