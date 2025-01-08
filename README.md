# Movie Search Project App

To prosta aplikacja webowa umożliwiająca użytkownikom przejrzenie informacji na temat filmów znajdujących się w grafowej bazie danych Neo4j, w tym: wyszukiwanie filmów po tytułach, gatunkach, aktorach czy reżyserach oraz wyświetlenie szczegółów filmów wraz z rekomendacjami podobnych tytułów. Jest to aplikacja oferująca wykonanie operacji zarządzania filmami (dodawania, edycji, usuwania, wyświetlania) korzystając z nierelacyjnej bazy danych Neo4j oraz frameworka Flask.
Aplikacja udostępnia prosty, przejrzysty interfejs użytkownika do intuicyjnej nawigacji po jej funkcjonalnościach.

## Funkcjonalności
- Wyszukiwanie filmów na podstawie różnych filtrów (tytuł, gatunek, aktor, reżyser).
- Dodawanie filmów.
- Edycja istniejących filmów.
- Usuwanie filmów.
- Oglądanie szczegółów filmów, wraz z wyświetlaniem rekomendacji dot. filmów, które mogą się spodobać użytkownikowi.

## Wymagania
- Python 3.x
- Neo4j (dostępny gotowy plik `docker-compose.yml` dla Dockera)
- Flask
- Neo4j Python driver
- Docker

## Setup

### 1. Sklonowanie repozytorium
Najpierw sklonuj repozytorium na swoją maszynę i przejdź do katalogu projektu:

```bash
git clone https://github.com/sylwusika7223/movie-CRUD-search-app
```

### 2. Uruchomienie Neo4j za pomocą Dockera
Przejdź do folderu `docker` i uruchom kontener Neo4j:

```bash
cd docker
docker-compose up -d
```

Neo4j zostanie uruchomiony na porcie `7474`, a jego endpoint Bolt na porcie `7687`.

### 3. Sprawdzenie bazy Neo4j
Otwórz swoją przeglądarkę i przejdź pod adres:

[http://localhost:7474](http://localhost:7474)

Zaloguj się, używając:
- **Username:** `neo4j`
- **Password:** `password`

Aby załadować dane startowe, możesz skopiować zawartość pliku `\docker\init.cypher` i uruchomić wszystkie polecenia w konsoli Neo4j pod adresem: [http://localhost:7474](http://localhost:7474).

### 4. Uruchomienie backendu Flask
Backend będzie dostępny pod adresem: [http://localhost:5000](http://localhost:5000)

Domyślna strona wyświetla wszystkie dostępne filmy oraz umożliwia filtrowanie wyników na podstawie tytułu, gatunku, aktorów lub reżyserów. Możesz także:
- **Dodać nowy film.**
- **Zobaczyć szczegóły istniejącego filmu.**
- **Edytować istniejący film.**
- **Usunąć istniejący film.**

### 5. Zatrzymanie kontenerów Docker
Aby zatrzymać kontenery Docker, użyj następującego polecenia w folderze `docker`:

```bash
docker-compose down
```

Gotowe! Aplikacja jest teraz w pełni uruchomiona.
---
