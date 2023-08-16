
from UnitsTypes import UnitsTypes
from loguru import logger

class ElementName:
    name: str
    units_types: UnitsTypes

    def __init__(self, name:str, units_types=None):
        self.set_name(name)
        self.set_units_types(units_types)


    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_units_types(self, unit_types: UnitsTypes):
        self.units_types = unit_types

    def get_units_types(self):
        return self.units_types

    @staticmethod
    def _get_number_from_name_with_simbols(oldname):
        # Метод извлечения числа из строки с числом и символами

        name = oldname.strip().replace(',', '.')
        new_name = ""
        isPointInText = False
        if len(name)>1:
            name_len = len(name)
            length = 0
            for i in range(name_len,0,-1):
                length = i - 1
                # print(f'{name} {name_len=} {i=} {name[length]}')

                # если символ не число
                if not name[i-1].isdigit():
                    # точка и точка еще не было
                    if name[i-1] in '.' and not isPointInText:
                        # обозначаем, что точка была
                        isPointInText = True
                    else:
                        break

            # print(f'{name[length+1:]=}')
            new_name = name[length+1:]
            # если длина числа равна 1 и точка была в тексте, то числа нет
            if len(new_name) == 1 and isPointInText == True:
                new_name = ''
        else:
            if name.isdigit():
                new_name = name

        return new_name


        # TODO описание логики поиска
        #   -
        #   для каждого "искомого слова"
        #   -
        #   Если "искомое слово" с единицей измерения содержится в имени, то
        #   делим имя по "искомое слово" на список
        #       если длина списка равна 1, то искомого слова нет
        #       если длина списка равна 2, то искомое число в 0м блоке
        #       если длина списка больше двух то ("искомых слов" больше одного)
        #           ищем числа во всех блоках,
        #               ( - если находим больше одного числа, то числа нет )
        #               ( - если ненаходим числа, то числа нет )
        #               если число встречается только один раз, то число найдено
        #   - поиск числа -
        #   блок обрезается от пробеллов
        #   - менаем ',' на '.' - т.к. float принимает только точки
        #   смотрим последний символ
        #       Если это не цифра или '.', то число не в этом блоке
        #       Иначе двигаемся дальше от конца, пока не прекратиться условие: это цифра или '.'
        #           вырезаем полученный текст с числом
        #           пробуем преобразовать в тип float
        #               если '.' появляется второй раз, то на этом число окончено

        # TODO
        #   переделать логику на 'л'
        #   -
        #   возвращает такое  значение на UnitsTypes.LITR - оно не верно!
        #   -
        #   Продумать - переделать - проверить
        #   -
        #   [Ceresit СN-178 Легковыравнивающаяся смесь (5-80мм) 25кг для внутр. и нар. работ
        #   ] сохранено valueFromName='178.0' units_types=[<UnitsTypes.LITR: 2>]
        #   -
        #   Попытка сформулировать алгоритм №1
        #   после некоторых единиц, напрмер, "л", "мл", "кг" измерения не должно быть символов,
        #       кроме <конец строки>, <пробел>, '.', ',','-','/' возможны варианты
        #   Если в конце указателя на такую "строгую" единицу измерения в конце стоит знак "!"
        #       то такой контент является строгим и обрабатывается этой логикой, иначе
        #       попускается продолжение текста (контента) любыми символами


    def get_value_of_units_in_name(self):
        result = ''

        if not self.units_types or len(self.units_types) == 0 or UnitsTypes.KG in self.units_types:
            # logger.info(f'f[ ] "кг" пробуем извлечь [{self.units_types=}] [{self.name}]')
            # если unit_types=None, или список пуст, или есть UnitsTypes.KG в списке, то:
            unitsList = ["килограмм", "кг!"]
            for units in unitsList:
                result = self._get_value_of_units_in_name_by_content(units)
                if len(result) > 0:
                    break

            # добавляем проверку на граммы
            if len(result) == 0:
                # logger.info(f'f[ ] "грамм" пробуем извлечь [{self.units_types=}] [{self.name}]')
                unitsList = ["грамм", "г!"]
                for units in unitsList:
                    result = self._get_value_of_units_in_name_by_content(units)
                    if len(result) > 0:
                        result = str(float(result)/1000)
                        break

        if self.units_types and UnitsTypes.LITR in self.units_types and len(result) == 0:
            # если unit_types не None и есть UnitsTypes.LITR в списке, то:
            # добавляем проверку на литр
            # logger.info(f'f[ ] "литр" пробуем извлечь [{self.units_types=}] [{self.name}]')
            # [Ceresit СN-178 Легковыравнивающаяся смесь (5-80мм) 25кг для внутр. и нар. работ
            # ] сохранено valueFromName='178.0' units_types=[<UnitsTypes.LITR: 2>]
            unitsList = ["литр", "л!"]
            for units in unitsList:
                result = self._get_value_of_units_in_name_by_content(units)
                if len(result) > 0:
                    break

            # добавляем проверку на милилитры
            if len(result) == 0:
                # logger.info(f'f[ ] "миллилитр" пробуем извлечь [{self.units_types=}] [{self.name}]')
                unitsList = ["миллилитр", "мл!"]
                for units in unitsList:
                    result = self._get_value_of_units_in_name_by_content(units)
                    if len(result) > 0:
                        result = str(float(result)/1000)
                        break

        if self.units_types and UnitsTypes.SHTUK in self.units_types and len(result) == 0:
            # logger.info(f'f[ ] "штук" пробуем извлечь [{self.units_types=}] [{self.name}]')
            unitsList = ["штук!", "шт!"]
            for units in unitsList:
                result = self._get_value_of_units_in_name_by_content(units)
                if len(result) > 0:
                    break


        if len(result) > 0:
            try:
                number = float(result)
                result = str(number)
                logger.info(f'[+] Удалось извлечь число из [{result}] [{self.name=}]')
            except Exception as Error:
                logger.warning(f'[-] Не удалось извлечь число из [{self.name=}] {Error=}')
                result = ''
        return result

    def _get_value_of_units_in_name_by_content(self, content):

        #  TODO
        #   Попытка сформулировать алгоритм №1
        #   после некоторых единиц, напрмер, "л", "мл", "кг" измерения не должно быть символов,
        #       кроме <конец строки>, <пробел>, '.', ',','-','/' возможны варианты
        #   Если в конце указателя на такую "строгую" единицу измерения в конце стоит знак "!"
        #       то такой контент является строгим и обрабатывается этой логикой, иначе
        #       попускается продолжение текста (контента) любыми символами

        if len(content) > 1 and content[-1] == "!":
            # допускается текст после content
            return self._get_Value_of_units_in_name_by_content_strong(content[:-1])
        else:
            # допускается ничего или только специальные символы после content
            return self._get_Value_of_units_in_name_by_content_soft(content)


    def _get_Value_of_units_in_name_by_content_soft(self, content):

        name = self.name.lower()

        # делим имя по имя через "искомое слово" на список
        strings = name.split(content.lower())

        string_len = len(strings)

        # если длина списка равна 1, то искомого слова нет
        if string_len == 1:
            return ''
        # если длина списка равна 2, то искомое число в 0м блоке
        if string_len == 2:
            return self._get_number_from_name_with_simbols(strings[0])

        # если длина списка больше двух то ("искомых слов" больше одного)
        #   ищем числа во всех блоках,
        count_of_numbers = 0
        # получаем список чисел в виде текста
        numbers_in_text = [self._get_number_from_name_with_simbols(text) for text in strings]
        # если длина элемента больше 0 то выставляем 1 иначе 0
        numbers_in_int = [1 if len(number_in_text)>0 else 0 for number_in_text in numbers_in_text]
        # если число встречается только один раз, то число найдено
        if sum(numbers_in_int) != 1:
            return ''
        else:
            return numbers_in_text[numbers_in_int.index(1)]

    @staticmethod
    def _check_begin_of_string_for_posible_simbols(str):
        if len(str) == 0:
            return True
        if str[0] in ' .,-()[]/\\':
            return True
        else:
            return False


    def _get_Value_of_units_in_name_by_content_strong(self, content):
        #  TODO
        #   Попытка сформулировать алгоритм №1
        #   после некоторых единиц, напрмер, "л", "мл", "кг" измерения не должно быть символов,
        #       кроме <конец строки>, <пробел>, '.', ',','-','/' возможны варианты
        #   Если в конце указателя на такую "строгую" единицу измерения в конце стоит знак "!"
        #       то такой контент является строгим и обрабатывается этой логикой, иначе
        #       попускается продолжение текста (контента) любыми символами

        # TODO
        #  не решена логика таких повторяющихся сивмолов как 'лл', 'гг'
        #  вариант решение отслеживанием двух подряд пустых элемента в strings
        #  -
        #  продумать логику - реализовать
        #  проверить

        name = self.name.lower()

        # делим имя по имя через "искомое слово" на список
        strings = name.split(content.lower())

        string_len = len(strings)

        # если длина списка равна 1, то искомого слова нет
        if string_len == 1:
            return ''
        # если длина списка равна 2, то искомое число в 0м блоке
        if string_len == 2:
            # проверяем на разрешенные символы после content
            if self._check_begin_of_string_for_posible_simbols(strings[1]):
                return self._get_number_from_name_with_simbols(strings[0])
            return ''

        # если длина списка больше двух то ("искомых слов" больше одного)
        #   ищем числа во всех блоках,
        count_of_numbers = 0
        # получаем список чисел в виде текста
        numbers_in_text = [self._get_number_from_name_with_simbols(text) for text in strings]
        # если длина элемента больше 0 то выставляем 1 иначе 0
        # numbers_in_int = [1 if len(number_in_text) > 0 else 0 for number_in_text in numbers_in_text]

        new_numbers_in_text = numbers_in_text.copy()
        # new_numbers_in_int = numbers_in_int.copy()
        new_numbers_in_int = []

        for x, number_in_text in enumerate(new_numbers_in_text):
            if len(number_in_text) == 0:
                new_numbers_in_int.append(0)
            elif x == len(new_numbers_in_text)-1:
                new_numbers_in_int.append(1)
            elif self._check_begin_of_string_for_posible_simbols(strings[x+1]) == True:
                new_numbers_in_int.append(1)
            else:
                new_numbers_in_int.append(0)


        # если число встречается только один раз, то число найдено
        if sum(new_numbers_in_int) != 1:
            return ''
        else:
            return new_numbers_in_text[new_numbers_in_int.index(1)]


    def translit_name(self):
        """
        переводит текст с кириллицы на транслит убирает символы нечитаемые zabbix'ом
        формат zabbix key: 0-9a-zA-Z_-.

        :param text: исходный текст
        :return: обработанный текст
        """

        text = self.name

        symbols = str.maketrans(u"абвгдезийклмнопрстуфхъыьАБВГДЕЗИЙКЛМНОПРСТУФХЪЫЬ",
                                u"abvgdezijklmnoprstufh'y'ABVGDEZIJKLMNOPRSTUFH'Y'")
        sequence = {
            u'ж': 'zh',
            u'ц': 'ts',
            u'ч': 'ch',
            u'ш': 'sh',
            u'щ': 'sch',
            u'ю': 'ju',
            u'я': 'ya',

            u'Ж': 'Zh',
            u'Ц': 'Ts',
            u'Ч': 'Ch',
            u'Ш': 'Sh',  # дописано
            u'Щ': 'Sch',  # дописано
            u'Ю': 'Ju',  # дописано
            u'Я': 'Ya',  # дописано

            u'э': 'eh',  # дополнено
            u'Э': 'Eh',  # дополнено
            u'Ё': 'Yo',  # дополнено
            u'ё': 'yo',  # дополнено
        }

        for char in sequence.keys():
            text = text.replace(char, sequence[char])

        txt = text.translate(symbols)

        # убрать символы нечитаемые zabbix'ом
        # https://www.zabbix.com/documentation/current/en/manual/config/items/item/key
        # 0-9a-zA-Z_-.

        ntext0 = ''.join([str(i) for i in range(10)])
        ntext1 = ''.join([chr(i) for i in range(ord('a'), ord('z') + 1)])
        ntext2 = ''.join([chr(i) for i in range(ord('A'), ord('Z') + 1)])
        ntext3 = '_.'
        ntext = ntext0 + ntext1 + ntext2 + ntext3

        # print(txt)
        for ch in txt:
            if ch not in ntext:
                txt = txt.replace(ch, '_')
        # print(txt)

        return txt



