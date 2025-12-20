from db.db import get_db

def get_matieres():
    db = get_db()
    matieres = db.execute("SELECT * FROM matiere").fetchall()
    db.close()

    if matieres is None:
        return []
    
    return matieres

def get_matiere_by_id(id_matiere):
    db = get_db()
    matiere = db.execute(
        "SELECT * FROM matiere WHERE id_matiere = ?",
        (id_matiere,)
    ).fetchone()
    db.close()
    return matiere

def add_matiere_by_id(nom):
    db = get_db()
    db.execute("INSERT INTO matiere (nom) VALUES (?)", (nom,))
    db.commit()
    db.close()

def delete_matiere_by_id(id_matiere):
    db = get_db()
    db.execute(
        "DELETE FROM matiere WHERE id_matiere = ?",
        (id_matiere,)
    )
    db.commit()
    db.close()

def update_matiere_by_id(id_matiere, nom):
    db = get_db()
    db.execute(
        "UPDATE matiere SET nom = ? WHERE id_matiere = ?",
        (nom, id_matiere)
    )
    db.commit()
    db.close()
