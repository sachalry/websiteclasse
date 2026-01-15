from db.db import get_db

def get_images_by_cours(id_cours):
    db = get_db()
    images = db.execute(
        "SELECT * FROM images WHERE id_cours = ?",
        (id_cours,)
    ).fetchall()
    db.close()

    if images is None:
        return []

    return images

def add_image_by_id_cours(filename, id_cours):
    db = get_db()
    db.execute(
        """
        INSERT INTO images (filename, id_cours)
        VALUES (?, ?)
        """,
        (filename, id_cours)
    )
    db.commit()
    db.close()

def delete_images_by_cours(id_cours):
    db = get_db()
    db.execute(
        "DELETE FROM images WHERE id_cours = ?",
        (id_cours,)
    )
    db.commit()
    db.close()

def get_images_by_fiches(id_fiches):
    db = get_db()
    images = db.execute(
        "SELECT * FROM images WHERE id_fiche = ?",
        (id_fiches,)
    ).fetchall()
    db.close()

    if images is None:
        return []

    return images

def add_image_by_id_fiches(filename, id_fiches):
    db = get_db()
    db.execute(
        """
        INSERT INTO images (filename, id_fiche)
        VALUES (?, ?)
        """,
        (filename, id_fiches)
    )
    db.commit()
    db.close()

def delete_images_by_fiches(id_fiches):
    db = get_db()
    db.execute(
        "DELETE FROM images WHERE id_fiches = ?",
        (id_fiches,)
    )
    db.commit()
    db.close()