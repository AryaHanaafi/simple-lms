# Gunakan image Python versi 3.10
FROM python:3.10-slim

# Mencegah Python membuat file .pyc dan memastikan output log langsung muncul
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Tentukan folder kerja di dalam container
WORKDIR /app

# Copy file requirements dan install library-nya
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode proyek kita ke dalam container
COPY . /app/