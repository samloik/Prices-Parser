
from UnitsTypes import UnitsTypes
from loguru import logger

class ElementName:
    def __init__(self, name:str, units_types=None):
        self.name = name
        self.units_types = units_types

    @staticmethod
    def _getNumberFromNameWithSimbols(oldname):
        # return name
        name = oldname.strip().replace(',', '.')
        new_name = ""
        isPointInText = False
        if len(name)>1:
            name_len = len(name)
            length = 0
            for i in range(name_len,0,-1):
                length = i - 1
                # print(f'{name} {name_len=} {i=} {name[length]}')

                # если символ не число и точка уже была
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
        #   для каждого "искомого слова"
        #   -
        #   Если "искомое слово" с единицей измерения содержится в имени, то
        #   делим имя по "искомое слово" на список
        #       если длина списка равна 1, то искомого слова нет
        #       если длина списка равна 2, то искомое число в 0м блоке
        #           (- такой вариант не возможен если есть искмое слово)
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
        #       Иначе двигаемся дальше от конца, пока не прекратиться условие: это не цифра или '.'
        #           вырезаем полученный текст с числом
        #           пробуем преобразовать в тип float
        #               если '.' появляется второй раз, то на этом число окончено
        #
        #

    def getValueOfUnitsInName(self):
        result = ''

        if not self.units_types or len(self.units_types) == 0 or UnitsTypes.KG in self.units_types:
            logger.info(f'f[ ] "кг" пробуем извлечь [{self.units_types=}] [{self.name}]')
            # если unit_types=None, или список пуст, или есть UnitsTypes.KG в списке, то:
            unitsList = ["килограмм", "кг"]
            for units in unitsList:
                result = self._getValueOfUnitsInNameByContent(units)
                if len(result) > 0:
                    break

            # добавляем проверку на граммы
            if len(result) == 0:
                logger.info(f'f[ ] "грамм" пробуем извлечь [{self.units_types=}] [{self.name}]')
                unitsList = ["грамм", "г"]
                for units in unitsList:
                    result = self._getValueOfUnitsInNameByContent(units)
                    if len(result) > 0:
                        result = str(float(result)/1000)
                        break

        if self.units_types and UnitsTypes.LITR in self.units_types and len(result) == 0:
            # если unit_types не None и есть UnitsTypes.LITR в списке, то:
            # добавляем проверку на литр
            logger.info(f'f[ ] "литр" пробуем извлечь [{self.units_types=}] [{self.name}]')
            unitsList = ["литр", "л"]
            for units in unitsList:
                result = self._getValueOfUnitsInNameByContent(units)
                if len(result) > 0:
                    break

            # добавляем проверку на милилитры
            if len(result) == 0:
                logger.info(f'f[ ] "миллилитр" пробуем извлечь [{self.units_types=}] [{self.name}]')
                unitsList = ["миллилитр", "мл"]
                for units in unitsList:
                    result = self._getValueOfUnitsInNameByContent(units)
                    if len(result) > 0:
                        result = str(float(result)/1000)
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


    def _getValueOfUnitsInNameByContent(self, content):
        # content = "кг"
        name = self.name.lower()

        # делим имя по "искомое слово" на список
        strings = name.split(content.lower())

        string_len = len(strings)

        # если длина списка равна 1, то искомого слова нет
        if string_len == 1:
            return ''
        # если длина списка равна 2, то искомое число в 0м блоке
        if string_len == 2:
            return self._getNumberFromNameWithSimbols(strings[0])

        # если длина списка больше двух то ("искомых слов" больше одного)
        #   ищем числа во всех блоках,
        count_of_numbers = 0
        # получаем список чисел в виде текста
        numbersInText = [self._getNumberFromNameWithSimbols(text) for text in strings]
        # если длина элемента больше 0 то выставляем 1 иначе 0
        numbersInInt = [1 if len(numberInText)>0 else 0 for numberInText in numbersInText]
        # если число встречается только один раз, то число найдено
        if sum(numbersInInt) != 1:
            return ''
        else:
            return numbersInText[numbersInInt.index(1)]


    def _getNumberFromStringByContent(self, name, content):
        new_string = ""
        # name = oldname
        # i = 133
        if content.lower() in name.lower():
            new_string = name[:name.lower().index(content.lower())].strip()
        # i = 133
        # print(f'{new_string=}')
        # print(f'{self._getNumberFromNameWithSimbols(new_string)=}')
        # i = 133
        return self._getNumberFromNameWithSimbols(new_string)




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
    products = products_utils.loadProductsFromFile("stock_centr_save_file.txt")

    # render = DataRenderer()
    # render.render(products, DataStrFormat.WIDE)
    print(f'\n{len(products)=}\n')

    # print('elementName.getUnitsFromName():')

    for name in products.products.keys():
        elementName = ElementName(name, [UnitsTypes.KG, UnitsTypes.LITR])

        valuesFromName = elementName.getValuesFromName()
        if  valuesFromName != "":
            # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
            print(f'[+] {name:>100} | {valuesFromName}')
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

    valuesFromName = elementName.getValuesFromName()
    if valuesFromName != "":
        # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
        print(f'[+] {name:>100} | {valuesFromName}')
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
    elementName = ElementName(name, [UnitsTypes.KG, UnitsTypes.LITR])

    valuesFromName = elementName.getValueOfUnitsInName()
    if valuesFromName != "":
        # print(f'[+] {products.products[name]:>50} | {valuesFromName}')
        print(f'[+] {name:>100} | {valuesFromName}')
    else:
        print(f'[ ] {name:>100} | Null')


def main6():
    # main()
    main2(name = 'Ceresit СN-173/20кг Пол быстротв.самовырав.универс.')
    main2(name = 'Ceresit СN-173/2-40,56л Пол быстротв.самовырав.универс.')
    main2(name = 'Ceresit СN-173/20литров Пол быстротв.самовырав.универс.')
    main2(name = 'Ceresit СN-173/20,54граМм Пол быстротв.самовырав.универс.')
    main2(name = 'Ceresit СN-173/0,540г Пол быстротв.самовырав.универс.')
    main2(name = 'Ceresit СN-173/540мл Пол быстротв.самовырав.универс.')

    # main2(name='Шпатлевка Шпакрил ЭКСТРА 2кг пакет Супербелый КВАРТ')
    # main2(name='Противоморозная добавка "Штайнберг FROST 25" 20.5 г')

if __name__ == '__main__':
    # main2(name = 'Ceresit СN-173/20литров Пол быстротв.самовырав.универс.')
    main6()
    # main5()