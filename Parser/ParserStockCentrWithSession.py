#
# 2025-05-08 - парсер работает исправно, тестируем
#
# возможны ошибки при запросе остатков
# решается обновлением значения data[hash]
# если будет мешать работе, найти автоматизированное решение
#

#
# Этот файл содержит дублирующийся код как в файле ParserLeroyMerlinWithSeleniumPagination.py
# Нужно продумать, как убрать дублирующийся код.
#

#
# При нормалной работе, после прохождениЯ тестов, завернуть в docker контейнер.
#


from ProductsElements.Products import Products
from ParserAbstract.Response import Response

# from ProductsElements.ProductsElement import ProductsElement
from ProductsElements.ProductsElementWithQuantity import ProductsElementWithQuantity
# from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from bs4 import BeautifulSoup
from ParserAbstract.ParserWithSession import ParserWithSession

from Utils.ProductsUtils import ProductsUtils

is_products_quantity_parsing_needed = True

import requests
from time import sleep

from Utils.ZabbixUtils import ZabbixUtils

import json
import re

class ParserStockCentrWithSession(ParserWithSession):
    _hash: str

    def __init__(self, siteUrl:str):
        self._hash = ""
        super().__init__(siteUrl)
        # self.set_current_page(0)
        # self.set_next_page_pause_time(0)

    def get_quantity_of_products(self):
        # получить количество товара на складе по url
        all_dict = self.get_products()
        for key in all_dict.keys():
            products_element = all_dict.get_element_by_name(key)
            url = products_element.get_url()

            # извлекаем productId из url
            # prod_id = url.split('-')[-1].replace('/', '')
            prod_id = url.split('/')[-1]

            quantity = self.get_quantity_by_product_id(prod_id, url)
            all_dict.get_element_by_name(key).set_quantity(quantity)

        # self.set_products(all_dict)
        logger.info(f'Остатки товаров на складах успешно получены')
        return all_dict

    def get_quantity_by_product_id(self, product_id, prod_url):

        REQUESTS_QUANTITY_MAX_ATTEMPTS = 5  # количество попыток загрузки страницы с данными по api
        REQUESTS_QUANTITY_TIMEOUT = 120     # время ожидания до следующей попытки

        MAX_PAGE_READ_ATTEMPTS = 5   # количество попыток загрузки страницы с данными
        MAX_PAGE_READ_TIMEOUT = 120  # время ожидания до следующей попытки (600 работает)
                                     # бывает устаревает qrator_jsid
        REQUESTS_CONNECT_TIMEOUT = 30  # тайм-аут подключения
        REQUESTS_READ_TIMEOUT = 28  # тайм-аут чтения

        url = 'https://stok-centr.com/my/s3/api/shop2/'

        cookies = {
        }


        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': '_ym_uid=1657170596902665083; referer=www.google.com; referer_referer=https%3A%2F%2Fwww.google.com%2F; referer_uri=%2F; referer_type=search; onc-61e611d5b887ee612f8b456a-url-ws=wss://n7.onicon.ru; onc-61e611d5b887ee612f8b456a-user-id=6646a98a7199b616628b885b; onc-61e611d5b887ee612f8b456a-user-hash=cc264b481b337fdd79be5012579e06c9; stats=1; referer_time=1724140462; code_verifier=TDlO0DMWkMNWENM551VUDOVyiODDMYDENlUNNWGB5QZ; s3_user_token=sKnEF8OCQwQL; _sntnl[en]=1; _ym_d=1724140439; _ym_isad=2; sh2lastfid=115408851; PRODUCT_RECENTLY_VIEWED_SHOP2_713051=%5B2157996506%2C1922734506%5D; _sntnl[dd]=2144879688',
            'origin': 'https://stok-centr.com',
            'priority': 'u=1, i',
            'referer': f'https://stok-centr.com/magazin/product/{product_id}',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'cmd': 'cartAddItem',
        }

        data = {
            # 'hash': '8e14c38a03aa1f63bbab1c6218cb9f31',
            'hash': self._hash,
            'ver_id': '987333',
            # 'kind_id': '1922734506',
            'kind_id': product_id,
            'amount': '9999',
        }

        import json

        # ============================================================

        for attempt in range(REQUESTS_QUANTITY_MAX_ATTEMPTS):
            response = None
            try:
                # REQUESTS_QUANTITY_TIMEOUT
                # logger.info(f'[{product_id=}] [{self._region_code=}]')
                logger.info(f'[{product_id=}] ')
                # response = requests.post(
                #     url=url,
                #     headers=headers,
                #     json=payload,
                #     timeout=REQUESTS_CONNECT_TIMEOUT,
                #     cookies=cookies
                # )

                # ==================
                response = requests.post(url, params=params, cookies=cookies,
                                         headers=headers, data=data)

                # context = json.loads(response.text)
                # text = context['errstr'].replace('Недостаточно товара "', '').replace('" на складе', '')
                # quantity = int(text.split(':')[1].strip())
                # == end ================

                # TODO обработка повторного запроса при ошибке
                if response.status_code == 200:
                    break
                if attempt == REQUESTS_QUANTITY_MAX_ATTEMPTS - 1:
                    logger.error(f'Не удалось прочитать страницу после [{REQUESTS_QUANTITY_MAX_ATTEMPTS=}]' +
                                 f' попыток [{REQUESTS_QUANTITY_TIMEOUT=}] [{response.status_code=}] [{response.cookies=}] {url=}')
                    logger.error(f'[{response=}]')

                    exit(1)
                # logger.warning(
                #     f'Не удачная попытка №[{attempt + 1}] спим [{MAX_PAGE_READ_TIMEOUT=}] ' +
                #     f'секунд, для получения контента со страницы  [{url}]'
                # )
                # sleep(REQUESTS_QUANTITY_TIMEOUT)
            except requests.exceptions.Timeout as error:
                logger.error(f"Ошибка запроса тайм-аут в post запросе о количестве" +
                             f" товара [попытка соединения № {attempt + 1}] {error}")
            except Exception as Err:
                logger.error(f"ошибка запроса без обработки {Err}")
            logger.warning(
                f'Не удачная попытка №[{attempt + 1}] спим [{MAX_PAGE_READ_TIMEOUT=}] ' +
                f'секунд, для получения контента со страницы [{response=}] [{url}]'
            )
            logger.warning( f'[{response.text[:120]=}]')
            logger.warning( f'[{response.cookies.get_dict()=}]')
            logger.warning(f'[{prod_url=}]')
            # 2023-03-24 17:16:56.821 | ERROR    | parsing_lerua_merilen:get_quantity_of_product_2:398 - Ошибка запроса тайм-аут в post запросе о количестве товара [попытка соединения № 1] HTTPSConnectionPool(host='api.leroymerlin.ru', port=443): Max retries exceeded with url: /experience/LeroymerlinWebsite/v1/navigation-pdp-api//get-stocks (Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection object at 0x00000237AE75D410>, 'Connection to api.leroymerlin.ru timed out. (connect timeout=30)'))
            # если будет мало времени, то можно увеличивать каждый следующий запрос
            #
            # или ошибка port=443): Max retries exceeded with url: /experience/LeroymerlinWebsite/v1/navigation-pdp-api//get-stocks
            # требует смены ip ????
            #
            # пока пробуем увеличить время между запросами

            sleep(REQUESTS_QUANTITY_TIMEOUT)

            # # === 15-03-2023 правка конец =========================================================

        # try:
        #     stores = response.json()['stocks']
        #     num = 0
        #     for store in stores:
        #         logger.info(f"{store['storeFullName']}, {store['stockValue']}")
        #         num += int(store['stockValue'])
        #
        # except Exception as Err:
        #     logger.info(f"Товара [{prod_url}][{payload['productId']}] нет в наличии {Err}")
        #     num = 0
        # logger.info(f'Всего товара [{num}] [{prod_url}]')

        # ==================
        try:
            num = 0
            context = json.loads(response.text)
            text = context['errstr'].replace('Недостаточно товара "', '').replace('" на складе', '')
            num = int(text.split(':')[1].strip())
            # ==================
            # print('# ', end='')
            # print(num)
            # == end ================
        except Exception as Err:
            logger.info(f"Товара [{prod_url}][{payload['productId']}] нет в наличии {Err}")
            num = 0
        logger.info(f'Всего товара [{num}] [{prod_url}]')
        # == end ================

        return num

