from Products import Products
from UnitsTypes import UnitsTypes
from ProductsElement import ProductsElement
from loguru import logger

class ProductsUtils:

    @staticmethod
    def saveProductsToFile(products: Products, filename:str):
        text = ""
        for key in products.products.keys():
            text += products.products[key].getProductElementStrFormatForWriteToFile() + '\n'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        logger.info(f'[SAVE] Сохраняем результат в файл [{len(products)} шт]: {filename}')

    # TODO - переделать логику
    # предполагается запускать метод класс наследника ProductElement
    # вопрос как, его сюда передать пока не решен
    # решение отложено до момента реализации такого класса, для лучшего понимания взаимодействия
    @staticmethod
    def loadProductsFromFile(filename:str): # (product_type:ProductsElement, filename:str):
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        str_format_from_file = text.split('\n')[:-1]
        products = Products()
        for product_element in str_format_from_file:
            # products.append(product_type.getProductElementCopyFromStrFormat(product_element))
            products.append(ProductsElement.getProductElementCopyFromStrFormat(product_element))
        logger.info(f'[LOAD] Загружаем элементы [{len(products)} шт] из файла: {filename}')
        return products

    @staticmethod
    def getCleanedProductsByStopList(products: Products, stopList: list):
        cleanedProducts = products.getProductsCopy()

        # TODO проверен алгоритм удаления
        # выяснить причину появления повторного удаления
        # причина ошибки повторного удаления в том, что элемент уже был удален ранее, по дугому стоп слову

        for stop_text in stopList:
            for name in products.products.keys():
                if stop_text.lower() in name.lower():
                    logger.info(f'удаление {name} по stop_text: [{stop_text}]')
                    try:
                        cleanedProducts.removeByName(name)
                    except:
                        logger.info(f'[*] Попытка повторного удаления! {name} по stop_text: [{stop_text}]')

        return cleanedProducts

        # TODO остановился здесь

        def getCleanedProductsByUnitsTypes(self, products: Products, units_types: list):
            pass
            # cleaned_products = products.getProductsCopy()
            #
            # for name in products.products.keys():
            #
            #     # units_type в нижнем регистре !!!
            #
            #     result = ''
            #
            #     if not units_types or len(units_types) == 0 or UnitsTypes.KG in units_types:
            #         logger.info(f'f[ОТЛАДКА] "кг" извлекаем [{units_types=}] [{name}]')
            #         # если unit_types=None, или список пуст, или есть "кг" в списке, то:
            #         result = get_kg_from_name_no_valid(name)
            #
            #         # добавляем проверку на г
            #         if len(result) == 0:
            #             logger.info(f'f[ОТЛАДКА] "граммы" извлекаем [{units_types=}] [{name}]')
            #             result = get_gramm_from_name_no_valid(name)
            #
            #     if units_types and UnitsTypes.LITR in units_types:
            #         # если unit_types не None и есть "литр" в списке, то:
            #         # добавляем проверку на литр
            #         logger.info(f'f[ОТЛАДКА] "литр" извлекаем [{units_types=}] [{name}]')
            #         if len(result) == 0:
            #             result = get_litr_from_name_no_valid(name)
            #
            #     if len(result) > 0:
            #
            #         result = validate_result_value(result)
            #         result = result.replace(',', '.', 1)
            #         try:
            #             number = float(result)
            #             result = str(number)
            #         except Exception as Error:
            #             logger.error(f'[-] Не удалось извлечь число из [{name=}] {Error=}')
            #             result = ''
            #     return result

