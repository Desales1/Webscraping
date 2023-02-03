CREER LES BASES DE DONNEES DANS PGADMIN 4 DEPUIS JUPYTER

 pip install psycopg2

import psycopg2


# Établir une connexion à la base de données
conn = psycopg2.connect(
  host="localhost",
    database="Youn_R",
    user="postgres",
    password="'password'"
)
cursor = conn.cursor()


create_table_categorie = """
CREATE TABLE categorie (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    description TEXT
);
"""
cursor.execute(create_table_categorie)


create_table_marque = """
CREATE TABLE marque (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    description TEXT
);
"""
cursor.execute(create_table_marque)


create_table_produit = """
CREATE TABLE produit (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    id_categorie INTEGER NOT NULL,
    id_marque INTEGER NOT NULL,
    FOREIGN KEY (id_categorie) REFERENCES categorie(id),
    FOREIGN KEY (id_marque) REFERENCES marque(id)
);
"""
cursor.execute(create_table_produit)



create_table_avis = """
CREATE TABLE avis (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    note INTEGER NOT NULL,
    id_produit INTEGER NOT NULL,
    FOREIGN KEY (id_produit) REFERENCES produit(id)
);
"""
cursor.execute(create_table_avis)


create_table_commentaire = """
CREATE TABLE commentaire (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    id_produit INTEGER NOT NULL,
    FOREIGN KEY (id_produit) REFERENCES produit(id)
);
"""
cursor.execute(create_table_commentaire)



create_table_tag = """
CREATE TABLE tag (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    description TEXT
);
"""
cursor.execute(create_table_tag)

conn.commit()
conn.rollback()


SCRAPPER LES DONNÉES AJOUTÉ A LA TABLE TAG

import psycopg2
import requests
from bs4 import BeautifulSoup

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="Nopoliceplease2"
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


SCRAPPER LES DONNÉES ET LES AJOUTER A LA TABLE CATEGORIE

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

SCRAPPER LES DONNÉES ET LES AJOUTER À LA TABLE PRODUIT

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
    database="postgres",
    user="postgres",
    password="Nopoliceplease2"
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


