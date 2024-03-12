
from ProductsElements.Products import Products
# from ParserSite import ParserSite
from ParserAbstract.Response import Response
from ProductsElements.ProductsElementWithQuantity import ProductsElementWithQuantity
# from time import sleep
# from SeleniumWebDriver import SeleniumWebDriver
from loguru import logger
from bs4 import BeautifulSoup
from ParserAbstract.ParserWithSeleniumPaginationSite import ParserWithSeleniumPaginationSite

import requests
from time import sleep
from time_decorator import timeit
from UnitsTypes import UnitsTypes
from Utils.ProductsUtils import ProductsUtils
from Utils.ZabbixUtils import ZabbixUtils


class ParserLeroyMerlinWithSeleniumPagination(ParserWithSeleniumPaginationSite):

    def __init__(self, siteUrl:str, region_code:str='habarovsk'):
        super().__init__(siteUrl, 5, 0)
        self._region_code = region_code

        self.next_x_path_button = '//*[@id="root"]/div/main/div[2]/div[2]/div/section/div[6]/section/div[2]/div/div/a[5]'


        self.set_current_page(1)
        self.set_next_page_pause_time(0)

    def get_quantity_of_products(self):
        # получить количество товара на складе по url
        all_dict = self.get_products()
        for key in all_dict.keys():
            products_element = all_dict.get_element_by_name(key)
            url = products_element.get_url()

            # извлекаем productId из url
            prod_id = url.split('-')[-1].replace('/', '')

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

        url = 'https://api.leroymerlin.ru/experience/LeroymerlinWebsite/v1/navigation-pdp-api//get-stocks'
        # url = 'https://178.248.235.76/experience/LeroymerlinWebsite/v1/navigation-pdp-api//get-stocks'

        cookies = {
            # '_ym_uid': '1657256896505620381',
            # '_ym_d': '1674454474',
            # 'cookie_accepted': 'true',
            # 'iap.uid': '2ca7dc1bbd554eaa8dc5a2323ab3d547',
            # 'tmr_lvid': 'b3e9dace7a48624c471d2d49640d6ecc',
            # 'tmr_lvidTS': '1657256895948',
            # 'aplaut_distinct_id': 'YVodqfQhgzTT',
            # 'uxs_uid': '3537efc0-9ae5-11ed-8a9d-954c1edc4e2b',
            # 'adrcid': 'AGEqwyQCsGm71wCny_JPupg',
            # 'X-API-Experiments-sub': 'B',
            # 'sawOPH': 'true',
            # 'user-geolocation': '0%2C0',
            # 'x-api-option': 'default-cce-309',
            # 'fromRegion': '34',
            # '_gaexp': 'GAX1.2.zv9EWltXRUeeE5C_zMiEbg.19487.1',
            # 'customerId': '105547923',
            # 'user-auth': 'true',
            # '_gcl_au': '1.1.1042180285.1677046168',
            # 'sid': 'G7lUk6pxyYoFcmIO3reMpmj_yPVpLPeQ.euGK9jw8UmRQqKQ%2FXumvUGeEDhs7ewyFsoi2fTYLg9g',
            # 'disp_react_aa': '2',
            # 'ggr-widget-test': '1',
            # '_gid': 'GA1.2.326691577.1677750879',
            # '_ym_isad': '2',
            # '_singleCheckout': 'true',
            # '_unifiedCheckout': 'true',
            # '_pickupMapSearch': 'true',
            # 'cartInfo': '81946281%3A1',
            # '_b2bBill': 'true',
            # '_ym_visorc': 'b',
            # 'GACookieStorage': 'GA1.3.75636049.1674454475',
            # 'storageForShopListActual': 'true',
            # 'lastConfirmedRegionID': '4124',
            # 'access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL2xlcm95LW1lcmxpbi1ydS1wcm9kLnJlYWNoNS5uZXQiLCJzdWIiOiJBWVozdTQyb05ZMk84TFJsTUQ1OSIsImV4cCI6MTY3NzkxOTM0NiwiaWF0IjoxNjc3OTE1NzQ2LCJqdGkiOiJnaDFsQVZ5aFZPOjE4IiwiYXVkIjpbImh0dHBzOi8vbGVyb3ktbWVybGluLXJ1LXByb2QucmVhY2g1Lm5ldC9pZGVudGl0eSJdLCJzY29wZSI6ImVtYWlsIGZ1bGxfd3JpdGUgb2ZmbGluZV9hY2Nlc3Mgb3BlbmlkIHBob25lIHByb2ZpbGUiLCJlbmZvcmNlc19zY29wZSI6dHJ1ZSwiY2xpZW50X2lkIjoiSDBCbUd1UTcySktUemluczFxSVgiLCJleHRlcm5hbF9pZCI6IjEwNTU0NzkyMyIsImF1dGhfdGltZSI6MTY3NzA0NjAyNywiYXpwIjoiSDBCbUd1UTcySktUemluczFxSVgiLCJpYXRfbXMiOjQ0MiwiYW1yIjpbInB3ZCJdfQ.bixZNs2rZxakul6P0MfU3Y2CxsvkNMz5it9tCCyQ9n_KuVkT2rfnAcnm6iTCTFz9TOH_HCT7pUzjyD0oQlcu1C_BHPnE4ZLAmEke-rDqGYBHVTe1aiZVoVn6OpokJYIqfFhm9ocloo7bxdy6ec1hg3XxKcgvf5Hh0eyMl4ySHAfhKNoXaRNyDz1rthArBmk7FJxXfKng3BjXc3synnB6N6x537HOMNE_ERmePWy-rl7jqZmolNg8RiS8wrcxddgDNIq1XJt_NR3rLGQVoRoOJr11_1Eb43NCdW6ltbbm58LymUZrvj8lpoFI1tigoiUwQ7v-4W9GwwkNpINRzF_QXw',
            # 'access-expire-date': '1677919346',
            # 'qrator_ssid': '1677915746.772.KeyQYp2KqT65bnMx-h5bo8d3bvqh34qv8nno8p76omj3de3t3',
            # '_regionID': '4124',
            # 'qrator_jsid': '1677915911.150.ftpjJUNR806XGg2K-9e2g5ilisgte1256uq22sunilkukq1en',
            # '_ga': 'GA1.2.75636049.1674454475',
            # '_gat_UA-20946020-1': '1',
            # '_ga_Z72HLV7H6T': 'GS1.1.1677914797.14.1.1677917014.0.0.0',
        }



        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            # 'Cookie': '_ym_uid=1657256896505620381; cookie_accepted=true; iap.uid=2ca7dc1bbd554eaa8dc5a2323ab3d547; tmr_lvid=b3e9dace7a48624c471d2d49640d6ecc; tmr_lvidTS=1657256895948; aplaut_distinct_id=YVodqfQhgzTT; uxs_uid=3537efc0-9ae5-11ed-8a9d-954c1edc4e2b; adrcid=AGEqwyQCsGm71wCny_JPupg; X-API-Experiments-sub=B; sawOPH=true; user-geolocation=0%2C0; fromRegion=34; customerId=105547923; sid=G7lUk6pxyYoFcmIO3reMpmj_yPVpLPeQ.euGK9jw8UmRQqKQ%2FXumvUGeEDhs7ewyFsoi2fTYLg9g; plp:facet:eligibilityByStores=%D0%A5%D0%B0%D0%B1%D0%B0%D1%80%D0%BE%D0%B2%D1%81%D0%BA; _slid=644ef74f8600a009a40705a6; _slid_server=644ef74f8600a009a40705a6; lastConfirmedRegionID=4124; x-api-option=cce-411; plpView=largeCard; _ym_d=1690262460; ggr-widget-test=1; qrator_jsr=1693646587.763.sPSqBBafAdkff4B1-roo3nqaf1dk8sdanp1s3drodhfs5mobq-00; qrator_jsid=1693646587.763.sPSqBBafAdkff4B1-i9k8p6gf8j4oruv5pc23i64gpgc3oc2j; qrator_ssid=1693646591.077.SC4j6jdMpmcFkuAo-pb7q6ti45aqrjl62tvtr1hfs9a35r4od; _reactCheckout=true; _b2bCheckout3=true; _gaPurchaseNew=true; _gid=GA1.2.310122151.1693646609; _ym_isad=2; _ga_Y706PSX1XZ=GS1.1.1693646611.15.0.1693646611.0.0.0; GACookieStorage=GA1.3.75636049.1674454475; _ym_visorc=b; adrdel=1; _regionID=4124; _ga=GA1.2.75636049.1674454475; _gat_UA-20946020-1=1; _ga_Z72HLV7H6T=GS1.1.1693646609.74.1.1693646717.0.0.0',
            'Origin': 'https://habarovsk.leroymerlin.ru',
            'Referer': 'https://habarovsk.leroymerlin.ru/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-api-key': 'nkGKLkscp80GVAQVY8YvajPjzaFTmIS8',
            # 'x-request-id': '2075a32a32498200da0fc554606cda4c',
        }

        payload = {
            # 'regionCode': 'habarovsk',
            'regionCode': self._region_code,
            # 'productId': '13857214',
            'productId': product_id,
            'unit': 'шт.',
            'currencyKey': 'RUB',
            'preferedStores': [],
            'source': 'Step',
        }

        # ============================================================

        for attempt in range(REQUESTS_QUANTITY_MAX_ATTEMPTS):
            response = None
            try:
                # REQUESTS_QUANTITY_TIMEOUT
                logger.info(f'[{product_id=}] [{self._region_code=}]')
                response = requests.post(
                    url=url,
                    headers=headers,
                    json=payload,
                    timeout=REQUESTS_CONNECT_TIMEOUT,
                    cookies=cookies
                )
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
            logger.warning( f'[{response.text[:80]=}]')
            logger.warning( f'[{response.cookies.get_dict()=}]')
            # 2023-03-24 17:16:56.821 | ERROR    | parsing_lerua_merilen:get_quantity_of_product_2:398 - Ошибка запроса тайм-аут в post запросе о количестве товара [попытка соединения № 1] HTTPSConnectionPool(host='api.leroymerlin.ru', port=443): Max retries exceeded with url: /experience/LeroymerlinWebsite/v1/navigation-pdp-api//get-stocks (Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection object at 0x00000237AE75D410>, 'Connection to api.leroymerlin.ru timed out. (connect timeout=30)'))
            # если будет мало времени, то можно увеличивать каждый следующий запрос
            #
            # или ошибка port=443): Max retries exceeded with url: /experience/LeroymerlinWebsite/v1/navigation-pdp-api//get-stocks
            # требует смены ip ????
            #
            # пока пробуем увеличить время между запросами

            sleep(REQUESTS_QUANTITY_TIMEOUT)

            # # === 15-03-2023 правка конец =========================================================

        try:
            stores = response.json()['stocks']
            num = 0
            for store in stores:
                logger.info(f"{store['storeFullName']}, {store['stockValue']}")
                num += int(store['stockValue'])

        except Exception as Err:
            logger.info(f"Товара [{prod_url}][{payload['productId']}] нет в наличии {Err}")
            num = 0
        logger.info(f'Всего товара [{num}] [{prod_url}]')

        return num


    def get_products_from_site(self):
        products = super(ParserLeroyMerlinWithSeleniumPagination, self).get_products_from_site()

        return products


    def is_next_page(self, response: Response):
        try:
            soup = BeautifulSoup(response.html, 'lxml')
            pages = soup.find(attrs={'aria-label': 'Pagination'}).findAll('a')

            # print(f'{len(pages)=} {pages=}')
            for item in pages:
                # print(f'{len(item)=} {item=}')

                if len(pages) > 0 and 'Следующая страница:' in pages[-1].attrs["aria-label"]:
                    logger.info(f'Следующая страница [{self.get_current_page()+1}] существует ')
                    return True

        except Exception as Err:
            logger.error(f'[{str(response)=}] {Err}')

        logger.info(f'Это была последняя страница [{self.get_current_page()}]')
        return False



    def get_products_from_response(self, response: Response):
        products = Products()

        # logger.info(f'{str(response)=}')

        soup = BeautifulSoup(response.html, 'lxml')
        # logger.warning(f'{soup=}')
        # all_products = soup.find_all(class_='po1t094_plp largeCard')
        all_products = soup.find_all(class_='p155f0re_plp largeCard')
        logger.info(f'Получили от html страницы [{len(all_products)}] элементов')

        # sleep(100)

        for next in all_products:
            item_price = ""
            try:
                # меняют названия классов с "t3y6ha_plp xc1n09g_plp p1q9hgmc_plp" на "mvc4syb_plp"
                # TODO возможно будет плавать при изменении структуры, тогда доработать на примере
                # item_name = next.find(class_='t9jup0e_plp').text
                item_name = next.find(class_='p1h8lbu4_plp').text
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
            products.append(ProductsElementWithQuantity(item_name, float(item_price.replace(',','.')), product_url))
        return products



