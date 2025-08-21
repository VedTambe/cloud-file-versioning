from flask import Flask, request, render_template, redirect, url_for
import os
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/uploads'

# MySQL Connection
db = mysql.connector.connect(
    host="db",
    user="root",
    password="root",
    database="file_versioning"
)
cursor = db.cursor()

# Home Page
@app.route('/')
def index():
    cursor.execute("SELECT * FROM files ORDER BY upload_time DESC")
    files = cursor.fetchall()
    return render_template("index.html", files=files)

# File Upload Route
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        cursor.execute("SELECT COUNT(*) FROM files WHERE filename=%s", (filename,))
        count = cursor.fetchone()[0]
        version = count + 1

        cursor.execute("INSERT INTO files(filename, version) VALUES (%s, %s)", (filename, version))
        db.commit()

    return redirect(url_for('index'))

# Version History Route
@app.route('/history/<filename>')
def history(filename):
    cursor.execute("SELECT * FROM files WHERE filename=%s ORDER BY version ASC", (filename,))
    versions = cursor.fetchall()
    return render_template("history.html", filename=filename, versions=versions)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