def main():

    from DataRenderer import DataRenderer
    # from Products import Products
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils
    from ElementName import ElementName
    # from UnitsTypes import UnitsTypes


    logger.remove()

    products_utils = ProductsUtils()
    # products = products_utils.loadProductsFromFile("cleaned_stock_centr_save_file.txt")
    products = products_utils.load_products_from_file("stock_centr_save_file.txt")

    # render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)
    print(f'\n{len(products)=}\n')

    # print('elementName.getUnitsFromName():')

    for name in products.products.keys():
        elementName = ElementName(name, [UnitsTypes.KG, UnitsTypes.LITR])

        values_from_name = elementName.get_value_of_units_in_name()
        if  values_from_name != "":
            # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
            print(f'[+] {name:>100} | {values_from_name}')
        else:
            print(f'[ ] {name:>100} | Null')


def main10(name):

    from DataRenderer import DataRenderer
    # from Products import Products
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils
    from ElementName import ElementName
    # from UnitsTypes import UnitsT

    logger.remove()

    # name = 'Ceresit СN-173/20кг Пол быстротв.самовырав.универс.'
    elementName = ElementName(name, [UnitsTypes.KG, UnitsTypes.LITR])

    values_from_name = elementName.get_value_of_units_in_name()
    if values_from_name != "":
        # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
        print(f'[+] {name:>100} | {values_from_name}')
    else:
        print(f'[ ] {name:>100} | Null')


