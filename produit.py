import requests
import psycopg2
from bs4 import BeautifulSoup

URL = "https://www.jumia.ci/category/"
CATEGORIES = {"Animalerie": 1, "Articles de sport": 2, "Beauté & Hygiène": 3, "Bétail": 4, "Divers": 5,
              "Industriel & Scientifique": 6, "Informatique": 7, "Instruments de musique": 8,
              "Jardin et plein air": 9, "Jeux vidéos & Consoles": 10, "Jouets et Jeux": 11,
              "Livres, Films et Musique": 12, "Maison et bureau": 13, "Mode": 14, "Produits pour bébés": 15,
              "Services": 16, "Supermarché": 17, "Téléphones & Tablettes": 18, "Voiture": 19, "Électronique": 20}

# connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="Youn_Rs",
    user="postgres",
    password="'password'"
)


# create a cursor
cur = conn.cursor()

for CATEGORY, id_categorie in CATEGORIES.items():
    # make a GET request to the URL
    response = requests.get(URL + CATEGORY)

    # parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # find all the article elements on the page
    articles = soup.find_all("article")

    # loop through the articles and insert them into the database
    for article in articles:
        h3 = article.find("h3")
        if h3:
            name = h3.get_text().strip()
            # insert the product into the database
            cur.execute("INSERT INTO produit (nom, description, id_categorie) VALUES (%s, %s, %s)", (name, None, id_categorie))

# commit the changes
conn.commit()

# close the cursor and the connection
cur.close()
conn.close()
