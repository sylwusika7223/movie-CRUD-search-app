# Wybór obrazu Pythona
FROM python:3.9-slim

# Ustalamy katalog roboczy
WORKDIR /app

# Kopiujemy pliki projektu do kontenera
COPY . .

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Uruchamiamy aplikację
CMD ["python", "backend/app.py"]
