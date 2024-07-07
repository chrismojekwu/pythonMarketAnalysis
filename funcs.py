import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen

def clean_tags(input):
    result = ""
    in_tag = False
    for i in range (0, len(input)):
        if i > 0 and input[i] == '<':
            break
        elif input[i] == '>':
            in_tag = True
            continue
        if in_tag:
            result += input[i]
    return result

def get_html_string(input):
    page = urlopen(input)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")

def main(commandLine, inputString = ""):
    if commandLine == False:
        productPageUrl = inputString
    else:
        print("Please input product page url: \n")
        productPageUrl = input()
        while productPageUrl.startswith("https://") == False:
            print("Please use an https:// url")
            productPageUrl = input()

        print("\nFetching HTML for a single book... \n") 

    htmlString = get_html_string(productPageUrl)

    soup = BeautifulSoup(htmlString, "html.parser")
    paragraphs = soup.find_all("p")

    # title
    productTitle = clean_tags(str((soup.find("h1")))).strip()
    # description
    productDescription = clean_tags(str(paragraphs[3]))
    # category
    productCategory = clean_tags(str(soup.find("ul").find_all("li")[2].find("a")))
    # review rating
    productRating = paragraphs[2].get("class")[1]
    # image url
    domain = productPageUrl[0:15]
    productImagePath = str(soup.find("img").get("src")[5:len(soup.find("img").get("src"))])

    # other data
    tdTags = soup.find_all("td")
    tdString = []
    for x in tdTags:
        tdString.append(clean_tags(str(x)))

    data = {
        "product_page_url": productPageUrl, 
        "universal_product_code (upc)":  tdString[0],
        "book_title": productTitle,
        "price_including_tax": tdString[3],
        "price_excluding_tax": tdString[2],
        "quantity_available": tdString[5],
        "product_description": productDescription,
        "category": productCategory,
        "review_rating": productRating,
        "image_url": "https://books.toscrape.com" + productImagePath
    }
    
    if commandLine == True: 
        temp = [data]
        fields = temp[0].keys()
        filename = "bookScrape_" + productTitle.replace(" ", "_") + ".csv"
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(temp)
    else:
        return data