def run():
    # проверяем как парсятся товарные позиции с сайта
    # проверяем как загружаются в файл

    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    parser = ParserLeroyMerlinWithSeleniumPagination("https://habarovsk.leroymerlin.ru/catalogue/suhie-smesi-i-gruntovki/?page=")
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
    products_utils.save_products_to_file(products, "ParserLeroyMerlinWithSeleniumPagination_save_file3.txt")


def run2():
    # проверяем как загружаются из файла
    # проверяем как очищается список по стоп словам
    # проверяем как очищается по отсуствию единиц измерения меры в имени (кг, литры, шт)
    # проверяем как конвертируется цена в цену за единицу
    # проверяем как загружаются в файл

    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat
    from Utils.ProductsUtils import ProductsUtils
    from UnitsTypes import UnitsTypes

    logger.remove()

    products_utils = ProductsUtils()
    products = products_utils.load_products_from_file("ParserLeroyMerlinWithSeleniumPagination_save_file.txt")

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)
    print(len(products))

    stop_list = [
        "латекс", "гипс", "замазка", "шпакрил", "керамзит", "мастика", "мел", "добавка", "жаростой",
        "шпатлевка", "шпатлёвк", "декоратив", "огнеупор", "наливной", "глино",
        "алебастр", "Шпаклевка", "газоблоков", "Шпаклёвка", "стекло", "Глина", "Бетонконтакт", "Финишпаста",
        "Краситель", "Плитонит", "Грунтовка", "Пропитка", "Ускоритель"
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

    products_utils.save_products_to_file(el, "cleaned_ParserLeroyMerlinWithSeleniumPagination_save_file.txt")


def run3():
    # проверяем как загружаются из файла
    # проверяем как извлекаются единицы измерения из имен

    from DataRenderer import DataRenderer
    from Utils.ProductsUtils import ProductsUtils
    from ProductsElements.ElementName import ElementName
    from UnitsTypes import UnitsTypes

    products_utils = ProductsUtils()
    products = products_utils.load_products_from_file("cleaned_ParserLeroyMerlinWithSeleniumPagination_save_file.txt")

    # logger.remove()

    render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)
    print(len(products))

    for name in products.products.keys():
        element_name = ElementName(name, [UnitsTypes.KG, UnitsTypes.LITR])

        values_from_name = element_name.get_value_of_units_in_name()
        if  values_from_name != "":
            print(f'[+] {name:>100} | {values_from_name} {element_name.get_units_types()}')
        else:
            print(f'[-] {name:>100} | Null  {element_name.get_units_types()}')

