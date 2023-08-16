from ProductsElement import ProductsElement, SEPARATOR

class ProductsElementAvto(ProductsElement):
    # _kod: str
    # _article: str
    # _brend: str
    SEPARATOR = '|'

    def __init__(self, name: str, price: float, url:str, kod:str, article:str, brend:str, adress:str):
        # super().__init__(name, price, url)

        self._kod = kod
        self._article = article
        self._brend = brend
        self._adress = adress
        super().__init__(
            self.encode_name(name),
            price,
            url
        )


    def get_kod(self):
        return self._kod

    def set_kod(self, kod):
        self._kod = kod

    def get_article(self):
        return self._article

    def set_article(self, article):
        self._article = article

    def get_brend(self):
        return self._brend

    def set_brend(self, brend):
        self._brend = brend

    def get_adress(self):
        return self._brend

    def set_adress(self, adress):
        self._adress = adress

    def encode_name(self, name):
        SEPARATOR = self.SEPARATOR
        return f"{self.get_kod()}{SEPARATOR}{self.get_article()}{SEPARATOR}{self.get_brend()}{SEPARATOR}{self.get_adress()}{SEPARATOR}{name}"


    def decode_name(self, encoded_string: str):
        SEPARATOR = self.SEPARATOR
        string = encoded_string.split(SEPARATOR)
        # print(f'{string=}')
        return string[-1]


    def get_copy(self):
        print(f'{self.decode_name(self.get_name())=}')
        return ProductsElementAvto(self.decode_name(self.get_name()), self.get_name(), self.get_name(), self.kod, self.article, self.brend, self.adress )


    def gget_str_format_for_write_to_file(self):
        # global SEPARATOR
        return super().get_str_format_for_write_to_file()
        # return f"{self.kod}{SEPARATOR}{self.article}{SEPARATOR}{self.brend}{SEPARATOR}{product_element}"


    def get_copy_from_str_format(self, string:str):
        global SEPARATOR
        from_string = string.split(SEPARATOR)
        self.kod = from_string[0]
        self.article = from_string[1]
        self.brend = from_string[2]
        # print(f'{SEPARATOR}'.join(from_string[4:]))
        product_element = ProductsElement.get_copy_from_str_format(f'{SEPARATOR}'.join(from_string[4:]))
        # print(f'{self.decodeName(product_element.name)=}')
        return ProductsElementAvto(
            self.decode_name(product_element.name),
            product_element.price,
            product_element.url,
            self.kod,
            self.article,
            self.brend,
            self.adress
        )

    def __str__(self):
        return '\n' + self.get_str_format_for_write_to_file()

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


