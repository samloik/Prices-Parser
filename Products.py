from ProductsElement import ProductsElement
# from loguru import logger
# from UnitsTypes import UnitsTypes

#
# class TeamIterator:
#    ''' Iterator class '''
#    def __init__(self, team):
#        # Team object reference
#        self._team = team
#        # member variable to keep track of current index
#        self._index = 0
#    def __next__(self):
#        ''''Returns the next value from team object's lists '''
#        if self._index < (len(self._team)):
#            return
#            if self._index < len(self._team._juniorMembers): # Check if junior members are fully iterated or not
#                result = (self._team._juniorMembers[self._index] , 'junior')
#            else:
#                result = (self._team._seniorMembers[self._index - len(self._team._juniorMembers)]   , 'senior')
#            self._index +=1
#            return result
#        # End of Iteration
#        raise StopIteration

class Products:
    _products:dict

    def __init__(self):
        self._products = {}

    def __len__(self):
        return len(self._products)

    def get_products(self):
        return self._products


    def keys(self):
        keys = self._products.keys()
        return keys

    def __getitem__(self, item):
        return self._products[item]

    def __setitem__(self, key, value):
        self._products[key] = value


    # def __next__(self):
    #     return self.products.__next__()

    def append(self, object: ProductsElement):
        # допущение имена не могут повторяться
        self._products[object.get_name()] = object

    def remove(self, object: ProductsElement):
        del self._products[object.get_name()]

    def remove_by_name(self, name: str):
        # print(name)
        del self._products[name]

    def clear_products(self):
        for product_key in self._products.keys():
            self.remove_element_by_name(product_key)

    def get_element_by_name(self, name:str):
        return self._products[name]

    def is_products_element_contained_in_products(self, other: ProductsElement):
        if not other is None and isinstance(other, ProductsElement):
            if other.get_name() in self._products.keys():
                return True
            else:
                return False

    def get_products_copy(self):
        new_products = Products()
        for product_key in self._products.keys():
            new_products.append(self._products[product_key].get_copy())
        return new_products

    # одинаковый код функций __add__ и __iadd__
    def __my_add_element(self, other, new_products):
        if not other is None and isinstance(other, (Products, ProductsElement)):
            # new_products = self.getProductsCopy()
            if isinstance(other, Products):
                for product_key in other._products.keys():
                    new_products.append(other._products[product_key].get_copy())
            else:
                new_products.append(other.get_copy())
            return new_products

    def __add__(self, other):
        # допущение имени добавляемого объекста еще нет в списке
        return self.__my_add_element(other, new_products=self.get_products_copy())

    def __iadd__(self, other):
        # допущение имени добавляемого объекста еще нет в списке
        return self.__my_add_element(other, new_products=self)

    # одинаковый код функций __sub__ и __isub__
    def __my_sub_element(self, other, new_products):
        if not other is None and isinstance(other, (Products, ProductsElement)):
            # new_products = self.getProductsCopy()
            if isinstance(other, Products):
                for product_key in other._products.keys():
                    new_products.remove_element_by_name(product_key)
            else:
                new_products.remove_element_by_name(other.get_name())
            return new_products

    def __sub__(self, other):
        return self.__my_sub_element(other, new_products=self.get_products_copy())

    def __isub__(self, other):
        return self.__my_sub_element(other, new_products=self)

    #
    # def getCleanedProdutcsByStopList(self, stop_list: list):
    #     cleaned_products = self.getProductsCopy()
    #
    #     # TODO проверить алгоритм удаления
    #     # выяснить причину появления повторного удаления
    #     # причина ошибки повторного удаления в том, что элемент уже был удален ранее, по дугому стоп слову
    #
    #     for stop_text in stop_list:
    #         for name in self.products.keys():
    #             if stop_text.lower() in name.lower():
    #                 logger.info(f'удаление {name} по stop_text: [{stop_text}]')
    #                 try:
    #                     cleaned_products.removeByName(name)
    #                 except:
    #                     logger.info(f'[*] Попытка повторного удаления {name} по stop_text: [{stop_text}]')
    #
    #     return cleaned_products
    #
    # def getCleanedProductsByWeightInName(self):
    #     pass


def test():
    from ParserProductComparison.ProductsElementAvto import ProductsElementAvto
    from ProductsElement import ProductsElement
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    products = Products()
    products.append(ProductsElement("Редиска", 250, "https://rediska.com"))
    products.append(ProductsElementAvto("Бруклин", 33.805, "https://kornishon.en", "HITACHI", "302782", "AA700-34", "Павловского"))

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    print()

    pre = ProductsElement("Груша", 32.805, "https://grusha.ru")
    prea = ProductsElementAvto("Хрюша", 33.805, "https://kornishon.en","TOTAL", "650432", "NN701-85", "Чапаего")
    # print(prea)
    print()

    products += pre

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    print('test += __iadd__')

    products += prea

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)


    print('test -= __isub__')

    products -= prea

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    print('test + __add__')

    products = products + prea

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    print('test - __add__')

    products = products - prea

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

def test2():
    from ParserProductComparison.ProductsElementAvto import ProductsElementAvto
    from ProductsElement import ProductsElement
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    products = Products()
    products.append(ProductsElement("Редиска", 250, "https://rediska.com"))
    products.append(ProductsElementAvto("Бруклин", 33.805, "https://kornishon.en", "HITACHI", "302782", "AA700-34", "Павловского"))

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    print()

    pre = ProductsElement("Груша", 32.805, "https://grusha.ru")
    prea = ProductsElementAvto("Хрюша", 33.805, "https://kornishon.en","TOTAL", "650432", "NN701-85", "Чапаего")
    # print(prea)
    print()

    products += pre

    for i in products.keys():
        print(str(i))



if __name__ == '__main__':
    test2()

