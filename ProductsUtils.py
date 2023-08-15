from Products import Products
from UnitsTypes import UnitsTypes
from ProductsElement import ProductsElement
from loguru import logger
from ElementName import ElementName

class ProductsUtils:
    pwd = 'C:\PycharmProjects\Prices-Parser\Save\\'


    def saveProductsToFile(self, products: Products, filename:str):
        text = ""
        for key in products.products.keys():
            text += products.products[key].getStrFormatForWriteToFile() + '\n'
        with open(self.pwd + filename, 'w', encoding='utf-8') as file:
            file.write(text)
        logger.info(f'[SAVE] Сохраняем результат в файл [{len(products)} шт]: {filename}')

    # TODO - переделать логику
    # предполагается запускать метод класс наследника ProductElement
    # вопрос как, его сюда передать пока не решен
    # решение отложено до момента реализации такого класса, для лучшего понимания взаимодействия

    def loadProductsFromFile(self, filename:str): # (product_type:ProductsElement, filename:str):
        with open(self.pwd + filename, 'r', encoding='utf-8') as file:
            text = file.read()
        str_format_from_file = text.split('\n')[:-1]
        products = Products()
        for product_element_in_str_format in str_format_from_file:
            # products.append(product_type.getProductElementCopyFromStrFormat(product_element))
            products.append(ProductsElement.getCopyFromStrFormat(product_element_in_str_format))
        logger.info(f'[LOAD] Загружаем элементы [{len(products)} шт] из файла: {filename}')
        return products

    @staticmethod
    def getCleanedProductsByStopList(products: Products, stopList: list):
        cleaned_products = products.getProductsCopy()

        # TODO проверен алгоритм удаления
        # выяснить причину появления повторного удаления
        # причина ошибки повторного удаления в том, что элемент уже был удален ранее, по дугому стоп слову
        for stop_text in stopList:
            for name in products.products.keys():
                if stop_text.lower() in name.lower():
                    logger.info(f'удаление {name} по stop_text: [{stop_text}]')
                    try:
                        cleaned_products.removeByName(name)
                    except:
                        logger.info(f'[*] Попытка повторного удаления! {name} по stop_text: [{stop_text}]')

        return cleaned_products


    @staticmethod
    def getCleanedProductsByUnitsTypes(products: Products, units_types: list):
        cleaned_products = products.getProductsCopy()

        for name in products.products.keys():
            element_name = ElementName(name, units_types)
            value_from_name = element_name.getValueOfUnitsInName()

            if  value_from_name == "":
                # print(f'[{name:>100}] удалено {valueFromName=} {units_types=}')
                cleaned_products.removeByName(name)
            # else:
                # print(f'[{name:>100}] сохранено {valueFromName=} {units_types=}')

        return cleaned_products


    def converPriceToPriceForUnit(self, products: Products, units_types: list):
        # допущение: пользователь будет только один раз конвертировать, иначе неверная информация

        converted_produtcs = products.getProductsCopy()

        for name in products.products.keys():
            element_name = ElementName(name, units_types)
            value_from_name = element_name.getValueOfUnitsInName()

            price = products.getElementByName(name).price / float(value_from_name)
            converted_produtcs.getElementByName(name).price = price

        return converted_produtcs




