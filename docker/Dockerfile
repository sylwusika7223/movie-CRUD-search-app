# Wybór obrazu Pythona
FROM python:3.9-slim

# Ustalamy katalog roboczy
WORKDIR /app

# Kopiujemy pliki projektu do kontenera
COPY ./backend /app/backend
COPY ./frontend /app/frontend
COPY ./backend/requirements.txt /app/requirements.txt

# Instalujemy zależności
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Eksponujemy port, na którym będzie działać Flask
EXPOSE 5000

# Ustawiamy zmienną środowiskową dla Flask
ENV FLASK_APP=backend/app.py

# Uruchamiamy aplikację Flask
CMD ["flask", "run", "--host=0.0.0.0"]