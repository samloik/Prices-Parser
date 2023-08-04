from Products import Products
from UnitsTypes import UnitsTypes

class ProductsUtils:

    def cleanProductsByStopList(self, products: Products, stopList: list):
        cleanedProducts = products.getProductsCopy()

        for stop_text in stopList:
            for name in cleanedProducts.products.keys():
                if stop_text.lower() in name.lower():
                    logger.info(f'удаление {name} по stop_text: [{stop_text}]')
                    try:
                        cleanedProducts.removeByName(name)
                    except:
                        logger.info(f'[!] Попытка повторного удаления! {name} по stop_text: [{stop_text}]')

        return cleanedProducts


    # def getProductsWithWeight(self, products: Products, unitsTypes: list):
    #     result = ""
    #
    #     if not units_types or len(units_types) == 0 or UnitsTypes.KG in units_types:
    #         logger.info(f'f[ОТЛАДКА] "кг" извлекаем [{units_types=}] [{name}]')
    #         # если unit_types=None, или список пуст, или есть UnitsTypes.KG в списке, то:
    #         result = get_kg_from_name_no_valid(name)
    #
    #         # добавляем проверку на граммы
    #         if len(result) == 0:
    #             logger.info(f'f[ОТЛАДКА] "граммы" извлекаем [{units_types=}] [{name}]')
    #             result = get_gramm_from_name_no_valid(name)
    #
    #     if units_types and UnitsTypes.LITR in units_types:
    #         # если unit_types не None и есть UnitsTypes.LITR в списке, то:
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

