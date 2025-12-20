import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from db.matiere_service import get_matieres, get_matiere_by_id, add_matiere_by_id, delete_matiere_by_id
from db.cours_service import get_cours_by_matiere, get_cours_by_id, add_cours_by_id, delete_cours_by_id
from db.images_service import get_images_by_cours

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.secret_key = "ce965c66ee6832ba08b69af2a550d78de8f9988c80cb31255d0a24533a2d3987"

print(os.path.join(BASE_DIR, "static"))
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.template_filter('format_date')
def format_date(value, format="%d/%m/%Y"):
    from datetime import datetime
    return datetime.strptime(value, "%Y-%m-%d").strftime(format)

# affichage des pages
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/cours/", methods=["GET"])
def cours():
    cours = {}
    matieres = get_matieres()
    for matiere in matieres:
        cours[matiere["id_matiere"]] = get_cours_by_matiere(matiere["id_matiere"])
        
    return render_template("cours/index.html" , matieres=matieres, cours=cours)

@app.route("/cours/matiere/<int:id_matiere>", methods=["GET"])
def matiere(id_matiere):
    matiere = get_matiere_by_id(id_matiere)
    nom = matiere["nom"]
    cours = get_cours_by_matiere(id_matiere)
    return render_template("cours/matiere.html", name=nom, cours=cours)

@app.route("/cours/cour/<int:id_cours>", methods=["GET"])
def cour(id_cours):
    cours = get_cours_by_id(id_cours)
    images = get_images_by_cours(id_cours)
    return render_template("cours/cour.html", cours=cours, images=images)

@app.route("/revision/", methods=["GET"])
def revision():
    return render_template("revision/index.html")

# API endpoint

@app.route("/api/", methods=["GET"])
def api_index():
    return "Welcome to the API!"

@app.route("/api/images", methods=["GET"])
def images():
    images = os.listdir(UPLOAD_FOLDER)
    return jsonify(images)

# Gestion des images

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")

    if not file or file.filename == "":
        return redirect(url_for("index"))

    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    return redirect(url_for("index"))

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/delete", methods=["POST"])
def delete_image():
    data = request.get_json()
    filename = data.get("filename")

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify(success=True)

    return jsonify(success=False), 404


# Gestion du panel admin

def load_admin() -> dict:
    import json
    with open("admin.json", "r") as f:
        return json.load(f)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin_data = load_admin()
        user = admin_data.get(username)

        if user and check_password_hash(user["password"], password):
            session["user"] = username
            session["is_admin"] = True
            return redirect(url_for("admin"))

        return render_template("admin/login.html", error="Identifiants invalides")

    return render_template("admin/login.html")

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

@app.route("/admin")
@login_required
def admin():
    cours = {}
    matieres = get_matieres()
    for matiere in matieres:
        cours[matiere["id_matiere"]] = get_cours_by_matiere(matiere["id_matiere"])
    return render_template("admin/panel.html", matieres=matieres, cours=cours)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


# Gestion des matières et cours

@app.route("/admin/matiere/add", methods=["POST"])
@login_required
def create_matiere():
    nom = request.form["nom"]
    add_matiere_by_id(nom)
    return redirect(url_for("admin"))

@app.route("/admin/matiere/delete/", methods=["POST"])
@login_required
def delete_matiere():
    id_matiere = request.form["id_matiere"]
    delete_matiere_by_id(id_matiere)
    return redirect(url_for("admin"))

@app.route("/admin/cours/add", methods=["POST"])
@login_required
def create_cours():
    id_matiere = request.form["id_matiere"]
    matiere = get_matiere_by_id(id_matiere)
    images = request.files.getlist("images")
    print(images)
    list_filenames = []
    for image in images:
        if image and allowed_file(image.filename):
            filename = f"{matiere['nom'].replace(' ', '_')}_{secure_filename(image.filename)}"
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            list_filenames.append(filename)

    add_cours_by_id(
        date=request.form["date"],
        contenu=request.form["contenu"],
        auteur=request.form["auteur"],
        images=list_filenames,
        id_matiere=request.form["id_matiere"]
    )
    return redirect(url_for("admin"))

@app.route("/admin/cours/delete/", methods=["POST"])
@login_required
def delete_cours():
    id_cours = request.form["id_cours"]
    delete_cours_by_id(id_cours)
    return redirect(url_for("admin"))

@app.route("/admin/panel/matiere/add", methods=["GET"])
@login_required
def add_matiere_form():
    return render_template("cours/add_matiere.html")

@app.route("/admin/panel/cours/add", methods=["GET"])
@login_required
def add_cours_form():
    matieres = get_matieres()
    return render_template("cours/add_cours.html", matieres=matieres)

@app.route("/admin/panel/matiere/delete", methods=["GET"])
@login_required
def delete_matiere_form():
    matieres = get_matieres()
    return render_template("cours/remove_matiere.html", matieres=matieres)

@app.route("/admin/panel/cours/delete/<int:id_matiere>", methods=["GET"])
@login_required
def delete_cours_form(id_matiere):
    cours = get_cours_by_matiere(id_matiere)
    return render_template("cours/remove_cours.html", cours=cours)

if __name__ == "__main__":
    print(generate_password_hash("admin"))
    app.run(debug=True)