@timeit
def run4():
    # проверяем как загружаются из файла
    # проверяем как очищается список по стоп словам
    # проверяем как очищается по отсуствию единиц измерения меры в имени (кг, литры, шт)
    # проверяем как конвертируется цена в цену за единицу
    # проверяем как парсятся остаки товара
    # проверяем как загружаются в файл товарные позиции и остаткки товара

    from Utils.ProductsUtils import ProductsUtils
    from UnitsTypes import UnitsTypes

    # logger.remove()

    products_utils = ProductsUtils()
    products = products_utils.load_products_from_file("ParserLeroyMerlinWithSeleniumPagination_save_file2.txt", ProductsElementWithQuantity)

    # render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)
    print(len(products))

    stop_list = [
        "латекс", "гипс", "замазка", "шпакрил", "керамзит", "мастика", "мел", "добавка", "жаростой",
        "шпатлевка", "шпатлёвк", "декоратив", "огнеупор", "наливной", "глино",
        "алебастр", "Шпаклевка", "газоблоков", "Шпаклёвка", "стекло", "Глина", "Бетонконтакт", "Финишпаста",
        "Краситель", "Плитонит", "Грунтовка", "Пропитка", "Ускоритель"
    ]

    cleaned_by_stop_list_products = products_utils.get_cleaned_products_by_stop_list(products, stop_list)

    print('Очистка по стоп словам')

    # render.render(cleaned_by_stop_list_products, DataStrFormat.WIDE)
    # print(len(cleaned_by_stop_list_products))

    print('Очистка по отсутвию единицы измерения (кг!, литр):')

    cleaned_by_units_type = products_utils.get_cleaned_products_by_units_types(cleaned_by_stop_list_products,
                                                                               [UnitsTypes.KG, UnitsTypes.LITR])

    # render.render(cleaned_by_units_type, DataStrFormat.WIDE)
    # print(len(cleaned_by_units_type))

    # print()

    el = products_utils.convert_price_to_price_for_unit(cleaned_by_units_type, [UnitsTypes.KG, UnitsTypes.LITR])

    print('Цена за единицу:')

    # render.render(el, DataStrFormat.WIDE)
    # print(len(el))

    parser = ParserLeroyMerlinWithSeleniumPagination("https://habarovsk.leroymerlin.ru/catalogue/suhie-smesi-i-gruntovki/?page=")
    parser.set_products(el)

    peq = parser.get_quantity_of_products()

    products_utils.save_products_to_file(peq, "quantity_ParserLeroyMerlinWithSeleniumPagination_save_file4.txt")

