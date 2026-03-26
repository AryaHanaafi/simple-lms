# Simple LMS - Django Dockerized

Tugas ini adalah implementasi setup environment development menggunakan Docker untuk proyek Django (Simple LMS) dengan database PostgreSQL.

## 📸 Dokumentasi

### 1. Django Welcome Page (Localhost:8000)
Halaman ini menunjukkan bahwa server Django berjalan dan dapat diakses melalui browser.
![Django Welcome Page](img/django-welcome.png)

### 2. Docker Containers Running
Screenshot di bawah ini menunjukkan bahwa kedua container (`web` dan `db`) berstatus **Up/Running**.
![Docker Containers](img/docker-ps.png)

## 🎯 Learning Objectives
- Memahami containerization dengan Docker.
- Membuat Dockerfile dan docker-compose.yml yang efisien.
- Konfigurasi Django dengan PostgreSQL di dalam Docker.

## 📦 Project Structure
Struktur proyek sesuai dengan instruksi tugas:
```text
simple-lms/
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── requirements.txt
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── README.

🛠️ Cara Menjalankan Project
1. Persiapan: Pastikan Docker Desktop sudah berjalan di latar belakang.
2. Build Container: Jalankan perintah berikut untuk membangun image:
    docker compose up -d --build
3. Migrasi Database: Lakukan migrasi agar tabel PostgreSQL terbuat:
    docker compose run --rm web python manage.py migrate
4. Akses Aplikasi: Buka browser di http://localhost:8000
