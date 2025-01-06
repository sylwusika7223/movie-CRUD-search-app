# Movie Search Project

To prosta aplikacja webowa umożliwająca użytkownikom wyszukiwanie filmów po tytułach, gatunkach, aktorach czy reżyserach. Jest to aplikacja oferująca CRUD korzystając z nierelacyjnej bazy danych Neo4j oraz frameworka Flask.

## Features
- Wyszukiwanie filmów na podstawie różnych filtrów (tytuł, gatunek, aktor, reżyser).
- Dodawanie filmów.
- Edycja istniejących filmów.
- Usuwanie filmów.

## Requirements
- Python 3.x
- Neo4j (Docker setup available)
- Flask
- Neo4j Python driver
- Docker installed on your machine.
- Docker Compose installed.

## Setup

### 1. Sklonowanie repozytorium
Najpierw sklonuj repozytorium na swoją maszynę i przejdź do katalogu projektu:

git clone https://github.com/sylwusika7223/movie-CRUD-search-app

### 2. Uruchomienie Neo4j za pomocą Dockera
Przejdź do folderu `docker` i uruchom kontener Neo4j:

cd docker
docker-compose up -d

Neo4j zostanie uruchomiony na porcie `7474`, a jego endpoint Bolt na porcie `7687`.

### 3. Sprawdzenie bazy Neo4j
Otwórz swoją przeglądarkę i przejdź pod adres:

http://localhost:7474

Zaloguj się, używając:
- **Username:** `neo4j`
- **Password:** `password`

Aby załadować dane startowe, możesz skopiować  zawartość pliku \docker\init.cypher i uruchomić wszystkie polecenia w konsoli Neo4j pod adresem: http://localhost:7474.


### 4. Uruchomienie backendu Flask

Backend będzie dostępny pod adresem: http://localhost:5000


Domyślna strona wyświetla wszystkie dostępne filmy oraz umożliwia filtrowanie wyników na podstawie tytułu, gatunku, aktorów lub reżyserów. Możesz także:
- **Dodać nowy film.**
- **Zobaczyć szczegóły istniejącego filmu.**
- **Edytować istniejący film.**
- **Usunąć istniejący film.**

### 7. Zatrzymanie kontenerów Docker
Aby zatrzymać kontenery Docker, użyj następującego polecenia w folderze `docker`:

docker-compose down


Gotowe! Twoja aplikacja jest teraz w pełni uruchomiona. 
---