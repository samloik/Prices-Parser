from Parser.ParserSite import SiteParser

def main():

    siteParser = SiteParser('https://habarovsk.leroymerlin.ru/search/?q=%D0%BF%D0%B5%D1%81%D0%BE%D0%BA&page=')

    siteParser.getProductsFromSite()


if __name__ == '__main__':
    main()

# TODO
#  добавить в отслеживание ВСЕ источники позицию мел, мука
#  добавить уровень (без цен) парсинг остатков - смотреть продажи позиций
#  добавить сайты мир упаковки, мир инструмента
#  "Упаком" цены и остатки https://upakom.com/katalog/pishhevaja-upakovka/