#
# def run(str):
#     str = str.split('/')[-1]
#     print(str)


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



        # -- начало блока ---ищем значение hash ------------------
        if self._hash == '':
            try:
                soup = BeautifulSoup(response.html, 'html.parser')
                # soup = BeautifulSoup(html_content, 'lxml')
                script_tag = soup.find('script', string=re.compile(r'shop2\.init'))

                if script_tag:
                    script_text = script_tag.string
                    # Извлекаем JSON-объект с помощью регулярного выражения
                    json_match = re.search(r'shop2\.init\(({.*?})\);', script_text, re.DOTALL)
                    if json_match:
                        json_data = json.loads(json_match.group(1))
                        cart_add_item = json_data.get('apiHash', {}).get('cartAddItem')
                        logger.info(f'Удалось найти значние hash=[{cart_add_item}]')  # Вывод: 5653d8517a8fd631e7c89fa4bf9d1a36
                        self._hash = cart_add_item
                else:
                    logger.error("Нужный скрипт не найден [hash].")
                    exit(1)

            except Exception as Err:
                logger.error(f'Не удалось найти значение hash [{Err}]')
                exit(1)
        # logger.error(f'Удалось найти значение hash [{self._hash=}]')
        # exit(0)
        # -- конец блока --- ищем значение hash ------------------

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
            products.append(ProductsElementWithQuantity(item_name, float(item_price), product_url))
        return products


    # def sleepWithTimeForNextResponse(self):
    #     sleep()

