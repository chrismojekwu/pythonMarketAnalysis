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


print("Please input product page url: \n")
productPageUrl = input()
while productPageUrl.startswith("https://") == False:
    print("Please use an https:// url")
    productPageUrl = input()

print("\nFetching HTML... \n") 

page = urlopen(productPageUrl)
html_bytes = page.read()
htmlString = html_bytes.decode("utf-8")
# print(htmlString.strip())

soup = BeautifulSoup(htmlString, "html.parser")

# title
productTitle = clean_tags(str((soup.find("h1")))).strip()

# description
# category
# review rating
# image url

# most other data
thTags = soup.find_all("th")
thString = []
for x in thTags:
    thString.append(clean_tags(str(x)))

tdTags = soup.find_all("td")
tdString = []
for x in tdTags:
    tdString.append(clean_tags(str(x)))

data = []
print("\n", productTitle)
print(thString)
print(tdString)

# create object and write to file




# fields = ["name", "age", "location"]
# filename = "text.csv"

# dict1 = [{"name": "Test 1", "age": "32" , "location": "home"},
#          {"name": "Test 2", "age": "24" , "location": "out"},
#          {"name": "Test 3", "age": "54" , "location": "friends couch"},]
# 
# with open(filename, 'w') as csvfile:
#     # creating a csv dict writer object
#     writer = csv.DictWriter(csvfile, fieldnames=fields)
#     writer.writeheader()
#     writer.writerows(dict1)