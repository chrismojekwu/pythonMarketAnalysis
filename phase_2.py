import csv
import math
from bs4 import BeautifulSoup
from datetime import date
from main import main as single_book, clean_tags, get_html_string

def main():
    html_string = get_html_string("https://books.toscrape.com/catalogue/category/books_1/index.html")
    soup = BeautifulSoup(html_string, "html.parser")
    categories = soup.find("div", {"class": "side_categories"}).find_all("a")
    category_strings = []
    for x in categories:
        category_strings.append(clean_tags(str(x).strip()).strip())

    category_strings = category_strings[1:len(category_strings)]
    catInt = 2
    all_page_paths = []
    all_book_data = []

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
        all_page_paths += page_paths
        catInt+=1
    helpfulInt = 1
    for b in all_page_paths:
        print(helpfulInt, "  Getting data for: ", "https://books.toscrape.com/catalogue" + b)
        all_book_data.append(single_book(False, "https://books.toscrape.com/catalogue" + b))
        helpfulInt+=1

    print("Writing book data to .csv", len(all_book_data))

    fields = all_book_data[0].keys()
    filename = "categoryScrape.csv"

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_book_data)

main()