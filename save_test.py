import requests
import random
import os
from bs4 import BeautifulSoup


def download_test(test_id=random.randint(1, 300)):
    r = requests.post("https://zno.osvita.ua/users/znotest/highload/",
                      data={
                          'znotest': test_id,
                          'do': 'send_all_serdata'
                      })

    data = r.json()
    soup = BeautifulSoup(data['result']['quest'], "html.parser")
    print("=" * 80)
    print("Downloading test #%d" % test_id)

    try:
        os.mkdir("zno_quests/%d" % test_id)
    except:
        pass

    for elem in soup.find_all(class_='question'):
        if 'q-info' in elem.attrs['class']:
            continue
        if 'noborder' in elem.attrs['class']:
            continue

        question_id = int(elem.attrs['id'].replace('q', ''))

        # Text
        # print(elem.prettify())
        question_text = elem.find(class_='q-txt')
        # question_img_src = question_text.find("img")["src"]
        question_html = question_text.contents[0]

        # Answer
        answers_type = 0
        answers_list = []  # ["Some text"] or [1] or [1, 2, 3, 4]
        answer_text = elem.find_all(class_='q-info')
        answers_table = elem.find("table", class_='q-answer')
        another_answers_table_list = elem.find_all("table", class_='answer')
        another_answers_table = None if len(another_answers_table_list) < 2 else another_answers_table_list[1]
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
        elif another_answers_table is not None:
            for row in another_answers_table.find_all("td"):
                bold_text = row.find('b')
                if bold_text is None:
                    continue

                answers_list.append(str(bold_text.text))
        elif len(answer_text) >= 2 and answer_text[1].find('b') is not None:
            answers_list.append(answer_text[1].find('b').text)

        print("=" * 80)
        print(question_id)
        # print(answer_text)
        print(answers_list)

        with open('zno_quests/%d/%d.html' % (test_id, question_id), 'w') as f:
            f.write(str(question_html))


if __name__ == "__main__":
    download_test()
