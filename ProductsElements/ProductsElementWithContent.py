from ProductsElements.ProductsElement import ProductsElement
from loguru import logger


class ProductsElementWithContent(ProductsElement):

    SEPARATOR = '|'

    # def __init__(self, name: str, price: float, url:str, kod:str, article:str, brend:str, adress:str):
    def __init__(self,
                 name: str,
                 price: float,
                 url:str,
                 content:dict=None):

        self.set_content(content)
        super().__init__(
            name,
            price,
            url
        )


    def set_content(self, content):
        # print(f'[set_quantity] {type(quantity)=} {quantity=}')
        if isinstance(content, dict):
            self._content = content
        elif isinstance(content, str):
            try:
                new_content =content.replace("'", "\"")
                self._content = eval(new_content)
                logger.warning(f'получаем содержимое в self._content=dict() из строки, т.к не соотвествие типу dict {type(content)=}')
            except Exception as Err:
                logger.error(f'не удается преобразовать в словарь для self._content=dict() из строки [{content=}], т.к не соотвествие типу dict {type(content)=}')
                logger.error(f'Ошибка: {Err}')
                exit(1)
        else:
            logger.warning(f'сбрасываем содержимое в self._content=dict() из-за не соотвествия типу dict {type(content)=}')
            self._content = {}


    def get_content(self):
        try:
            content = self._content
        except Exception as Err:
            logger.warning(f'запрашиваемый self._content не задан, возвращаем пустой dict()')
            content = {}
        return content


    @classmethod
    def decode_elements(cls, encoded_string: str):
        # возвращает список из [kod, article, breand, adress, name]
        SEPARATOR = cls.SEPARATOR
        string = encoded_string.split(SEPARATOR)
        return string


    def get_copy(self):
        # print(f'{self.decode_name(self.get_name())=}')
        return ProductsElementWithContent(
            self.get_name(),
            self.get_price(),
            self.get_url(),
            self.get_content()
        )

    def get_monitoring_value(self):
        # Этот метод будет выбирать какие данные мониторятся
        # для извлечения отслеживаемых данных для Zabbix и подобных
        # например: (цена или цена за единицу)
        # возвращает словарь с именами и значениями отследивающихся параметров
        # пример: { 'price': self.get_price() }
        # if self.get_quantity() == None:
        #     logger.warning(f'[{self.get_name()=}] [{self.get_price()=}] [{self.get_quantity()=} {self.get_url()=}]')

        content = self.get_content()
        return {
            'price': self.get_price()
        } | content


    def get_str_format_for_write_to_file(self):
        SEPARATOR = self.SEPARATOR
        return super().get_str_format_for_write_to_file()+f"{SEPARATOR}{str(self.get_content())}"
        # return f"{self.kod}{SEPARATOR}{self.article}{SEPARATOR}{self.brend}{SEPARATOR}{product_element}"

    def __str__(self):
        return '\n' + self.get_str_format_for_write_to_file()

    @staticmethod
    def get_copy_from_str_format(string:str):
        SEPARATOR = self.SEPARATOR
        from_string = string.split(SEPARATOR)
        content = from_string[-1]
        product_element = ProductsElement.get_copy_from_str_format(f'{SEPARATOR}'.join(from_string[:-1]))

        price = product_element.get_price(),
        url = product_element.get_url(),


        return ProductsElementWithContent(
            name = product_element.get_name(),
            price = product_element.get_price(),
            url = product_element.get_url(),
            content = content
        )



def test():
    pr_el_a = ProductsElementWithContent("Аккумулятор", 3568, "Google.com", {"302782": "12", "Серега":-1})
    pr_el_a2 = ProductsElementWithContent("Аккумулятор2", 3568, "Google.com")

    print(pr_el_a, pr_el_a2)


def test2():
    from ProductsElements.Products import Products
    from ProductsElements.ProductsElement import ProductsElement
    from DataRenderer import DataRenderer
    from DataStrFormat import DataStrFormat

    products = Products()
    products.append(ProductsElement("Редиска", 250, "https://rediska.com"))
    products.append(ProductsElementWithContent("Бруклин", 33.805, "https://kornishon.en", {"43":"302782"}))

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    print()

    pre = ProductsElement("Груша", 32.805, "https://grusha.ru")
    prea = ProductsElementWithContent("Хрюша", 33.805, "https://kornishon.en", {650432: 131})
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

    prea = ProductsElementWithContent("Хрюша", 33.805, "https://kornishon.en", "{'650432' : '43'}")
    products += prea

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    prea_str = prea.get_str_format_for_write_to_file()
    print(f'{prea_str=}')

    prea_str2 = "TTT" + prea_str

    prea2 = ProductsElementWithContent.get_copy_from_str_format(prea_str2)

    products += prea2

    prea_str3 = prea2.get_str_format_for_write_to_file()
    print(f'{prea_str3=}')

    render = DataRenderer()
    render.render(products, DataStrFormat.WIDE)

    pr = products.get_element_by_name(prea2.get_name())
    print(f'==> {(type(pr.get_content()))=}')




if __name__ == '__main__':
    # test_string= "'650432' : '43'"
    # test_string = "{'Nikhil' : 1, 'Akshat' : 2, 'Akash' : 3}"
    # res = eval(test_string.replace("'", "\""))
    # print(res)


    # test_get_copy_from_str_format()
    test()