@timeit
def run5():
    # проверяем как загружаются из файла
    # проверяем как отправляются на zabbix-сервер товарные позиции и остаткки товара

    from Utils.ProductsUtils import ProductsUtils
    from Utils.ZabbixUtils import ZabbixUtils

    # logger.remove()

    products_utils = ProductsUtils()
    products = products_utils.load_products_from_file("quantity_ParserLeroyMerlinWithSeleniumPagination_save_file4.txt", ProductsElementWithQuantity)

    zabbix_config = {
        'ZABBIX_SERVER': "http://192.168.1.60",  # http://192.168.1.60   - не работает на ZabbixSender()
        'ZABBIX_USER': "Admin",
        'ZABBIX_PASSWORD': "zabbix",
        'ZABBIX_HOST': "STC.test",
        'ZABBIX_SENDER_SERVER': '192.168.1.60'  # работает на ZabbixSender() только без 'http://'
    }

    sender = ZabbixUtils(zabbix_config)
    sender.send_items_with_values(products, 'price')
    sender.send_items_with_values(products, 'quantity')

@timeit
def run6():
    # проверяем как загружаются из файла
    # проверяем как очищается список по стоп словам
    # проверяем как очищается по отсуствию единиц измерения меры в имени (кг, литры, шт)
    # проверяем как конвертируется цена в цену за единицу
    # проверяем как парсятся остаки товара
    # проверяем как загружаются в файл товарные позиции и остаткки товара
    # проверяем как отправляются на zabbix-сервер товарные позиции и остаткки товара

    from Utils.ProductsUtils import ProductsUtils
    from UnitsTypes import UnitsTypes
    from Utils.ZabbixUtils import ZabbixUtils

    # logger.remove()

    products_utils = ProductsUtils()

    parser = ParserLeroyMerlinWithSeleniumPagination("https://habarovsk.leroymerlin.ru/catalogue/suhie-smesi-i-gruntovki/?page=")
    products = parser.get_products_from_site()

    # render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)
    logger.info(f'{len(products)=}')

    stop_list = [
        "латекс", "гипс", "замазка", "шпакрил", "керамзит", "мастика", "мел", "добавка", "жаростой",
        "шпатлевка", "шпатлёвк", "декоратив", "огнеупор", "наливной", "глино",
        "алебастр", "Шпаклевка", "газоблоков", "Шпаклёвка", "стекло", "Глина", "Бетонконтакт", "Финишпаста",
        "Краситель", "Плитонит", "Грунтовка", "Пропитка", "Ускоритель"
    ]

    cleaned_by_stop_list_products = products_utils.get_cleaned_products_by_stop_list(products, stop_list)
    cleaned_by_units_type = products_utils.get_cleaned_products_by_units_types(cleaned_by_stop_list_products,
                                                                               [UnitsTypes.KG, UnitsTypes.LITR])
    el = products_utils.convert_price_to_price_for_unit(cleaned_by_units_type, [UnitsTypes.KG, UnitsTypes.LITR])


    parser.set_products(el)
    products = parser.get_quantity_of_products()

    products_utils.save_products_to_file(products, "quantity_ParserLeroyMerlinWithSeleniumPagination_save_file4.txt")

    # ###
    #
    # products = products_utils.load_products_from_file("quantity_ParserLeroyMerlinWithSeleniumPagination_save_file4.txt", ProductsElementWithQuantity)
    #
    # ####


    zabbix_config = {
        'ZABBIX_SERVER': "http://192.168.1.60",  # http://192.168.1.60   - не работает на ZabbixSender()
        'ZABBIX_USER': "Admin",
        'ZABBIX_PASSWORD': "zabbix",
        'ZABBIX_HOST': "LM2.test",
        'ZABBIX_SENDER_SERVER': '192.168.1.60'  # работает на ZabbixSender() только без 'http://'
    }

    sender = ZabbixUtils(zabbix_config)
    sender.send_items_with_values(products, 'price_for_kg')
    sender.send_items_with_values(products, 'quantity')


