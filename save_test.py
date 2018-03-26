import requests
import random
from bs4 import BeautifulSoup

r = requests.post("https://zno.osvita.ua/users/znotest/highload/",
                  data={
                      'znotest': random.randint(1, 300),
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

    question_id = int(elem.attrs['id'].replace('q', ''))

    # Text
    print(elem.prettify())
    question_text = elem.find(class_='q-txt')
    question_img_src = question_text.find("img")["src"]
    # print(question_img_src)

    # Answer
    answers_type = 0
    answers_list = [] # ["Some text"] or [1] or [1, 2, 3, 4]
    answer_text = elem.find_all(class_='q-info')
    answers_table = elem.find("table", class_='q-answer')
    if answers_table is not None:
        answers_type = 1

        table_rows_without_heading = answers_table.find_all("tr")[1:]
        for row in table_rows_without_heading:
            current_answer = 0
            for td in row.find_all('td'):
                # warning!!! Это сломается если на одной строке будет больше одного ответа
                if 'ok' in td.find('span').attrs['class']:
                    answers_list.append(current_answer)

                current_answer += 1

        if len(table_rows_without_heading) != len(answers_list):
            raise RuntimeError("Сломалось из-за того, что на одной строке появилось больше одного ответа")
    elif len(answer_text) >= 2 and answer_text[1].find('b') is not None:
        answers_list.append(answer_text[1].find('b').text)

    print("=" * 80)
    print(question_id)
    #print(answer_text)
    print(answers_list)



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