def main5():
    string = 'Ceresit СN-173/20  грамм Пол быстротв.самовырав.универс.'
    print(string.split('г1'))
    print(float(".0565"))

def main2(name):
    from DataRenderer import DataRenderer
    # from Products import Products
    from DataStrFormat import DataStrFormat
    from ProductsUtils import ProductsUtils
    from ElementName import ElementName
    # from UnitsTypes import UnitsT

    # logger.remove()

    # name = 'Ceresit СN-173/20кг Пол быстротв.самовырав.универс.'
    elementName = ElementName(name, [UnitsTypes.SHTUK, UnitsTypes.LITR])

    values_from_name = elementName.get_value_of_units_in_name()
    if values_from_name != "":
        # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
        print(f'[+] {name:>100} | {values_from_name}')
    else:
        print(f'[ ] {name:>100} | Null')


def main6():
    # main()
    # main2(name = 'Ceresit СN-173/20кг Пол быстротв.самовырав.универс.')
    # main2(name = 'Ceresit СN-173/2-40,56л Пол быстротв.самовырав.универс.')
    main2(name = 'Ceresit СN-173/2-40,57лт Пол быстротв.самовырав.универс.40,56л')
    # main2(name = 'Ceresit СN-173/2- Пол быстротв.самовырав.универс.40,56л')
    # main2(name = 'Ceresit СN-173/20литров Пол быстротв.самовырав.универс.')
    # main2(name = 'Ceresit СN-173/20,54граМм Пол быстротв.самовырав.универс.')
    # main2(name = 'Ceresit СN-173/0,540г Пол быстротв.самовырав.универс.')
    # main2(name = 'Ceresit СN-173/540млл Пол быстротв.самовырав.универс.')

    # main2(name='Шпатлевка Шпакрил ЭКСТРА 2кг пакет Супербелый КВАРТ')
    # main2(name='Противоморозная добавка "Штайнберг FROST 25" 20.5 г')

