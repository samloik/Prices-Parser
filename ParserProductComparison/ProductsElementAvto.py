from ProductsElement import ProductsElement, SEPARATOR

class ProductsElementAvto(ProductsElement):
    kod: str
    article: str
    brend: str

    def __init__(self, name: str, price: float, url:str, kod:str, article:str, brend:str):
        super().__init__(name, price, url)
        self.kod = kod
        self.article = article
        self.brend = brend

    def getCopy(self):
        return ProductsElementAvto(self.name, self.price, self.url, self.kod, self.article, self.brend )

    def getStrFormatForWriteToFile(self):
        global SEPARATOR
        product_element = super().getStrFormatForWriteToFile()
        return f"{self.kod}{SEPARATOR}{self.article}{SEPARATOR}{self.brend}{SEPARATOR}{product_element}"


    def getCopyFromStrFormat(self, string:str):
        global SEPARATOR
        from_string = string.split(SEPARATOR)
        self.kod = from_string[0]
        self.article = from_string[1]
        self.brend = from_string[2]
        product_element = ProductsElement.getCopyFromStrFormat(f'{SEPARATOR}'.join(from_string[3:]))
        return ProductsElementAvto(
            product_element.name,
            product_element.price,
            product_element.url,
            self.kod,
            self.article,
            self.brend
        )

    def __str__(self):
        return '\n' + self.getStrFormatForWriteToFile()

def test():
    pr_el_a = ProductsElementAvto("Аккумулятор", 3568, "Google.com", "HITACHI", "302782", "AA700-34")
    pr_el_a2 = ProductsElementAvto("Аккумулятор2", 3568, "Google.com", "HITACHI", "302732", "AA701-34")

    print(pr_el_a, pr_el_a2)

if __name__ == '__main__':
    test()