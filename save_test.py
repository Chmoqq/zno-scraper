import requests
from bs4 import BeautifulSoup

r = requests.post("https://zno.osvita.ua/users/znotest/highload/",
                  data={
                      'znotest': 1,
                      'do': 'send_all_serdata'
                  })

data = r.json()
soup = BeautifulSoup(data['result']['quest'], "html.parser")
#print(soup.prettify())

for elem in soup.find_all(class_='question'):
    if 'q-info' in elem.attrs['class']:
        continue
    if 'noborder' in elem.attrs['class']:
        continue

    # Text
    #print(elem.prettify())
    question_text = elem.find(class_='q-txt')
    question_img_src = question_text.find("img")["src"]
    print(question_img_src)

    # Answer
    answers_type = 0
    answers_table = elem.find("table", class_='q-answer')
    if answers_table is not None:
        answers_type = 1

        table_rows = answers_table.find_all("tr")
        print(table_rows)

    # i = 0
    # for elem in answers_table.find_all('th'):
    #
    #     answer_valid = not (table_rows[1].find_all('td')[i].find(class_='ok') is None)
    #     print(elem.text, answer_valid)
    #
    #     i += 1

   # for elem in answers_table.find_all('td'):
   #     print(elem.html)

    #break


# soup = BeautifulSoup(r.text, "html.parser")
#
# # print(soup.prettify())
# for elem in soup.find_all(class_="question"):
#     question_text = elem.find(class_="q-txt")
#     question_img_src = question_text.find("img")["src"]
#     print(question_img_src)
#
#     #
#
#     # break
