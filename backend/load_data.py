import os
import json
from neo4j_database import get_neo4j_session

def clear_existing_data():
    # Funkcja czyszcząca istniejące dane w bazie
    session = get_neo4j_session()
    # Usuwamy wszystkie węzły i relacje w bazie
    session.run("MATCH (n) DETACH DELETE n")
    session.close()

def load_data():
    clear_existing_data()

    base_path = os.path.dirname(os.path.abspath(__file__))  # Ścieżka do katalogu, w którym znajduje się ten skrypt
    json_file_path = os.path.join(base_path, '..', 'data', 'movies-data.json')  # Ścieżka względna do pliku JSON

    # Zamieniamy ścieżkę na absolutną
    json_file_path = os.path.abspath(json_file_path)

    print(f"Plik JSON: {json_file_path}") 

    # Wczytujemy dane z pliku JSON
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Debugging: Wypisz dane z JSON, aby upewnić się, że są prawidłowe
    print(json.dumps(data, indent=4))

    # Zainicjalizuj sesję z Neo4j
    session = get_neo4j_session()

    # Funkcja do dodawania filmu i powiązań
    def add_movie(movie):
        print(f"Adding movie: {movie['title']}")  # Debugging: Sprawdzamy, który film jest dodawany

        # Tworzymy węzły dla filmu
        session.run("""
        MERGE (m:Movie {title: $title, genre: $genre, year: $year})
        """, title=movie['title'], genre=movie['genre'], year=movie['year'])

        # Tworzymy węzły dla aktorów i relacje z filmem
        for actor in movie['actors']:
            session.run("""
            MERGE (a:Actor {name: $actor})
            MERGE (a)-[:ACTED_IN]->(m)
            """, actor=actor, title=movie['title'])

        # Tworzymy węzeł dla reżysera i relację z filmem
        if movie['director']:  # Sprawdzamy, czy reżyser nie jest pusty
            session.run("""
            MERGE (d:Director {name: $director})
            MERGE (d)-[:DIRECTED_BY]->(m)
            """, director=movie['director'], title=movie['title'])

    # Ładujemy filmy z pliku JSON i dodajemy do bazy danych
    for movie in data['movies']:
        add_movie(movie)

    # Zamykamy sesję
    session.close()