# @timeit
def get_products_from_site(url, units_types, stop_list, region_code:str='habarovsk'):

    # parser = ParserLeroyMerlinWithSeleniumPagination(siteUrl=url, region_code=region_code)
    # parser = ParserStockCentrWithSession(siteUrl=url, region_code=region_code)
    parser = ParserStockCentrWithSession(siteUrl=url)

    # zabbix_config=zabbix_config,
    # units_types=["кг"]

    products = parser.get_products_from_site()

    logger.info(f'{len(products)=}')

    products_utils = ProductsUtils()
    cleaned_by_stop_list_products = products_utils.get_cleaned_products_by_stop_list(products, stop_list)
    cleaned_by_units_type = products_utils.get_cleaned_products_by_units_types(cleaned_by_stop_list_products,
                                                                               units_types)

    products_with_price_for_unit = products_utils.convert_price_to_price_for_unit(cleaned_by_units_type, units_types)

    # AttributeError: 'Products' object has no attribute 'get_quantity_of_products'
    parser.set_products(products_with_price_for_unit)

    # костыль

    # products_with_quantity = parser.get_quantity_of_products()

    global is_products_quantity_parsing_needed
    if is_products_quantity_parsing_needed == True:
        products_with_quantity = parser.get_quantity_of_products()
    else:
        return products_with_price_for_unit
    # конец костыля


    return products_with_quantity

def send_products_to_zabbix(zabbix_config, products):
    sender = ZabbixUtils(zabbix_config)
    sender.send_items_with_values(products, 'price_for_kg')

    # TODO
    #  кривое решение по внедрению возможности отправки цен и количества в разные узлы

    zabbix_qunatity_config = zabbix_config
    zabbix_qunatity_config['ZABBIX_HOST'] = zabbix_config['ZABBIX_HOST-QUANTITY']

    # костыль

    # sender2 = ZabbixUtils(zabbix_qunatity_config)
    # sender2.send_items_with_values(products, 'quantity')

    global is_products_quantity_parsing_needed
    if is_products_quantity_parsing_needed == True:
        sender2 = ZabbixUtils(zabbix_qunatity_config)
        sender2.send_items_with_values(products, 'quantity')
    # конец костыля


