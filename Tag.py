import psycopg2
import requests
from bs4 import BeautifulSoup

conn = psycopg2.connect(
    host="localhost",
    database="Youn_R",
    user="postgres",
    password="'password"
)

cursor = conn.cursor()
url = "https://www.jumia.ci/index/allcategories/"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
categories = soup.find_all("a", class_="-pbm -m -upp -hov-or5")

results = []
for category in categories:
    name = category.text
    results.append({name})

print(results)

for i, category in enumerate(categories, start=1):
    name = category.text
    cursor.execute("INSERT INTO Tag (id, nom) VALUES (%s, %s)", (i, name))

conn.commit()
cursor.close()
conn.close()
