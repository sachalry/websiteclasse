import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)
print(os.path.join(BASE_DIR, "static"))
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# affichage des pages
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/cours/", methods=["GET"])
def cours():
    return render_template("cours/index.html")

@app.route("/revision/", methods=["GET"])
def revision():
    return render_template("revision/index.html")

# API endpoint to get list of images
@app.route("/teste/images", methods=["GET"])
def teste_images():
    return render_template("cours/teste.html")

@app.route("/api/images", methods=["GET"])
def images():
    images = os.listdir(UPLOAD_FOLDER)
    return jsonify(images)

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

if __name__ == "__main__":
    app.run(debug=True)
