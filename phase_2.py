import csv
import math
from bs4 import BeautifulSoup
from main import main as single_book, clean_tags, get_html_string


#single_book(True)
html_string = get_html_string("https://books.toscrape.com/catalogue/category/books_1/index.html")
soup = BeautifulSoup(html_string, "html.parser")
categories = soup.find("div", {"class": "side_categories"}).find_all("a")
category_strings = []
for x in categories:
    category_strings.append(clean_tags(str(x).strip()).strip())

category_strings = category_strings[1:len(category_strings)]

catInt = 2
for y in category_strings:
    url = "https://books.toscrape.com/catalogue/category/books/" + y.lower().replace(" ", "-") + "_" + str(catInt)+ "/index.html"
    print(url)
    html_string = get_html_string(url)
    soup = BeautifulSoup(html_string, "html.parser")
    result_num = clean_tags(str(soup.find_all("strong")[1]))
    product_page_tags = soup.find_all("div", {"class": "image_container"})
    page_paths = []
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
        #break

    print(soup.find("title"), result_num, len(page_paths), page_paths )
    catInt+=1

#print(category_strings)
#print(single_book(False, "https://books.toscrape.com/catalogue/shakespeares-sonnets_989/index.html"))