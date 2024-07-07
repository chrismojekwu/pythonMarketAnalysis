import csv
import math
import os
import urllib.request 
from bs4 import BeautifulSoup
from funcs import main as single_book, clean_tags, get_html_string

def main():
    html_string = get_html_string("https://books.toscrape.com/catalogue/category/books_1/index.html")
    soup = BeautifulSoup(html_string, "html.parser")
    categories = soup.find("div", {"class": "side_categories"}).find_all("a")
    category_strings = []
    for x in categories:
        category_strings.append(clean_tags(str(x).strip()).strip())

    category_strings = category_strings[1:len(category_strings)]
    catInt = 2
    category_title = ""

    for y in category_strings:
        url = "https://books.toscrape.com/catalogue/category/books/" + y.lower().replace(" ", "-") + "_" + str(catInt)+ "/index.html"
        print(url)
        html_string = get_html_string(url)
        soup = BeautifulSoup(html_string, "html.parser")
        result_num = clean_tags(str(soup.find_all("strong")[1]))
        product_page_tags = soup.find_all("div", {"class": "image_container"})
        page_paths = []
        category_title = clean_tags(str(soup.find("h1")))

        for x in product_page_tags:
            curr = str(x.find("a").get("href"))
            page_paths.append(curr[8:len(curr)])
        if int(result_num) > 20:
            number_of_pages = math.ceil(int(result_num) / 20)
            current_page = 2
            while current_page <= number_of_pages:
                url2 = "https://books.toscrape.com/catalogue/category/books/" + y.lower().replace(" ", "-") + "_" + str(catInt) + "/page-" + str(current_page) + ".html"
                html_string2 = get_html_string(url2)
                soup2 = BeautifulSoup(html_string2, "html.parser")
                product_page_tags2 = soup2.find_all("div", {"class": "image_container"})
                for z in product_page_tags2:
                    curr = str(z.find("a").get("href"))
                    page_paths.append(curr[8:len(curr)])
                current_page+=1
        
        cat_data = []; 
        for b in page_paths:
            print("Getting data for: ", "https://books.toscrape.com/catalogue" + b)
            cat_data.append(single_book(False, "https://books.toscrape.com/catalogue" + b))

        print("Writing .csv file for category: ", category_title)

        if os.path.exists("/Users/chris/Dev/pythonMarketAnalysis/data") == False:
            os.mkdir("/Users/chris/Dev/pythonMarketAnalysis/data")
        if os.path.exists("/Users/chris/Dev/pythonMarketAnalysis/data/img") == False:
            os.mkdir("/Users/chris/Dev/pythonMarketAnalysis/data/img")

        print("Downloading all book covers for category: ", category_title)

        for c in cat_data:
            urllib.request.urlretrieve(c["image_url"], "/Users/chris/Dev/pythonMarketAnalysis/data/img/" + category_title + "_" + c["book_title"].replace(" ", "_") + "_img.png")
        
        fields = cat_data[0].keys()
        filename = "categoryScrape_" + category_title.replace(" ", "_") + ".csv"
        with open("/Users/chris/Dev/pythonMarketAnalysis/data/" + filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(cat_data)    
        catInt+=1
main()