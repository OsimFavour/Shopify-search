from crawler import Crawler
import re


def store_search():
    while True:

        URL = input("Please input in this format - Kerrits, fashionnova, jadedldn - e.t.c\nWhat shopify store do you want to track products in? ").lower()
            
        pattern = re.compile(r"(https)?(://)?(www\.)?\w+\.[a-z]*")
        match = pattern.search(URL)
        digit_pattern = re.compile(r"[\d.,-](\s)?")

        space_pattern = re.compile(r"(\W)+")
        space_match = space_pattern.search(URL)
        digit_match = digit_pattern.search(URL)
        if match:
            print("Wrong Match, please use the format given!\n")
        elif digit_match:
            print("Not allowed!\n")
            continue
        elif space_match:
            print("Invalid!\n")
            continue
        else:
            break
    return URL

webpage = store_search()

web_store = Crawler(f"https://{webpage}.com/")

for page in range(1, 25):
    webpage = web_store.get_json(page)
    try:
        web_store.parse_json(webpage) 
    except TypeError:
        pass
    data = web_store.search()
    try:
        for s in data:
            print(s)
    except TypeError:
        break

