# from DataStrFormat import DataStrFormat

SEPARATOR = ";"

class ProductsElement:
    _name: str
    _price: float
    _url: str

    def __init__(self, name: str, price: float, url:str):
        self._name = name
        self._price = price
        self._url = url

    def get_copy(self):
        return ProductsElement(self.get_name(), self.get_price(), self.get_url())

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def set_price(self, price):
        self._price = price

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = url


    # TODO сомнительная реализация
    def get_str_format_for_write_to_file(self):
    # def getProductElementStrFormatForWriteToFile(self):
        global SEPARATOR
        return f"{self.get_name()}{SEPARATOR}{str(self.get_price())}{SEPARATOR}{self.get_url()}"

    # TODO сомнительная реализация
    @staticmethod
    def get_copy_from_str_format(string:str):
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
            if self.get_name() == other.get_name():
                return True
        return False


    def __str__(self):
        return self.get_str_format_for_write_to_file()



def test():
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
    products.append(ProductsElementAvto("Бруклин", 33.805, "https://kornishon.en","HITACHI", "302782", "AA700-34", "Chicago"))



    print(products)

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    products_utils = ProductsUtils()
    products_utils.saveProductsToFile(products, "save_file.txt")


def test2():
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
    test()
    test2()
    test3()