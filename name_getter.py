import requests
import sqlite3
from bs4 import BeautifulSoup

r = requests.get("https://zno.osvita.ua/spanish/")

soup = BeautifulSoup(r.text, "html.parser")
conn = sqlite3.connect('zno_quests/answers.sqlite')
c = conn.cursor()

links = soup.find("ul", class_="links")
for elem in links.find_all("li"):
	id = elem.find("a", class_="but")["href"]
	name = elem.find("a", class_="but")["title"]
	link_array = id.split('/')
	zno_id = link_array[len(link_array) - 2] if id.endswith('/') else link_array[len(link_array) - 1]
	print(zno_id)
	print(name)
	c.execute("INSERT into tests VALUES (?, ?, ?)",
					   [zno_id, 11, name])
conn.commit()