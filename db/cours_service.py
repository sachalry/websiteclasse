from db.db import get_db
from db.images_service import add_image_by_id

def get_cours_by_matiere(id_matiere):
    db = get_db()
    cours = db.execute(
        "SELECT * FROM cours WHERE id_matiere = ? ORDER BY date DESC",
        (id_matiere,)
    ).fetchall()
    db.close()
    return cours

def get_cours_by_id(id_cours):
    db = get_db()
    cours = db.execute(
        "SELECT * FROM cours WHERE id_cours = ?",
        (id_cours,)
    ).fetchone()
    db.close()
    if cours is None:
        return []
    return cours

def add_cours_by_id(date, contenu, auteur, images:list, id_matiere):
    db = get_db()
    db.execute(
        """
        INSERT INTO cours (date, contenu, auteur, id_matiere)
        VALUES (?, ?, ?, ?)
        """,
        (date, contenu, auteur, id_matiere)
    )
    id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.commit()
    db.close()
    for filename in images:
        add_image_by_id(filename, id)

def delete_cours_by_id(id_cours):
    db = get_db()
    db.execute(
        "DELETE FROM cours WHERE id_cours = ?",
        (id_cours,)
    )
    db.commit()
    db.close()

def update_cours(id_cours, date, contenu, auteur):
    db = get_db()
    db.execute(
        """
        UPDATE cours
        SET date = ?, contenu = ?, auteur = ?
        WHERE id_cours = ?
        """,
        (date, contenu, auteur, id_cours)
    )
    db.commit()
    db.close()
