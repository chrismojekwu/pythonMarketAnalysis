import csv
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
    resultNum = clean_tags(str(soup.find_all("strong")[1]))
    print(soup.find("title"), resultNum)
    catInt+=1

#print(category_strings)
#print(single_book(False, "https://books.toscrape.com/catalogue/shakespeares-sonnets_989/index.html"))