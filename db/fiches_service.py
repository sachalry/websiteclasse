from db.db import get_db

def get_fiches():
    db = get_db()
    fiches = db.execute("SELECT * FROM fiches").fetchall()
    db.close()

    if fiches is None:
        return []
    
    return fiches

def get_fiche_by_id(id_fiche):
    db = get_db()
    fiche = db.execute(
        "SELECT * FROM fiches WHERE id_fiche = ?",
        (id_fiche,)
    ).fetchone()
    db.close()
    return fiche

def add_fiche(title, auteur, id_matiere, date):
    db = get_db()
    db.execute(
        "INSERT INTO fiches (title, auteur, id_matiere, date) VALUES (?, ?, ?, ?)",
        (title, auteur, id_matiere, date)
    )
    id_fiche = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.commit()
    db.close()
    return id_fiche

def delete_fiche_by_id(id_fiche):
    db = get_db()
    db.execute(
        "DELETE FROM fiches WHERE id_fiche = ?",
        (id_fiche,)
    )
    db.commit()
    db.close()

def get_fiches_by_matiere(id_matiere):
    db = get_db()
    fiches = db.execute(
        "SELECT * FROM fiches WHERE id_matiere = ?",
        (id_matiere,)
    ).fetchall()
    db.close()

    if fiches is None:
        return []
    
    return fiches

def like_fiche(id_fiche):
    db = get_db()
    db.execute(
        "UPDATE fiches SET nb_likes = nb_likes + 1 WHERE id_fiche = ?",
        (id_fiche,)
    )
    db.commit()
    db.close()

def unlike_fiche(id_fiche):
    db = get_db()
    db.execute(
        "UPDATE fiches SET nb_likes = nb_likes - 1 WHERE id_fiche = ? AND nb_likes > 0",
        (id_fiche,)
    )
    db.commit()
    db.close()