def main():
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    # parser = ParserStockCentrWithSession("https://stok-centr.com/magazin/folder/sukhiye-smesi/p/")
    parser = ParserStockCentrWithSession("https://stok-centr.com/magazin/folder/502822709/p/")
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
    products_utils.save_products_to_file(products, "stock_centr_with_session_save_file2.txt")


def main2():
    from DataRenderer import DataRenderer
    # from Products import Products
    from DataStrFormat import DataStrFormat
    from Utils.ProductsUtils import ProductsUtils
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


def main3():
    from DataRenderer import DataRenderer
    # from Products import Products
    from Utils.ProductsUtils import ProductsUtils
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
            # print(f'[+] {name:>100} | {values_from_name} {element_name.units_types}')
            print(f'[+] {name:>100} | {values_from_name} {element_name.get_units_types()}')
        else:
            # print(f'[-] {name:>100} | Null  {element_name.units_types}')
            print(f'[-] {name:>100} | Null  {element_name.get_units_types()}')


def main4():
    from DataRenderer import DataRenderer
    # from Products import Products
    from Utils.ProductsUtils import ProductsUtils
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
            # print(f'[+] {name:>100} | {values_from_name} {element_name.units_types}')
            print(f'[+] {name:>100} | {values_from_name} {element_name.get_units_types()}')
        else:
            # print(f'[-] {name:>100} | Null  {element_name.units_types}')
            print(f'[-] {name:>100} | Null  {element_name.get_units_types()}')

def main_working_version():
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat
    from UnitsTypes import UnitsTypes


    logger.add(
        "stok-centr-with-session.log",
        backtrace=True,
        diagnose=True,
        level='INFO',
        rotation="2 month",
        compression="zip"
    )

    logger.info('>>>>>>>>>>>>>>>>> Программа начала свою работу... <<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

    ZABBIX_SERVER_ADDRESS = '192.168.1.60'

    zabbix_config = {
        'ZABBIX_SERVER': f"http://{ZABBIX_SERVER_ADDRESS}",  # http://192.168.1.60   - не работает на ZabbixSender()
        'ZABBIX_USER': "Admin",
        'ZABBIX_PASSWORD': "zabbix",

        'ZABBIX_HOST': "Stok-Centr site price monitoring",
        'ZABBIX_HOST-QUANTITY': "Stok-Centr site quantity monitoring",
        'ZABBIX_SENDER_SERVER': ZABBIX_SERVER_ADDRESS  # работает на ZabbixSender() только без 'http://'
    }

    # СМЕСИ
    url='https://stok-centr.com/magazin/folder/502822709/p/'
    stop_list=[
        "латекс", "гипс", "замазка", "шпакрил", "керамзит", "мастика", "мел", "добавка", "жаростой",
        "шпатлевка", "шпатлёвк", "декоратив", "огнеупор", "наливной", "глино",
        "алебастр", "Шпаклевка", "газоблоков", "Шпаклёвка", "стекло", "Глина", "Бетонконтакт", "Финишпаста",
        "Краситель", "Плитонит", "Грунтовка", "Пропитка", "Ускоритель"
    ]

    # units_types=["кг"]
    units_types = [UnitsTypes.KG]

    # products_01 = get_products_from_site(url, units_types, stop_list)
    # send_products_to_zabbix(zabbix_config, products_01)


    # parser = ParserStockCentrWithSession("https://stok-centr.com/magazin/folder/sukhiye-smesi/p/")
    # parser = ParserStockCentrWithSession(url)
    # products = parser.get_products_from_site()
    products = get_products_from_site(url, units_types, stop_list)

    # render = DataRenderer()
    # print('\n\nproducts')
    # render.render(products, DataStrFormat.WIDE)

    #
    # from Utils.ProductsUtils import ProductsUtils
    #
    # render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)
    #
    # products_utils = ProductsUtils()
    # products_utils.save_products_to_file(products, "stock_centr_with_session_save_file2.txt")

    send_products_to_zabbix(zabbix_config, products)
    logger.info('>>>>>>>>>>>>>>>>>>> Программа закончила свою работу <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')


if __name__ == '__main__':
    # main()
    # main2()
    # main3()
    # main4()
    main_working_version()
    # run('https://stok-centr.com/magazin/product/3640806509')

