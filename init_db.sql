CREATE DATABASE IF NOT EXISTS file_versioning;

USE file_versioning;

CREATE TABLE IF NOT EXISTS files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    version INT,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
