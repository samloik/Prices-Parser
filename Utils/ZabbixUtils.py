from ProductsElements.Products import Products
from pyzabbix import ZabbixAPI, ZabbixMetric, ZabbixSender, ZabbixAPIException
# from config import *
from ProductsElements.ElementName import ElementName
from loguru import logger
from time import sleep

class ZabbixUtils:

    # пример формата zabbix_config:
    #
    # zabbix_config = {
    #     'ZABBIX_SERVER': "http://192.168.1.60",  # http://192.168.1.60   - не работает на ZabbixSender()
    #     'ZABBIX_USER': "Admin",
    #     'ZABBIX_PASSWORD': "zabbix",
    #     'ZABBIX_HOST': "STC.test",
    #     'ZABBIX_SENDER_SERVER': '192.168.1.60'  # работает на ZabbixSender() только без 'http://'
    # }

    def __init__(self, config:dict):
        self.config = config
        self.sender_server = config['ZABBIX_SENDER_SERVER']
        self.host_name = config['ZABBIX_HOST']
        # self.products = None
        # self.value = None
        self.zapi = self.connect()

    def __del__(self):
        self.zapi.user.logout()


    def connect(self):
        try:
            zapi = ZabbixAPI(
                url=self.config['ZABBIX_SERVER'],
                user=self.config['ZABBIX_USER'],
                password=self.config['ZABBIX_PASSWORD']
            )
        except Exception as e:
            logger.error(f'ZabbixAPI: Ошибка аутентификации: {e}')
            # TODO exit(1)
            exit(1)
        return zapi

    def create_host(self):
        # Host create
        logger.info(f"Пытаемся создать хост [{self.host_name}]")
        host_name = self.host_name
        result_host = None
        try:
            result_host = self.zapi.do_request(method="host.create", params={
                "host": host_name,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": "127.0.0.1",
                        "dns": "",
                        "port": "10050"
                    }
                ],
                "groups": [
                    {
                        "groupid": "19"
                    }
                ],
                # "templates": [     # "templates": Linux by Zabbix agent:
                #     {
                #         "templateid": "10001"
                #     }
                # ],
            }
                                          )
        except Exception as err:
            logger.error(f'Ошибка при создании хоста [{host_name}]: {err}')
        if not result_host and not result_host['result']:
            logger.error(f'Не удалось создать хост [{host_name}]')
            exit(1)
        else:
            logger.info(f'Создан хост [{host_name}]')
        return result_host

    def find_host(self):
        host_name = self.host_name
        result_host = None
        try:
            result_host = self.zapi.do_request('host.get', {'filter': {'name': host_name}})
            if not result_host['result']:
                logger.info(f'Хост не найден: [{host_name}]')
            else:
                logger.info(f"Найден хост [{host_name}] {result_host['result']}")
        except Exception as e:
            logger.error(f'Ошибка при поиске хоста [{host_name}]: {e}')

        return result_host


    def find_or_create_host(self):
        # проверяем наличие хоста, если нет, то создаем такой хост
        result_host = self.find_host()
        if not result_host or not result_host['result']:
            result_host = self.create_host()
        return result_host


    def find_hosts(self, groupids=19):
        zapi, host_name = self.zapi, self.host_name
        # Получаем список хостов в группе с id 19 - Applications")
        logger.info(f"Получаем список хостов в группе с id 19 - Applications")
        hosts = zapi.host.get(groupids=groupids, output=['hostid', 'name'])
        # for host in hosts:
        #     print(host['hostid'], host['name'])
        hosts = zapi.host.get(filter={"host": host_name}, selectInterfaces=["interfaceid"])
        return hosts


    def find_host_id(self, groupids=19):
        hosts = self.find_hosts(groupids)
        if hosts:
            # TODO переделать hosts[0]["hostid"]: реализовать поиск по имени
            host_id = hosts[0]["hostid"]  # первый хост из списка - если он один с таким именем
            logger.info(f"Найден хост: [{host_id=}]")
            return host_id, hosts
        else:
            logger.error(f"Хост [{self.host_name}] не найден")
            return None, hosts


    def get_items_names(self):
        zapi, host_id = self.zapi, self.host_id
        # Получаем список item с хоста c host_name

        # hosts = zabbix_find_hosts(zapi, host_name, groupids)

        names_of_items = []
        if host_id:
            # host_id = hosts[0]["hostid"]    # первый хост из списка - если он один с таким именем
            # TODO проверить на работоспособность - возможно таких hosts больше чем 1
            # logger.info(f"Найден host: host_ id={host_id}")

            # Пример №5 Печатаем список item ----------------------------------------------------------------
            # Получаем список item с хоста c hostids

            try:
                # items = zapi.item.get(hostids=host_id, output=['itemid', 'name', 'key_'])
                items = zapi.item.get(hostids=host_id, output=['name'])
                for item in items:
                    names_of_items.append(item['name'])
                    # print(item['itemid'], item['name'], item['key_'])
                # print(f' len(items) = {len(items)}')
                logger.info(f"Получен список items в количестве [{len(names_of_items)} шт] с хоста hostids={host_id}")
                # TODO Ошибка №11 от 2023/03/11
                #  временный код для поиска ошибки

                fibr = 'Фибра для бетонов и растворов Fibr'
                for cur_name in names_of_items:
                    if cur_name.startswith(fibr):
                        logger.info(f'{cur_name=}')

                logger.info(f'Конец теста')
                # exit(1)
                # TODO конец временного кода
                return names_of_items
            except ZabbixAPIException as e:
                logger.error(f'[ОШИБКА]: {e}')

        logger.error(f"[ОШИБКА]: нет [{host_id=}]")
        return names_of_items


    @staticmethod
    def  get_normalized_key(key, value):
        return key + '.' + value

    def create_item(self, name, key):
        zapi, hosts, host_id = self.zapi, self.hosts, self.host_id

        # пример создания zabbix item на созданном zapi->ZABBIX_SERVER, HOST_NAME

        if host_id:
            # type_list = [0, 2, 3, 5, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
            # type_list_names = ['Zabbix_agent - 0', 'Zabbix traper - 2', 'Simple chek -3', 'Zabbix internal - 5',
            #                   'Zabbix agent(active) - 7', 'Extarnal check - 10', 'Database Monitor - 11',
            #                   12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
            # value_type_list_names = ['Numeric(float) - 0', 'Character - 1', 'Log - 2', 'Numeric(unsigned) - 3', 'Text - 4']

            try:
                item = zapi.item.create(
                    hostid=host_id,
                    name=name,
                    key_=key,
                    type=2,
                    value_type=0,
                    # TODO переписать - затычку hosts[0]["interfaces"][0]["interfaceid"]
                    interfaceid=hosts[0]["interfaces"][0]["interfaceid"],
                    delay=30,  # ,было delay=30, нужно 0
                    history='3650d',
                    trends='3650d'  # срок хранения item 3650 дней
                )
                # TODO переписать - затычку item['itemids'][0]
                logger.info(f"Добавлен item[{name}] с itemid={item['itemids'][0]} на host: {host_id}")
            except ZabbixAPIException as e:
                logger.error(f'[ОШИБКА]: {e}')

        return host_id

    def set_items(self, products:Products, value):
        zabbix_sender_server, host_name = self.sender_server, self.host_name
        # устанавливаем значения items списком

        try:
            # packet = [
            #     ZabbixMetric(
            #         host=host_name,
            #         key=get_normalized_key(values_dict[key][1], value)
            #         # считаем значение - цена за килограмм
            #         value=float(f'{float(values_dict[key][0][value]):.2f}'))
            # for key in values_dict.keys()
            # ]

            packet = []

            for key in products.keys():
                name = ElementName(key)
                translit_name = name.translit_name()

                # logger.warning( f'{(products.get_element_by_name(key)).get_monitoring_value()=}' )

                packet.append(
                    ZabbixMetric(
                        host=host_name,
                        key=self.get_normalized_key(translit_name, value),
                        # считаем значение - цена за килограмм
                        # getattr(zs, 'host_name')
                        # value=float(f'{float(getattr(products.get_element_by_name(key), value)):.2f}'))
                        # value=float(f'{float((products.get_element_by_name(key)).get_monitoring_value()[value]):.2f}'))
                        value=(products.get_element_by_name(key)).get_monitoring_value()[value]
                    )
                )

            sender = ZabbixSender(zabbix_server=zabbix_sender_server)
            result = sender.send(packet)
            logger.info(f'пакет items размером [{len(packet)} шт] ' +
                        f'отправлен на сервер = [{zabbix_sender_server}]')
            return result

        except ZabbixAPIException as e:
            logger.error(f'[ОШИБКА отправки]: {e}')
            return None


    def send_items_with_values(self, products:Products, value="price_for_kg"):
        zabbix_sender_server, host_name, zapi = self.sender_server, self.host_name, self.zapi

        # проверяем наличие хоста, если нет, то создаем такой хост
        self.find_or_create_host()

        self.host_id, self.hosts = self.find_host_id(groupids=19)

        # -----
        # Получаем список item с хоста c hostids
        items_names = self.get_items_names()

        # список имен items к созданию
        names_of_items_to_add = []

        # если список с сайта содержит новые items, то добавить такой item в names_of_items_to_add
        # TODO ошибка №11 от 2024/03/11
        #   Появляется элемент к добавлению, который уже существует.
        #   'Fibra_dlya_betonov_i_rastvorov_Fibra__150_g'
        #   Не верно работает код. Либо был сбой.

        for name in products.keys():
            if self.get_normalized_key(name, value) not in items_names:
                # TODO Ошибка №11 от 2023/03/11
                #  временный код для поиска ошибки

                fibr = 'Фибра для бетонов и растворов Fibr'

                logger.warning('names_of_items_to_add.append(name): [{name=}] [{value=}] [{self.get_normalized_key(name, value)=}]')
                logger.warning(f'[{len(products.keys())=}] [{len(items_names)}]')

                # TODO конец временного кода

                names_of_items_to_add.append(name)

        logger.info(f'Список новых items в количестве [{len(names_of_items_to_add)} шт] готовы к созданию в zabbix')

        # создаем items в zabbix соотвествующие translit именам
        for key in names_of_items_to_add:
            name = ElementName(key)
            translit_name = name.translit_name()

            self.create_item(
                name=self.get_normalized_key(key, value),
                key=self.get_normalized_key(translit_name, value)
            )
            logger.info(f'Item [{key=}] успешно создан [{name=} {value=}]')

        if names_of_items_to_add:
            # необходима задержка после создания, иначе данные не запишутся
            sec = 60
            logger.info(f'ждем [{sec}] сек, чтобы успешно отправить данные')
            sleep(sec)

        # устанавливаем значения items списком
        self.set_items(products, value)

        # zapi.user.logout() - перемещено в __del__()


    # def sendItemsQuantity(self, products:Products, value="quantity"):
    #     # отправляем данные в zabbix - "quantity"
    #     self.sendItems(products, value)


