from DataStrFormat import DataStrFormat
from ProductsElements.ProductsElement import ProductsElement
from ProductsElements.Products import Products

class DataRenderer:

    def render(self, products:Products, dataStrFormat=DataStrFormat.SHORT):
        for product_key in products.keys():
            product = products[product_key]
            line = {
                DataStrFormat.WIDE: "<" + f"{product.get_name():>120}|{float(product.get_price()):>9.2f}|{product.get_url()}" + ">\n",
                DataStrFormat.MIDDLE: "<" + f"{product.get_name():>40}|{float(product.get_price()):>9.2f}|{product.get_url()}" + "> ",
                DataStrFormat.SHORT: "<" + f"{product.get_name()}|{float(product.get_price()):>0.2f}|{product.get_url()}" + "> "
            }[dataStrFormat]
            print(line, end='')



if __name__ == '__main__':

    products = Products()
    products.append(ProductsElement("Редиска", 250, "https://rediska.com"))
    products.append(ProductsElement("Груша", 32.805, "https://grusha.ru"))
    products.append(ProductsElement("Корнишон", 32.805, "https://kornishon.en"))

    print(products)

    render = DataRenderer()
    #
    render.render(products, DataStrFormat.WIDE)


    pr = products.getProductsElementByName("Груша")
    products.remove(pr)

    print()

    render.render(products, DataStrFormat.SHORT)

    products2 = Products()
    products2.append(ProductsElement("Редиска2", 250, "https://rediska.com"))
    products2.append(ProductsElement("Груша2", 32.805, "https://grusha.ru"))


    products3 = Products()
    products3.append(ProductsElement("3Редиска", 250, "https://rediska.com"))
    products3.append(ProductsElement("3Груша", 32.805, "https://grusha.ru"))
    products3.append(ProductsElement("3Корнишон", 32.805, "https://kornishon.en"))


    print('\n\nproducts')
    render.render(products)
    print('\n\nproducts2')
    render.render(products2)

    # pr = products + ProductsElement("Редиска3", 250, "https://rediska.com") + ProductsElement("Редиска4", 250, "https://rediska.com") + products2
    # pr = products2 + products + ProductsElement("Груша6", 32.805, "https://grusha.ru") + products + ProductsElement("Груша-хрюша", 32.805, "https://grusha.ru")
    # pr = products2 + products + ProductsElement("Груша6", 32.805, "https://grusha.ru") + 2
    pr = products2 + products + products3

    # pr = products2 + products
    # pr = products2.__add__(products)

    print('\n\npr = products2 + products + products3')
    render.render(pr)

    pr2 = products3 + products + products2
    print('\n\npr2 = products3 + products + products2')
    render.render(pr2)

    print()
    print()
    p5 = products
    render.render(p5)
    print()
    print()
    p5 += products3
    render.render(p5)
    p5 += products2
    print()
    print()
    render.render(p5)






