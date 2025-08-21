from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
import mysql.connector
from datetime import datetime
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# MySQL Connection with Retry
for i in range(10):
    try:
        db = mysql.connector.connect(
            host="db",
            user="root",
            password="root",
            database="file_versioning"
        )
        cursor = db.cursor()
        print("MySQL connected successfully!")
        break
    except mysql.connector.Error as err:
        print(f"MySQL not ready yet, retrying in 5 sec... ({i+1}/10)")
        time.sleep(5)
else:
    print("Could not connect to MySQL after 10 attempts. Exiting...")
    exit(1)

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

# PDF Preview Route
@app.route('/preview/<path:filename>')
def preview(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# OPTIONAL: If you want to allow direct access via /uploads/<filename>
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

