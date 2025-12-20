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

def add_image_by_id(filename, id_cours):
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