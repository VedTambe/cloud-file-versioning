```markdown
# ☁️ Cloud File Versioning

A simple **Flask** web application with **MySQL** backend that allows users to upload files with automatic versioning, preview PDFs, and view file history — all powered by **Docker Compose** for easy deployment!

---

## 🚀 Features

- Upload files with automatic version control
- View all uploaded files with latest versions
- Preview PDF files directly in the browser
- Track and view version history of each file
- Easy to deploy using Docker and Docker Compose

---

## 🛠️ Tech Stack

| Technology      | Version          |
|-----------------|------------------|
| Python (Flask)  | 3.9+             |
| MySQL           | 5.7+             |
| Docker          | Latest           |
| Docker Compose  | Latest           |
| Frontend        | HTML, CSS (Bootstrap-like styling) |

---

## 📁 Project Structure

```

cloud-file-versioning/
├── app/
│   ├── app.py               # Flask application
│   ├── templates/           # HTML templates (index, history, preview)
│   ├── static/              # Static files (CSS)
│   └── uploads/             # Folder to store uploaded files
├── docker-compose.yml       # Docker Compose config
├── Dockerfile               # Dockerfile for Flask app
└── README.md                # This file

````

---

## ⚙️ Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/VedTambe/cloud-file-versioning.git
cd cloud-file-versioning
````

---

### Step 2: Create Uploads Directory

The app needs a directory to save uploaded files:

```bash
mkdir -p app/uploads
```

---

### Step 3: Run with Docker Compose

Build and start the app with one command:

```bash
sudo docker-compose up --build -d
```

This will start two containers:

* **MySQL database** on port `3306`
* **Flask web app** on port `5000`

---

### Step 4: Access the Application

Open your browser and go to:

```
http://localhost:5000
```

Or if running on a remote server (like AWS EC2), use your server's public IP:

```
http://your-server-ip:5000
```

---

## 🐳 Deploying on AWS EC2 (Ubuntu)

Follow these quick steps to deploy the app on an EC2 instance:

1. **Launch Ubuntu EC2 instance** with security group opening ports 22, 5000, and 3306 (optional).

2. **SSH into your EC2:**

   ```bash
   ssh -i /path/to/key.pem ubuntu@your-ec2-ip
   ```

3. **Install Docker & Docker Compose:**

   ```bash
   sudo apt update
   sudo apt install -y docker.io
   sudo systemctl start docker
   sudo systemctl enable docker

   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   docker-compose --version
   ```

4. **Clone repo & create uploads folder:**

   ```bash
   git clone https://github.com/VedTambe/cloud-file-versioning.git
   cd cloud-file-versioning
   mkdir -p app/uploads
   ```

5. **Run Docker Compose:**

   ```bash
   sudo docker-compose up --build -d
   ```

6. **Open your browser:**

   ```
   http://your-ec2-ip:5000
   ```

---

## ⚠️ Troubleshooting

* **File upload errors?**
  Make sure `app/uploads` directory exists and has write permissions.

* **Ports not accessible?**
  Check your firewall and EC2 security group rules to open port 5000.

* **Database connection issues?**
  Verify MySQL container is running and `db` service name matches in `app.py`.

---

## 📝 License

MIT License © VedTambe

---

Made with ❤️ by VedTambe

```
