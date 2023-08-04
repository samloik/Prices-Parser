# from DataStrFormat import DataStrFormat

class ProductsElement:
    name: str
    price: float
    url: str

    def __init__(self, name: str, price: float, url:str):
        self.name = name
        self.price = price
        self.url = url

    def getProductsElementCopy(self):
        return ProductsElement(self.name, self.price, self.url)


    def getProductElementName(self):
        return self.name

