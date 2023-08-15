# from DataStrFormat import DataStrFormat

SEPARATOR = ";"

class ProductsElement:
    name: str
    price: float
    url: str

    def __init__(self, name: str, price: float, url:str):
        self.name = name
        self.price = price
        self.url = url

    def getCopy(self):
        return ProductsElement(self.name, self.price, self.url)

    # def getProductsElementCopy(self):
    #     return ProductsElement(self.name, self.price, self.url)


    def getName(self):
        return self.name


    # def getProductElementName(self):
    #     return self.name

    # TODO сомнительная реализация
    def getStrFormatForWriteToFile(self):
    # def getProductElementStrFormatForWriteToFile(self):
        global SEPARATOR
        return f"{self.name}{SEPARATOR}{str(self.price)}{SEPARATOR}{self.url}"

    # TODO сомнительная реализация
    @staticmethod
    def getCopyFromStrFormat(string:str):
    # def getProductElementCopyFromStrFormat(string:str):
        global SEPARATOR
        from_string = string.split(SEPARATOR)
        name = from_string[0]
        price = float(from_string[1])
        url = from_string[2]
        return ProductsElement(name, price, url)

    def __eq__(self, other):
        # Допущение объект не должен быть равен самому себе
        if not other is None and isinstance(other, ProductsElement) and not id(self) == id(other):
            if self.name == other.name:
                return True
        return False

    # def __ne__(self, other):
    #     pass




def main():
    from DataRenderer import DataRenderer
    from Products import Products
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils
    products = Products()
    products.append(ProductsElement("Редиска", 250, "https://rediska.com"))
    products.append(ProductsElement("Груша", 32.805, "https://grusha.ru"))
    products.append(ProductsElement("Корнишон", 32.805, "https://kornishon.en"))
    products.append(ProductsElement("2Корнишон", 33.805, "https://kornishon.en"))

    from ParserProductComparison.ProductsElementAvto import ProductsElementAvto
    products.append(ProductsElementAvto("Бруклин", 33.805, "https://kornishon.en","HITACHI", "302782", "AA700-34"))



    print(products)

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    products_utils = ProductsUtils()
    products_utils.saveProductsToFile(products, "save_file.txt")


def main2():
    from DataRenderer import DataRenderer
    from Products import Products
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils

    products_utils = ProductsUtils()
    products = products_utils.loadProductsFromFile("save_file.txt")

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)


def test3():
    from DataRenderer import DataRenderer
    from Products import Products
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils
    products = Products()
    pe1 = ProductsElement("Редиска", 250, "https://rediska.com")
    pe2 = ProductsElement("Груша", 32.805, "https://grusha.ru")
    pe3 = ProductsElement("Корнишон", 32.805, "https://kornishon.en")
    pe4 = ProductsElement("2Корнишон", 33.805, "https://kornishon.en")
    pe5 = ProductsElement("Редиска", 250, "https://rediska.com")

    print(pe1==pe2)
    print(pe1==pe3)
    print(pe1==pe5)
    print(pe1==pe1)


if __name__ == '__main__':
    test3()