# @timeit
def get_products_from_site(url, units_types, stop_list, region_code:str='habarovsk'):

    parser = ParserLeroyMerlinWithSeleniumPagination(siteUrl=url, region_code=region_code)

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

    products_with_quantity = parser.get_quantity_of_products()


    return products_with_quantity


def send_products_to_zabbix(zabbix_config, products):
    sender = ZabbixUtils(zabbix_config)
    sender.send_items_with_values(products, 'price_for_kg')

    # TODO
    #  кривое решение по внедрению возможности отправки цен и количества в разные узлы

    zabbix_qunatity_config = zabbix_config
    zabbix_qunatity_config['ZABBIX_HOST'] = zabbix_config['ZABBIX_HOST-QUANTITY']

    sender2 = ZabbixUtils(zabbix_qunatity_config)
    sender2.send_items_with_values(products, 'quantity')


def run7():

    # СМЕСИ
    url='https://habarovsk.leroymerlin.ru/catalogue/suhie-smesi-i-gruntovki/?page='
    units_types = [UnitsTypes.KG, UnitsTypes.LITR]

    ZABBIX_SERVER_ADRESS = '192.168.1.60'

    zabbix_config = {
        'ZABBIX_SERVER': f"http://{ZABBIX_SERVER_ADRESS}",  # http://192.168.1.60   - не работает на ZabbixSender()
        'ZABBIX_USER': "Admin",
        'ZABBIX_PASSWORD': "zabbix",

        # 'ZABBIX_HOST': "LERUA-price-NEW3",
        'ZABBIX_HOST': "LM2.test",
        # 'ZABBIX_HOST-QUANTITY': "LERUA-quantity-NEW3",
        'ZABBIX_HOST-QUANTITY': "LM3.test",
        'ZABBIX_SENDER_SERVER': ZABBIX_SERVER_ADRESS  # работает на ZabbixSender() только без 'http://'
    }

    stop_list=[
        "латекс", "гипс", "замазка", "шпакрил", "керамзит", "мастика", "мел", "добавка", "жаростой",
        "шпатлевка", "шпатлёвк", "декоратив", "огнеупор", "наливной", "глино",
        "алебастр", "Шпаклевка", "газоблоков", "Шпаклёвка", "стекло", "Глина", "Бетонконтакт", "Финишпаста",
        "Краситель", "Плитонит", "Грунтовка", "Пропитка", "Ускоритель"
    ]

    logger.add(
        "out-lerua-class.log",
        backtrace=True,
        diagnose=True,
        level='INFO',
        rotation = "2 month",
        compression = "zip"
    )


    products = get_products_from_site(url, units_types, stop_list)
    send_products_to_zabbix(zabbix_config, products)

