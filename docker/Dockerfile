# Python
FROM python:3.9-slim

# Katalog roboczy
WORKDIR /app

# Kopia plików projektu do kontenera
COPY ./backend /app/backend
COPY ./frontend /app/frontend
COPY ./backend/requirements.txt /app/requirements.txt

# Zależności
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Port działania aplikacji Flask
EXPOSE 5000

# Zmienna środowiskowa dla Flask
ENV FLASK_APP=backend/app.py

# Uruchomienie aplikacji Flask
CMD ["flask", "run", "--host=0.0.0.0"]