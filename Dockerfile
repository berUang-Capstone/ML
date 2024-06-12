# Gunakan image dasar Python
FROM python:3.9

# Tetapkan direktori kerja
WORKDIR /Api

# Salin requirements.txt dan install dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file aplikasi ke dalam container
COPY . .

# Tetapkan perintah untuk menjalankan aplikasi Flask
CMD ["python", "app.py"]