def test():
    zs = ZabbixSender("Hi", "Hello")

    print(zs.host_name)
    setattr(zs, 'host_name', 'Right')
    print(getattr(zs, 'host_name'))

def test2():
    # проверяем как загружаются из файла
    # проверяем как извлекаются единицы измерения меры из имени (кг, литры, шт)
    # проверяем как отправляются на zabbix-сервер товарные позиции и остаткки товара

    from DataRenderer import DataRenderer
    from ProductsUtils import ProductsUtils
    from ProductsElements.ElementName import ElementName
    from UnitsTypes import UnitsTypes

    # logger.remove()

    logger.add("ZabbixUtils.log", level="INFO", rotation="100 MB")

    products_utils = ProductsUtils()
    products = products_utils.load_products_from_file("cleaned_stock_centr_save_file.txt")
    # products = products_utils.loadProductsFromFile("stock_centr_save_file.txt")

    render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)
    print(len(products))

    for name in products.keys():
        element_name = ElementName(name, [UnitsTypes.KG, UnitsTypes.LITR])

        values_from_name = element_name.get_value_of_units_in_name()
        if  values_from_name != "":
            # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
            print(f'[+] {name:>100} | {values_from_name:<10} {element_name.get_units_types()}')
        else:
            print(f'[-] {name:>100} | Null       {elementName.get_units_types()}')

    zabbix_config = {
        'ZABBIX_SERVER': "http://192.168.1.60",  # http://192.168.1.60   - не работает на ZabbixSender()
        'ZABBIX_USER': "Admin",
        'ZABBIX_PASSWORD': "zabbix",
        'ZABBIX_HOST': "STC.test",
        'ZABBIX_SENDER_SERVER': '192.168.1.60'  # работает на ZabbixSender() только без 'http://'
    }

    sender = ZabbixUtils(zabbix_config)

    sender.send_items_with_values(products)


if __name__ == '__main__':
    test2()