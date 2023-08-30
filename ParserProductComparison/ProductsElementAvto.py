from ProductsElement import ProductsElement, SEPARATOR

class ProductsElementAvto(ProductsElement):
    # _kod: str
    # _article: str
    # _brend: str
    SEPARATOR = '|'

    # def __init__(self, name: str, price: float, url:str, kod:str, article:str, brend:str, adress:str):
    def __init__(self,
                 name: str,
                 price: float,
                 url:str,
                 kod:str,
                 article:str,
                 brend:str,
                 adress:str,
                 quantity=None):

        self.set_kod(kod)
        self.set_article(article)
        self.set_brend(brend)
        self.set_adress(adress)
        self.set_quantity(quantity)
        super().__init__(
            self.encode_name(name),
            price,
            url
        )


    def set_kod(self, kod):
        self._kod = kod

    def get_kod(self):
        return self._kod


    def set_article(self, article):
        self._article = article

    def get_article(self):
        return self._article


    def set_brend(self, brend):
        self._brend = brend

    def get_brend(self):
        return self._brend


    def set_adress(self, adress):
        self._adress = adress

    def get_adress(self):
        return self._adress


    def set_quantity(self, quantity):
        # print(f'[set_quantity] {type(quantity)=} {quantity=}')
        if isinstance(quantity, str):
            try:
                # print(f'--> Start')
                self._quantity= {
                    'None': None
                 }[quantity]
                # print(f'--> End {self._quantity=}')

            except Exception as Err:
                # print(f'--> exception')
                self._quantity = quantity
        else:
            # print(f'--> not isinstance')
            self._quantity = quantity

    def get_quantity(self):
        return self._quantity


    def encode_name(self, name):
        SEPARATOR = self.SEPARATOR
        return f"{self.get_kod()}{SEPARATOR}{self.get_article()}{SEPARATOR}{self.get_brend()}{SEPARATOR}{self.get_adress()}{SEPARATOR}{name}"


    def decode_name(self, encoded_string: str):
        SEPARATOR = self.SEPARATOR
        string = encoded_string.split(SEPARATOR)
        return string[-1]

    @classmethod
    def decode_elements(cls, encoded_string: str):
        # возвращает список из [kod, article, breand, adress, name]
        SEPARATOR = cls.SEPARATOR
        string = encoded_string.split(SEPARATOR)
        return string


    def get_copy(self):
        # print(f'{self.decode_name(self.get_name())=}')
        return ProductsElementAvto(
            self.decode_name(self.get_name()),
            self.get_price(),
            self.get_url(),
            self.get_kod(),
            self.get_article(),
            self.get_brend(),
            self.get_adress(),
            self.get_quantity()
        )


    def get_str_format_for_write_to_file(self):
        global SEPARATOR
        return super().get_str_format_for_write_to_file()+f"{SEPARATOR}{self.get_quantity()}"
        # return f"{self.kod}{SEPARATOR}{self.article}{SEPARATOR}{self.brend}{SEPARATOR}{product_element}"

    def __str__(self):
        return '\n' + self.get_str_format_for_write_to_file()

    @staticmethod
    def get_copy_from_str_format(string:str):
        global SEPARATOR
        from_string = string.split(SEPARATOR)

        from_string2 = ProductsElementAvto.decode_elements(from_string[0])
        kod = from_string2[0]
        article = from_string2[1]
        brend = from_string2[2]
        adress = from_string2[3]
        name = from_string2[4]

        quantity = from_string[-1]

        product_element = ProductsElement.get_copy_from_str_format(f'{SEPARATOR}'.join(from_string[:-1]))

        price = product_element.get_price(),
        url = product_element.get_url(),


        return ProductsElementAvto(
            name,
            product_element.get_price(),
            product_element.get_url(),
            kod =  kod,
            article = article,
            brend = brend,
            adress = adress,
            quantity = quantity
        )



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


def test_get_copy_from_str_format():
    from Products import Products
    from ProductsElement import ProductsElement
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    products = Products()

    prea = ProductsElementAvto("Хрюша", 33.805, "https://kornishon.en", "TOTAL", "650432", "NN701-85", "Чапаего")
    products += prea

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    prea_str = prea.get_str_format_for_write_to_file()
    print(f'{prea_str=}')

    prea_str2 = "TTT" + prea_str

    prea2 = ProductsElementAvto.get_copy_from_str_format(prea_str2)

    products += prea2

    prea_str3 = prea2.get_str_format_for_write_to_file()
    print(f'{prea_str3=}')

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    pr = products.get_element_by_name(prea2.get_name())
    print(f'==> {(type(pr.get_quantity()))=}')

if __name__ == '__main__':
    # print(isinstance(None, str))
    test_get_copy_from_str_format()
    # test2()


