import os
import json
from flask import Flask, render_template, send_from_directory, jsonify
from urllib.parse import quote, unquote

app = Flask(__name__)

# Cartella dove sono già presenti le immagini estratte dai PDF
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "images")

# ----------------------------------------------------
# ROUTE PRINCIPALE – LISTA “PDF” (cartelle di immagini)
# ----------------------------------------------------
@app.route("/")
def index():
    pdf_folders = [
        {
            "name": f,
            "url_name": quote(f),
            "display_name": f.replace("_", " ").title()
        }
        for f in sorted(os.listdir(IMAGE_DIR))
        if os.path.isdir(os.path.join(IMAGE_DIR, f))
    ]
    return render_template("index.html", pdf_files=pdf_folders)

# ----------------------------------------------------
# ROUTE PER VISUALIZZARE LE IMMAGINI
# ----------------------------------------------------
@app.route("/view/<pdf_name>")
def view_pdf(pdf_name):
    pdf_name = unquote(pdf_name)  # decodifica URL
    folder_path = os.path.join(IMAGE_DIR, pdf_name)

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        available = os.listdir(IMAGE_DIR)
        return f"Cartella '{pdf_name}' non trovata. Cartelle disponibili: {available}", 404

    # Prende tutte le immagini già presenti nella cartella
    images = sorted([img for img in os.listdir(folder_path) if img.lower().endswith((".jpg", ".jpeg", ".png"))])
    return render_template("viewer.html", pdf_name=pdf_name, images=images)

# ----------------------------------------------------
# ROUTE PER L'INDICE DI RICERCA
# ----------------------------------------------------
@app.route("/search_index/<pdf_name>")
def search_index(pdf_name):
    pdf_name = unquote(pdf_name)
    index_path = os.path.join(IMAGE_DIR, pdf_name, "search_index.json")
    if not os.path.exists(index_path):
        return jsonify({"pages": {}})
    with open(index_path, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

# ----------------------------------------------------
# ROUTE STATIC PER LE IMMAGINI
# ----------------------------------------------------
@app.route('/static/images/<folder>/<filename>')
def serve_image(folder, filename):
    folder_path = os.path.join(IMAGE_DIR, folder)
    return send_from_directory(folder_path, filename)

# ----------------------------------------------------
# AVVIO APP (locale)
# ----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8080)

# Export per Vercel
app = app
