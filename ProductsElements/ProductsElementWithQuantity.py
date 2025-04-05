from ProductsElements.ProductsElement import ProductsElement
from loguru import logger


class ProductsElementWithQuantity(ProductsElement):

    SEPARATOR = '|'

    # def __init__(self, name: str, price: float, url:str, kod:str, article:str, brend:str, adress:str):
    def __init__(self,
                 name: str,
                 price: float,
                 url:str,
                 quantity:str=None):

        self.set_quantity(quantity)
        super().__init__(
            name,
            price,
            url
        )


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


    @classmethod
    def decode_elements(cls, encoded_string: str):
        # возвращает список из [kod, article, breand, adress, name]
        SEPARATOR = cls.SEPARATOR
        string = encoded_string.split(SEPARATOR)
        return string


    def get_copy(self):
        # print(f'{self.decode_name(self.get_name())=}')
        return ProductsElementWithQuantity(
            self.get_name(),
            self.get_price(),
            self.get_url(),
            self.get_quantity()
        )

    def get_monitoring_value(self):
        # Этот метод будет выбирать какие данные мониторятся
        # для извлечения отслеживаемых данных для Zabbix и подобных
        # например: (цена или цена за единицу)
        # возвращает словарь с именами и значениями отследивающихся параметров
        # пример: { 'price': self.get_price() }
        # if self.get_quantity() == None:
        #     logger.warning(f'[{self.get_name()=}] [{self.get_price()=}] [{self.get_quantity()=} {self.get_url()=}]')

        # TODO
        #
        # quantity = float(f'{float(self.get_quantity()):.2f}')
        #                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
        # TypeError: float() argument must be a string or a real number, not 'NoneType'


        # quantity = float(f'{float(self.get_quantity()):.2f}')

        try:
            # quantity = float(f'{float(self.get_quantity()):.2f}')
            quantity = round(self.get_quantity(), 2)
        except Exception as Err:
            logger.error(f'{Err=}')
            # logger.error("quantity = float(f'{float(self.get_quantity()):.2f}')")
            logger.error("quantity = round(self.get_quantity(), 2)")
            logger.info(f'{self.get_name()=} {self.get_quantity()=} {self.get_url()=}')

        return {
            # 'price': self.get_price(),
            'price_for_kg': self.get_price(),

            # костыль quantity - is_products_quantity_parsing_needed

            # 'quantity': quantity
            'quantity': self.get_quantity()
            # конец костыля
        }


    def get_str_format_for_write_to_file(self):
        SEPARATOR = self.SEPARATOR
        return super().get_str_format_for_write_to_file()+f"{SEPARATOR}{self.get_quantity()}"
        # return f"{self.kod}{SEPARATOR}{self.article}{SEPARATOR}{self.brend}{SEPARATOR}{product_element}"

    def __str__(self):
        return '\n' + self.get_str_format_for_write_to_file()

    @staticmethod
    def get_copy_from_str_format(string:str):
        SEPARATOR = self.SEPARATOR
        from_string = string.split(SEPARATOR)
        quantity = from_string[-1]
        product_element = ProductsElement.get_copy_from_str_format(f'{SEPARATOR}'.join(from_string[:-1]))

        price = product_element.get_price(),
        url = product_element.get_url(),


        return ProductsElementWithQuantity(
            name = product_element.get_name(),
            price = product_element.get_price(),
            url = product_element.get_url(),
            quantity = quantity
        )



def test():
    pr_el_a = ProductsElementWithQuantity("Аккумулятор", 3568, "Google.com", "302782")
    pr_el_a2 = ProductsElementWithQuantity("Аккумулятор2", 3568, "Google.com")

    print(pr_el_a, pr_el_a2)


def test2():
    from ProductsElements.Products import Products
    from ProductsElements.ProductsElement import ProductsElement
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    products = Products()
    products.append(ProductsElement("Редиска", 250, "https://rediska.com"))
    products.append(ProductsElementWithQuantity("Бруклин", 33.805, "https://kornishon.en", "302782"))

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    print()

    pre = ProductsElement("Груша", 32.805, "https://grusha.ru")
    prea = ProductsElementWithQuantity("Хрюша", 33.805, "https://kornishon.en", 650432)
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

    print(products.keys())


def test_get_copy_from_str_format():
    from ProductsElements.Products import Products
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    products = Products()

    prea = ProductsElementWithQuantity("Хрюша", 33.805, "https://kornishon.en", "650432")
    products += prea

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    prea_str = prea.get_str_format_for_write_to_file()
    print(f'{prea_str=}')

    prea_str2 = "TTT" + prea_str

    prea2 = ProductsElementWithQuantity.get_copy_from_str_format(prea_str2)

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


