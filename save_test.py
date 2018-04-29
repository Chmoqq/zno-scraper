#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import random
import os
import sqlite3
import re
from bs4 import BeautifulSoup

conn = sqlite3.connect('zno_quests/answers.sqlite')

# Создать таблицу с ответами если её не существует
c = conn.cursor()
c.execute(
    "CREATE TABLE IF NOT EXISTS answers (test_id INTEGER, question_id INTEGER, answer_1 TEXT, answer_2 TEXT, answer_3 TEXT, answer_4 TEXT);")


def download_test(cursor, test_id=random.randint(1, 300)):
    r = requests.post("https://zno.osvita.ua/users/znotest/highload/",
                      data={
                          'znotest': test_id,
                          'do': 'send_all_serdata'
                      })

    data = r.json()
    soup = BeautifulSoup(data['result']['quest'], "html.parser")
    print("=" * 80)
    print("Downloading test #%d" % test_id)

    question_blocks = []
    for elem in soup.find_all(class_='question'):
        if 'q-info' in elem.attrs['class']:
            continue
        if 'noborder' in elem.attrs['class']:
            continue

        question_blocks.append(elem)

    if len(question_blocks) == 0:
        print("No such test: %d" % test_id)
        return

    try:
        os.mkdir("zno_quests/%d" % test_id)
    except:
        pass

    for elem in question_blocks:
        question_id = int(elem.attrs['id'].replace('q', ''))

        # Text
        # print(elem.prettify())
        question_text = elem.find(class_='q-txt')
        # question_img_src = question_text.find("img")["src"]
        question_html = ''.join([str(x) for x in question_text.contents])
        # question_html = ''.join([str(x) for x in question_text.contents])
        if "width" in question_html:
            question_html = re.sub(' (height|width)="(\w+)"', '', question_html)
        question_answers = elem.find(class_="quest col")
        question_html += str(question_answers)

        # Answer
        answers_type = 0
        answers_list = []  # ["Some text"] or [1] or [1, 2, 3, 4]
        answer_text = elem.find_all(class_='q-info')
        answers_table = elem.find("table", class_='q-answer')
        another_answers_table_list = elem.find_all("table", class_='answer')
        another_answers_table = " " if len(another_answers_table_list) < 2 else another_answers_table_list[1]
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
        elif another_answers_table != " ":
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

        # Save to DB
        cursor.execute("INSERT into answers VALUES (?, ?, ?, ?, ?, ?)",
                       [test_id, question_id] + [str(answers_list[x]) if len(answers_list) > x else None for x in
                                                 range(4)])
        with open('zno_quests/%d/%d.html' % (test_id, question_id), 'w') as f:
            if "None" in question_html:
                question_html = re.sub('None', '', question_html)
            f.write(str(question_html))


if __name__ == "__main__":
    c = conn.cursor()

    # download_test(c, 247)

    for x in range(0, 300):
        if x in [266, 267, 268, 269, 276, 270, 271, 274, 275, 272, 273]:
            continue
        download_test(c, x)
    conn.commit()
