from Products import Products
from ProductsElements.ProductsElement import ProductsElement
from loguru import logger
from ProductsElements.ElementName import ElementName

class ProductsUtils:
    pwd = 'C:\PycharmProjects\Prices-Parser\Save\\'


    def save_products_to_file(self, products: Products, filename:str):
        text = ""
        # products = products_to_save.get_products()
        # for key in products.products.keys():
        # for key in products.keys():
        for key in products.keys():
            text += products[key].get_str_format_for_write_to_file() + '\n'
        with open(self.pwd + filename, 'w', encoding='utf-8') as file:
            file.write(text)
        logger.info(f'[SAVE] Сохраняем результат в файл [{len(products)} шт]: {filename}')

    # TODO - переделать логику
    # предполагается запускать метод класс наследника ProductElement
    # вопрос как, его сюда передать пока не решен
    # решение отложено до момента реализации такого класса, для лучшего понимания взаимодействия

    def load_products_from_file(self, filename:str, productsElement=ProductsElement):
        with open(self.pwd + filename, 'r', encoding='utf-8') as file:
            text = file.read()
        str_format_from_file = text.split('\n')[:-1]
        products = Products()
        for product_element_in_str_format in str_format_from_file:
            # products.append(product_type.getProductElementCopyFromStrFormat(product_element))
            products.append(productsElement.get_copy_from_str_format(product_element_in_str_format))
        logger.info(f'[LOAD] Загружаем элементы [{len(products)} шт] из файла: {filename}')
        return products

    @staticmethod
    def get_cleaned_products_by_stop_list(products: Products, stopList: list):
        logger.info(f"Очищаем список элементов по стоп листу...")
        cleaned_products = products.get_products_copy()

        # TODO проверен алгоритм удаления
        # выяснить причину появления повторного удаления
        # причина ошибки повторного удаления в том, что элемент уже был удален ранее, по дугому стоп слову
        for stop_text in stopList:
            for name in products.keys():
                if stop_text.lower() in name.lower():
                    logger.info(f'удаление {name} по stop_text: [{stop_text}]')
                    try:
                        cleaned_products.remove_by_name(name)
                    except:
                        logger.info(f'[*] Попытка повторного удаления! {name} по stop_text: [{stop_text}]')

        return cleaned_products


    @staticmethod
    def get_cleaned_products_by_units_types(products: Products, units_types: list):
        logger.info(f"Очищаем список элементов по единицам измерения в имени {units_types}...")
        cleaned_products = products.get_products_copy()

        for name in products.keys():
            element_name = ElementName(name, units_types)
            value_from_name = element_name.get_value_of_units_in_name()

            if  value_from_name == "":
                # print(f'[{name:>100}] удалено {valueFromName=} {units_types=}')
                cleaned_products.remove_by_name(name)
            # else:
                # print(f'[{name:>100}] сохранено {valueFromName=} {units_types=}')

        return cleaned_products


    def convert_price_to_price_for_unit(self, products: Products, units_types: list):
        # допущение: пользователь будет только один раз конвертировать, иначе неверная информация

        converted_produtcs = products.get_products_copy()

        for name in products.keys():
            element_name = ElementName(name, units_types)
            value_from_name = element_name.get_value_of_units_in_name()

            price_for_unit = products.get_element_by_name(name).get_price() / float(value_from_name)
            converted_produtcs.get_element_by_name(name).set_price(price_for_unit)

        return converted_produtcs


def test():
    # проверяем как парсятся товарные позиции с сайта
    # проверяем как очищается список по стоп словам
    # проверяем как очищается по отсуствию единиц измерения меры в имени (кг, литры, шт)


    from DataRenderer import DataRenderer
    from UnitsTypes import UnitsTypes
    from Parser.ParserStockCentrWithSession import ParserStockCentrWithSession

    pu = ProductsUtils()
    render = DataRenderer()

    # products = pu.load_products_from_file("stock_centr_save_file.txt")
    parser = ParserStockCentrWithSession("https://stok-centr.com/magazin/folder/sukhiye-smesi/p/")
    products = parser.get_products_from_site()

    # render.render(products, DataStrFormat.WIDE)
    print(f'Список неочищен от стоп слов: {len(products)}')

    stop_list = [
        "латекс", "гипс", "замазка", "шпакрил", "керамзит", "мастика", "мел", "добавка", "жаростой",
        "шпатлевка", "шпатлёвк", "декоратив", "огнеупор", "наливной", "глино"
        # "клей"
    ]

    cleaned_products = pu.get_cleaned_products_by_stop_list(products, stop_list)

    # render.render(cleaned_products, DataStrFormat.WIDE)
    print(f'Список очищен от стоп слов: {len(cleaned_products)}')


    cleaned_by_units_type_kg_litr_products = pu.get_cleaned_products_by_units_types(products, [UnitsTypes.KG,
                                                                                               UnitsTypes.LITR])

    print(f'Список отобран по наличию единиц (кг,литр): {len(cleaned_by_units_type_kg_litr_products)}')

    products.append(ProductsElement("пакет фасовочный (20шт) ", 351, "https://my_url.com"))
    cleaned_by_units_type_shtuk_products = pu.get_cleaned_products_by_units_types(products,
                                                                                    [UnitsTypes.SHTUK])
    # render.render(cleaned_products, DataStrFormat.WIDE)
    print(f'Список отобран по наличию единиц (шт): {len(cleaned_by_units_type_shtuk_products)}')



if __name__ == '__main__':
    test()