# import os
#
# def run8():
#     # ZABBIX_SERVER_ADDRESS = '192.168.1.60'
#     logger.info(f"{s.getenv('ZABBIX_SERVER_ADDRESS')=}")


@timeit
def main_working_version():
    logger.add(
        "out-lerua-class.log",
        backtrace=True,
        diagnose=True,
        level='INFO',
        rotation="2 month",
        compression="zip"
    )

    # try:
    #     logger.info(f'Start Run8 function...')
    #     run8()
    #     logger.info(f'End Run8 function!')
    # except Err as Err:
    #     logger.error(f'{Err}')


    ZABBIX_SERVER_ADDRESS = '192.168.1.60'

    zabbix_config = {
        'ZABBIX_SERVER': f"http://{ZABBIX_SERVER_ADDRESS}",  # http://192.168.1.60   - не работает на ZabbixSender()
        'ZABBIX_USER': "Admin",
        'ZABBIX_PASSWORD': "zabbix",

        'ZABBIX_HOST': "LERUA-price-NEW3",
        # 'ZABBIX_HOST': "LM2.test",
        'ZABBIX_HOST-QUANTITY': "LERUA-quantity-NEW3",
        # 'ZABBIX_HOST-QUANTITY': "LM3.test",
        'ZABBIX_SENDER_SERVER': ZABBIX_SERVER_ADDRESS  # работает на ZabbixSender() только без 'http://'
    }

    # СМЕСИ
    url='https://habarovsk.leroymerlin.ru/catalogue/suhie-smesi-i-gruntovki/?page='
    stop_list=[
        "латекс", "гипс", "замазка", "шпакрил", "керамзит", "мастика", "мел", "добавка", "жаростой",
        "шпатлевка", "шпатлёвк", "декоратив", "огнеупор", "наливной", "глино",
        "алебастр", "Шпаклевка", "газоблоков", "Шпаклёвка", "стекло", "Глина", "Бетонконтакт", "Финишпаста",
        "Краситель", "Плитонит", "Грунтовка", "Пропитка", "Ускоритель"
    ]

    # units_types=["кг"]
    units_types = [UnitsTypes.KG]

    products_01 = get_products_from_site(url, units_types, stop_list)
    # send_products_to_zabbix(zabbix_config, products_01)


    # ПЕСОК
    url='https://habarovsk.leroymerlin.ru/search/?q=%D0%BF%D0%B5%D1%81%D0%BE%D0%BA&page='
    stop_list=[
        "Краска", "Затирка", "Грунт", "Гидрогель", "Набор", "Ширма", "Интерактивный", "Штукатурка", "Морской",
        "Гидроизоляция", "лепки", "Смесь", "Ваза", "Герметик", "Покрытие"
    ]
    units_types=[UnitsTypes.KG]

    products_02 = get_products_from_site(url, units_types, stop_list)
    # send_products_to_zabbix(zabbix_config, products_02)

    # ИЗВЕСТЬ
    url='https://habarovsk.leroymerlin.ru/search/?q=%D0%B8%D0%B7%D0%B2%D0%B5%D1%81%D1%82%D1%8C&page='
    stop_list=["гуашь", "краска", "средство", "краскопульт", "аэрограф", "пневма"]
    units_types=[UnitsTypes.KG, UnitsTypes.LITR]

    products_03 = get_products_from_site(url, units_types, stop_list)
    # send_products_to_zabbix(zabbix_config, products_03)

    # ПУШОНКА
    url='https://habarovsk.leroymerlin.ru/search/?q=%D0%BF%D1%83%D1%88%D0%BE%D0%BD%D0%BA%D0%B0&page='
    stop_list=[]
    units_types=[UnitsTypes.KG, UnitsTypes.LITR]

    products_04 = get_products_from_site(url, units_types, stop_list)
    # send_products_to_zabbix(zabbix_config, products_04)


    # МУКА
    url='https://habarovsk.leroymerlin.ru/search/?q=%D0%BC%D1%83%D0%BA%D0%B0&page='
    stop_list=["семена", "гидрогель", "постер"]
    units_types=[UnitsTypes.KG, UnitsTypes.LITR]

    products_05 = get_products_from_site(url, units_types, stop_list)
    # send_products_to_zabbix(zabbix_config, products_05)


    # КЛЕЙ ДЛЯ ОБОЕВ
    url='https://habarovsk.leroymerlin.ru/search/?q=%D0%BA%D0%BB%D0%B5%D0%B9+%D0%B4%D0%BB%D1%8F+%D0%BE%D0%B1%D0%BE%D0%B5%D0%B2&suggest=true&page='
    stop_list=['поклейкой']
    units_types=[UnitsTypes.KG, UnitsTypes.LITR]

    products_06 = get_products_from_site(url, units_types, stop_list)
    # send_products_to_zabbix(zabbix_config, products_06)

    # БОКАШИ - Хабаровск
    url='https://habarovsk.leroymerlin.ru/search/?q=%D0%B1%D0%BE%D0%BA%D0%B0%D1%88%D0%B8&page='
    stop_list=[]
    units_types=[UnitsTypes.KG, UnitsTypes.LITR]


    products_07 = get_products_from_site(url, units_types, stop_list)
    # send_products_to_zabbix(zabbix_config, products_07)

    # # БОКАШИ - Новосибирск
    # url='https://novosibirsk.leroymerlin.ru/search/?q=%D0%B1%D0%BE%D0%BA%D0%B0%D1%88%D0%B8&page='
    # stop_list=[]
    # region_code='novosibirsk'
    # units_types=[UnitsTypes.KG, UnitsTypes.LITR]
    #
    # products_08 = get_products_from_site(url, units_types, stop_list, region_code=region_code)
    # # send_products_to_zabbix(zabbix_config, products_08)

    # # БОКАШИ - Москва
    # url='https://leroymerlin.ru/search/?q=%D0%B1%D0%BE%D0%BA%D0%B0%D1%88%D0%B8&page='
    # stop_list=[]
    # region_code='moscow'
    # units_types=[UnitsTypes.KG, UnitsTypes.LITR]
    #
    # products_09 = get_products_from_site(url, units_types, stop_list, region_code=region_code)
    # # send_products_to_zabbix(zabbix_config, products_09)

    # Биогумус - Хабаровск
    url='https://habarovsk.leroymerlin.ru/search/?q=%D0%B1%D0%B8%D0%BE%D0%B3%D1%83%D0%BC%D1%83%D1%81&page='
    stop_list=[]
    units_types = [UnitsTypes.KG, UnitsTypes.LITR]

    products_10 = get_products_from_site(url, units_types, stop_list, region_code='habarovsk')
    # send_products_to_zabbix(zabbix_config, products_10)

    all_products = products_01
    all_products += products_02
    all_products += products_03
    all_products += products_04
    all_products += products_05
    all_products += products_06
    all_products += products_07

    # all_products += products_08
    # all_products += products_09

    all_products += products_10

    send_products_to_zabbix(zabbix_config, all_products)

if __name__ == '__main__':
    main_working_version()

