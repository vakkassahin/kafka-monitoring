# Temel imaj olarak python:3.9-alpine kullan
FROM python:3.9-alpine

# Çalışma dizinini /app olarak belirle
WORKDIR /app

# Gereksinimler dosyasını imaja kopyala
COPY requirements.txt .

# Gereksinimleri kur
RUN pip install -r requirements.txt

# Uygulama kodlarını imaja kopyala
COPY app.py .

# Uygulamayı çalıştıracak komutu belirle
CMD ["python", "app.py"]

# Uygulamanın dinleyeceği portu belirle
EXPOSE 5000
