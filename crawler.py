import requests
import re
from content import Content


class Crawler:

    def __init__(self, url) -> None:
        self.url = url
        self.boutique_products = []
        self.print_content = Content()


    def get_json(self, page):
        """Gets the websites product json format
        """
        try:
            response = requests.get(f"{self.url}products.json?limit=250&page={page}", timeout=7)
        except requests.exceptions.RequestException:
            return None
        if response.status_code == 200 and len(response.json()["products"]) > 0:
            data = response.json()["products"]
            return data
        else:
            return


    def parse_json(self, json_data):
        """Parses the json and return back the products and the price
        """
        for product in json_data:
            try:
                product_name = product["title"]
                for var in product["variants"]:
                    product_price = var["price"]
                    item = {
                        "product_name": product_name,
                        "product_price": product_price
                    }
            except TypeError:
                print("Sorry! Website is not available")
                pass
            self.boutique_products.append(item)
        return self.boutique_products


    def search(self):
        """Searches a given website for the product requested for and records all products in the pages found
        """
        products_name = [key["product_name"] for key in self.boutique_products]
        products_price = [key["product_price"] for key in self.boutique_products]

        end = False

        search = input("\nWhat product are you looking for? ")

        word_pattern = re.compile(r"[a-z]+\s[a-z]+")
        word_match = word_pattern.search(search)

        # To end the loop
        while not end:
            if search == "q" or search == "quit":
                return True

        if word_match:
            search = search.split()

            pattern = re.compile(r"""(
            [A-Za-z\s]*                             # Any word before the search word
            ({search1}*\s?[search2]*)               # The search containing two or more words
            [A-Za-z\s]*                             # Any word after the search word
            )""".format(search1=search[0], search2=search[1]), re.VERBOSE | re.I)

        else:   
            
            pattern = re.compile(r"""(
                [A-Za-z\s]*             # Any word before the search word
                ({search}?)             # The search word
                [A-Za-z\s]*             # Any word after the search word
                )""".format(search=search), re.VERBOSE | re.I)

        product_list = filter(pattern.findall, products_name)

        store_list = [f"{self.print_content.print_product(product, products_price[products_name.index(product)])}" for product in product_list]

        return store_list
       