def main7():
    string = "кг!"
    print(string)
    print(string[-1])
    print(string[:-1])

    string2 = 'Привет как у тебя дела?'
    print(string2)
    new_numbers_in_text = string2.split("к")
    print(new_numbers_in_text)
    new_numbers_in_int = []
    for x, number_in_text in enumerate(new_numbers_in_text):
        print(f'{x=} {number_in_text=} {len(new_numbers_in_text)=}')
        if len(number_in_text) == 0:
            new_numbers_in_int.append(0)
        elif x == len(new_numbers_in_text)-1:
            new_numbers_in_int.append(1)
        else:
            new_numbers_in_int.append(0)
    print(new_numbers_in_int)

def translit_test():
    en = ElementName(u"Желёзная дорога эхо", [UnitsTypes.KG, UnitsTypes.LITR])
    en2 = ElementName(u"Privet", [UnitsTypes.KG, UnitsTypes.LITR])
    en3 = ElementName(u"Пакет ПВД 2,5кг 250х350 (200шт) 25мк Impacto Pro Оптима", [UnitsTypes.KG, UnitsTypes.LITR, UnitsTypes.SHTUK])

    print(en.translitName())
    print(en2.translitName())
    print(en3.translitName())

if __name__ == '__main__':
    main2(name = 'Ceresit СN-173/20литров Пол быстротв.самовырав.универс.')
    main2(name = 'Пакет ПВД 2,5кг 250х350 (200шт) 25мк Impacto Pro Оптима')
    # translit_test()
    # main6()
    # main5()