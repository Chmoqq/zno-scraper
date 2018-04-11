import requests
from bs4 import BeautifulSoup

r = requests.get("https://zno.osvita.ua/mathematics/247/")
# print(r.text)

soup = BeautifulSoup(r.text, "html.parser")

# print(soup.prettify())
for elem in soup.find_all(class_="question"):
    question_text = elem.find(class_="q-txt")
    question_img_src = question_text.find("img")["src"]
    print(question_img_src)

    #

    #break