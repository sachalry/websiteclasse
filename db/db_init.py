import sqlite3

conn = sqlite3.connect("db/database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS matiere (
    id_matiere INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cours (
    id_cours INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    contenu TEXT NOT NULL,
    auteur TEXT NOT NULL,
    id_matiere INTEGER NOT NULL,
    FOREIGN KEY (id_matiere) REFERENCES matiere(id_matiere)
        ON DELETE CASCADE
)
""")
# create images table
cursor.execute("""
CREATE TABLE IF NOT EXISTS images (
    id_image INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    id_cours INTEGER NOT NULL,
    FOREIGN KEY (id_cours) REFERENCES cours(id_cours)
        ON DELETE CASCADE
)
""")

conn.commit()
conn.close()

print("✅ Base de données initialisée")
