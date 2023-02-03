import psycopg2
import requests
from bs4 import BeautifulSoup

conn = psycopg2.connect(
    host="localhost",
    database="Youn_R",
    user="postgres",
    password="'password'"
)


cursor = conn.cursor()

url = "https://www.jumia.ci/index/allcategories/"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
tags = soup.find_all("a", class_="-gy5 -hov-m -hov-gy8")

for i, tag in enumerate(tags, start=1):
    name = tag.text
    cursor.execute("INSERT INTO Categorie (id, nom) VALUES (%s, %s)", (i, name))

conn.commit()
cursor.close()
conn.close()
