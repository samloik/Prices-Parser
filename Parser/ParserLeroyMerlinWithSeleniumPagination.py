
from Products import Products
# from ParserSite import ParserSite
from ParserAbstract.Response import Response
from ProductsElement import ProductsElement
# from time import sleep
# from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from bs4 import BeautifulSoup
from ParserAbstract.ParserWithSeleniumPaginationSite import ParserWithSeleniumPaginationSite
from time import sleep


class ParserLeroyMerlinWithSeleniumPagination(ParserWithSeleniumPaginationSite): # rename to SeleniumParser

    def __init__(self, siteUrl:str):
        super().__init__(siteUrl, 10, 5)

        self.next_x_path_button = '/html/body/div[1]/div/div[2]/main/div/div[5]/ul/li[last()]/a'
        self.next_x_path_button = '//*[@id="root"]/div/main/div[2]/div[2]/div/section/div[6]/section/div[2]/div/div/a[5]/span/div/svg'
        self.next_x_path_button = '//*[@id="root"]/div/main/div[2]/div[2]/div/section/div[6]/section/div[2]/div/div/a[5]'
        self.next_x_path_button = '//*[@id="root"]/div/main/div[2]/div[2]/div/section/div[6]/section/div[2]/div/div/a[5]/span/div/svg'
        self.next_x_path_button = '//*[@id="root"]/div/main/div[2]/div[2]/div/section/div[6]/section/div[2]/div/div/a[5]/span/div'
        self.next_x_path_button = '//*[@id="root"]/div/main/div[2]/div[2]/div/section/div[6]/section/div[2]/div/div/a[5]/span/div'
        # contains[aria-label="Следующая страница: 8"]
        self.next_x_path_button = '//*[@id="root"]/div/main/div[2]/div[2]/div/section/div[6]/section/div[2]/div/div'
        self.next_x_path_button = '//*[@id="root"]/div/main/div[2]/div[2]/div/section/div[6]/section/div[2]/div/div/a[5]'


        self.currentPage = 1
        self.setNextPagePauseTime(0)


    def isNextPage(self, response: Response):
        try:
            soup = BeautifulSoup(response.html, 'lxml')

            pages = soup.find(attrs={'aria-label': 'Pagination'}).findAll('a')

            # print(f'{len(pages)=} {pages=}')
            for item in pages:
                # print(f'{len(item)=} {item=}')

                if len(pages) > 0 and 'Следующая страница:' in pages[-1].attrs["aria-label"]:
                    logger.info(f'Следующая страница [{self.currentPage+1}] существует ')
                    return True

        except Exception as Err:
            logger.error(f'isNextPAge: {Err}')

        logger.info(f'"Это была последняя страница [{self.currentPage}]')
        return False



    # def isNextPage(self, response: Response):
    #     webElements = self.webDriver.driver.find_elements(By.XPATH, self.next_x_path_button)
    #
    #     # webElement = WebDriverWait(self.webDriver.driver, self.WAIT_PAUSE_TIM).until(
    #     #     EC.element_to_be_clickable((By.XPATH, self.next_x_path_button))
    #     # )
    #
    #     if len(webElements) > 0:
    #         logger.info(f'существует следующая страница')
    #         return True
    #
    #     logger.info(f'это была последняя страница')
    #     return False

    # return Products
    def getProductsFromResponse(self, response: Response):
        products = Products()

        # logger.info(f'{str(response)=}')

        soup = BeautifulSoup(response.html, 'lxml')
        all_products = soup.find_all(class_='po1t094_plp largeCard')
        logger.info(f'Получили от html страницы [{len(all_products)}] элементов')

        # sleep(100)

        for next in all_products:
            item_price = ""
            try:
                # меняют названия классов с "t3y6ha_plp xc1n09g_plp p1q9hgmc_plp" на "mvc4syb_plp"
                # TODO возможно будет плавать при изменении структуры, тогда доработать на примере
                item_name = next.find(class_='t9jup0e_plp').text
            except Exception as Err:
                logger.error(f'Не удалось найти имя продукта [{Err}]')
                exit(1)
            try:
                item_price = next.find(attrs={'data-qa': 'primary-price-main'}).text.replace('\xa0', '')
            except:
                pass
            try:
                item_price = next.find(attrs={'data-qa': 'new-price-main'}).text.replace('\xa0', '')
            except:
                pass

            try:
                # price = item.find(class_='_3rC-Ot1yr4_plp _1pNwL6sJc8_plp nfh3x0v_plp').text.replace('\xa0', '')
                item_price = next.find(attrs={'data-qa': 'best-price-main'}).text.replace('\xa0', '')
            except:
                pass

            if item_price == "":
                logger.error(f'Не удалось найти цену продукта [{item_name}]')

            try:
                product_url = 'https://habarovsk.leroymerlin.ru' + next.find('a', class_='bex6mjh_plp b1f5t594_plp ihytpj4_plp nf842wf_plp').get('href')
            except Exception as Err:
                logger.error(f'Не удалось найти URL продукта [{item_name}] [{Err}]')
                product_url = ""

            logger.info(f"[добавление] {item_name=}:{item_price=}:{product_url=}")
            products.append(ProductsElement(item_name, float(item_price), product_url))
        return products


    # def sleepWithTimeForNextResponse(self):
    #     sleep(10)



def main():
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    parser = ParserLeroyMerlinWithSeleniumPagination("https://habarovsk.leroymerlin.ru/catalogue/suhie-smesi-i-gruntovki/?page=")
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
    products_utils.saveProductsToFile(products, "ParserLeroyMerlinWithSeleniumPagination_save_file2.txt")


def main2():
    from DataRenderer import DataRenderer
    # from Products import Products
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils
    from UnitsTypes import UnitsTypes

    logger.remove()

    products_utils = ProductsUtils()
    products = products_utils.loadProductsFromFile("ParserLeroyMerlinWithSeleniumPagination_save_file.txt")

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)
    print(len(products))

    stop_list = [
        "латекс", "гипс", "замазка", "шпакрил", "керамзит", "мастика", "мел", "добавка", "жаростой",
        "шпатлевка", "шпатлёвк", "декоратив", "огнеупор", "наливной", "глино",
        "алебастр", "Шпаклевка", "газоблоков", "Шпаклёвка", "стекло", "Глина", "Бетонконтакт", "Финишпаста",
        "Краситель", "Плитонит", "Грунтовка", "Пропитка", "Ускоритель"
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

    products_utils.saveProductsToFile(el, "cleaned_ParserLeroyMerlinWithSeleniumPagination_save_file.txt")



def main3():
    from DataRenderer import DataRenderer
    # from Products import Products
    from ProductsUtils import ProductsUtils
    from ElementName import ElementName
    from UnitsTypes import UnitsTypes

    products_utils = ProductsUtils()
    products = products_utils.loadProductsFromFile("cleaned_ParserLeroyMerlinWithSeleniumPagination_save_file.txt")
    # products = products_utils.loadProductsFromFile("stock_centr_save_file.txt")

    # logger.remove()

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


