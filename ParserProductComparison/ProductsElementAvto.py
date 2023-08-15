from ProductsElement import ProductsElement, SEPARATOR

class ProductsElementAvto(ProductsElement):
    kod: str
    article: str
    brend: str
    SEPARATOR = '|'

    def __init__(self, name: str, price: float, url:str, kod:str, article:str, brend:str, adress:str):
        # super().__init__(name, price, url)

        self.kod = kod
        self.article = article
        self.brend = brend
        self.adress = adress
        super().__init__(
            self.encodeName(name),
            price,
            url
        )

    def encodeName(self, name):
        SEPARATOR = self.SEPARATOR
        return f"{self.kod}{SEPARATOR}{self.article}{SEPARATOR}{self.brend}{SEPARATOR}{self.adress}{SEPARATOR}{name}"


    def decodeName(self, encoded_string: str):
        SEPARATOR = self.SEPARATOR
        string = encoded_string.split(SEPARATOR)
        # print(f'{string=}')
        return string[-1]


    def getCopy(self):
        print(f'{self.decodeName(self.name)=}')
        return ProductsElementAvto(self.decodeName(self.name), self.price, self.url, self.kod, self.article, self.brend, self.adress )


    def getStrFormatForWriteToFile(self):
        # global SEPARATOR
        return super().getStrFormatForWriteToFile()
        # return f"{self.kod}{SEPARATOR}{self.article}{SEPARATOR}{self.brend}{SEPARATOR}{product_element}"


    def getCopyFromStrFormat(self, string:str):
        global SEPARATOR
        from_string = string.split(SEPARATOR)
        self.kod = from_string[0]
        self.article = from_string[1]
        self.brend = from_string[2]
        # print(f'{SEPARATOR}'.join(from_string[4:]))
        product_element = ProductsElement.getCopyFromStrFormat(f'{SEPARATOR}'.join(from_string[4:]))
        # print(f'{self.decodeName(product_element.name)=}')
        return ProductsElementAvto(
            self.decodeName(product_element.name),
            product_element.price,
            product_element.url,
            self.kod,
            self.article,
            self.brend,
            self.adress
        )

    def __str__(self):
        return '\n' + self.getStrFormatForWriteToFile()

def test():
    pr_el_a = ProductsElementAvto("Аккумулятор", 3568, "Google.com", "HITACHI", "302782", "AA700-34")
    pr_el_a2 = ProductsElementAvto("Аккумулятор2", 3568, "Google.com", "HITACHI", "302732", "AA701-34")

    print(pr_el_a, pr_el_a2)


def test2():
    from Products import Products
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

    print()

    products += prea

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)


    print()

    products -= prea

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)


if __name__ == '__main__':
    test2()


