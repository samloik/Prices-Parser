from ProductsElement import ProductsElement

class Products:

    def __init__(self):
        self.products = {}

    def append(self, object: ProductsElement):
        # допущение имена не могут повторяться
        self.products[object.name] = object

    def remove(self, object: ProductsElement):
        del self.products[object.name]

    def removeByName(self, name: str):
        del self.products[name]


    def clearProducts(self):
        for productKey in self.products.keys():
            self.remove(self.getProductsElementByName(productKey))


    def getProductsElementByName(self, name:str):
        return self.products[name]


    def isProductsElementContainedInProducts(self, other: ProductsElement):
        if not other is None and isinstance(other, ProductsElement):
            if other.name in self.products.keys():
                return True
            else:
                return False


    def getProductsCopy(self):
        new_products = Products()
        for productKey in self.products.keys():
            new_products.append(self.products[productKey].getProductsElementCopy())
        return new_products


    # одинаковый код функций __add__ и __iadd__
    def __my_add_element(self, other, new_products):
        if not other is None and isinstance(other, (Products, ProductsElement)):
            # new_products = self.getProductsCopy()
            if isinstance(other, Products):
                for productKey in other.products.keys():
                    new_products.append(other.products[productKey].getProductsElementCopy())
            else:
                new_products.append(other.getProductsElementCopy())
            return new_products


    def __add__(self, other):
        # допущение имени добавляемого объекста еще нет в списке
        return self.__my_add_element(other, new_products=self.getProductsCopy())


    def __iadd__(self, other):
        # допущение имени добавляемого объекста еще нет в списке
        return self.__my_add_element(other, new_products=self)















