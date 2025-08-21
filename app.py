import os
import uuid
import sqlite3
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---------------- Database Setup ----------------
def init_db():
    with sqlite3.connect("db.sqlite3") as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        original_name TEXT,
                        stored_name TEXT,
                        version INTEGER,
                        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
        conn.commit()

init_db()

# Get next version number
def get_next_version(filename):
    with sqlite3.connect("db.sqlite3") as conn:
        c = conn.cursor()
        c.execute("SELECT MAX(version) FROM files WHERE original_name=?", (filename,))
        result = c.fetchone()[0]
        return (result or 0) + 1

# ---------------- Routes ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file uploaded!", "danger")
            return redirect(url_for("index"))
        file = request.files['file']
        if file.filename == "":
            flash("No file selected!", "danger")
            return redirect(url_for("index"))

        original_name = file.filename
        version = get_next_version(original_name)
        stored_name = f"{uuid.uuid4()}_v{version}_{original_name}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], stored_name))

        # Save record in DB
        with sqlite3.connect("db.sqlite3") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO files (original_name, stored_name, version) VALUES (?, ?, ?)",
                      (original_name, stored_name, version))
            conn.commit()

        flash(f"File '{original_name}' uploaded successfully (v{version})!", "success")
        return redirect(url_for("index"))

    # Show all uploaded files
    with sqlite3.connect("db.sqlite3") as conn:
        c = conn.cursor()
        c.execute("SELECT id, original_name, stored_name, version, uploaded_at FROM files ORDER BY uploaded_at DESC")
        files = c.fetchall()

    return render_template("index.html", files=files)

@app.route("/download/<stored_name>")
def download(stored_name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], stored_name, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
