from flask import jsonify
from neo4j_database import get_neo4j_session

from neo4j_database import get_neo4j_session

def add_movie_service(title, genre, year, actors, director):
    session = get_neo4j_session()

    try:
        # Przetwarzanie danych wejściowych
        title = title.strip()
        genre = genre.strip()
        year = str(year).strip()
        director = director.strip()
        actors = [actor.strip() for actor in actors]

        print(f"Adding movie: {title}, Genre: {genre}, Year: {year}")
        print(f"Actors: {actors}, Director: {director}")

        # Sprawdzamy, czy film już istnieje
        if movie_exists(title, year, director):
            print(f"Movie '{title}' already exists. Skipping creation.")
            return  # Przerwij, jeśli film już istnieje

        # Rozpocznij transakcję
        with session.begin_transaction() as tx:

            # Sprawdzenie, czy parametry są obecne
            if not genre or not year:
                print(f"Brakuje wymaganych parametrów: Gatunek={genre}, Rok={year}")
                return jsonify({"error": "Brak gatunku lub roku!"}), 400

            # Tworzenie węzła filmu z odpowiednimi parametrami
            movie_query = """
            MERGE (m:Movie {title: $title})
            SET m.genre = $genre, m.year = $year
            """
            tx.run(movie_query, {"title": title, "genre": genre, "year": year})

            # Tworzenie reżysera i relacji
            director_query = """
            MERGE (m:Movie {title: $title})
            ON CREATE SET m.genre = $genre, m.year = $year
            MERGE (d:Director {name: $director})
            MERGE (m)-[:DIRECTED_BY]->(d)
            """
            tx.run(director_query, {"director": director, "title": title, "genre": genre, "year": year})


            # Tworzenie gatunku i relacji IN_GENRE
            genre_query = """
            MERGE (g:Genre {name: $genre})
            WITH g
            MATCH (m:Movie {title: $title})
            MERGE (m)-[:IN_GENRE]->(g)
            """
            tx.run(genre_query, {"genre": genre, "title": title})

            # Tworzenie aktorów i relacji ACTED_IN
            for actor_name in actors:
                actor_query = """
                MERGE (a:Actor {name: $actor_name})
                WITH a
                MATCH (m:Movie {title: $title})
                MERGE (a)-[:ACTED_IN]->(m)
                """
                tx.run(actor_query, {"actor_name": actor_name, "title": title})

            # Zatwierdzenie transakcji
            tx.commit()

        print(f"Successfully created movie '{title}' and its relationships.")

    except Exception as e:
        print(f"Error while adding movie: {e}")
    finally:
        session.close()

def edit_movie_service(movie_title, title, genre, year, actors, director):
    session = get_neo4j_session()

    try:
        # Walidacja danych
        if not title or not genre or not year or not actors:
            return {'error': 'Wszystkie pola są wymagane'}, 400

        # Normalizacja danych wejściowych
        actors = [actor.strip().title() for actor in actors]
        director = director.strip().title()

        print(f"Edytowanie filmu: {movie_title}")
        print(f"Nowy tytuł: {title}, Gatunek: {genre}, Rok: {year}, Aktorzy: {actors}, Reżyser: {director}")

        # 1. Zaktualizowanie danych filmu (zmiana tytułu, gatunku, roku)
        query = """
        MATCH (m:Movie)
        WHERE toLower(m.title) = toLower($movie_title)
        SET m.title = $title, m.genre = $genre, m.year = $year
        """
        session.run(query, {"movie_title": movie_title, "title": title, "genre": genre, "year": year})

        # Aktualizacja zmiennej movie_title na nowy tytuł
        movie_title = title

        # 2. Pobranie aktualnych aktorów związanych z filmem
        actor_query = """
        MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
        WHERE toLower(m.title) = toLower($movie_title)
        RETURN a.name AS actor_name
        """
        result = session.run(actor_query, {"movie_title": movie_title})
        current_actors = [record["actor_name"] for record in result]

        # Debugowanie
        print(f"Aktorzy w bazie: {current_actors}")
        print(f"Nowi aktorzy z formularza: {actors}")

        # Ustal, którzy aktorzy zostali usunięci i którzy muszą być dodani
        current_actors_normalized = [actor.strip().lower() for actor in current_actors]
        actors_normalized = [actor.strip().lower() for actor in actors]

        actors_to_remove = [actor for actor in current_actors if actor.strip().lower() not in actors_normalized]
        actors_to_add = [actor for actor in actors if actor.strip().lower() not in current_actors_normalized]

        print(f"Aktorzy do usunięcia: {actors_to_remove}")
        print(f"Aktorzy do dodania: {actors_to_add}")

        # 2.1. Usuwanie powiązań z aktorami, którzy zostali usunięci
        if actors_to_remove:
            actor_remove_query = """
            MATCH (a:Actor)-[r:ACTED_IN]->(m:Movie)
            WHERE toLower(m.title) = toLower($movie_title) AND a.name IN $actors_to_remove
            DELETE r
            """
            session.run(actor_remove_query, {"movie_title": movie_title, "actors_to_remove": actors_to_remove})

        # 2.2. Dodanie nowych aktorów, którzy są w formularzu
        for actor_name in actors_to_add:
            actor_add_query = """
            MATCH (m:Movie)
            WHERE toLower(m.title) = toLower($movie_title)
            MERGE (a:Actor {name: $actor_name})
            MERGE (a)-[:ACTED_IN]->(m)
            """
            session.run(actor_add_query, {"movie_title": movie_title, "actor_name": actor_name})

        # 3. Aktualizacja reżysera
        if director:
            director_query = """
            MATCH (m:Movie)
            WHERE toLower(m.title) = toLower($movie_title)
            OPTIONAL MATCH (m)-[r:DIRECTED_BY]->(d:Director)
            DELETE r
            MERGE (new_director:Director {name: $director})
            MERGE (m)-[:DIRECTED_BY]->(new_director)
            """
            session.run(director_query, {"movie_title": movie_title, "director": director})

        return {'success': True}

    except Exception as e:
        print(f"Błąd podczas edytowania filmu: {e}")
        return {'error': 'Wystąpił błąd podczas edytowania filmu'}, 500
    finally:
        session.close()



def delete_movie_service(movie_title):
    session = get_neo4j_session()
    
    # Usuwanie relacji przed usunięciem węzła
    query = """
    MATCH (m:Movie {title: $movie_title})-[r]-()
    DELETE r
    """
    session.run(query, {"movie_title": movie_title})
    
    # Teraz usunięcie samego filmu
    query = """
    MATCH (m:Movie) WHERE m.title = $movie_title
    DELETE m
    """
    session.run(query, {"movie_title": movie_title})
    session.close()
    
    return {'success': True, 'message': f"Film '{movie_title}' został usunięty."}

def get_movie_by_title(movie_title):
    session = get_neo4j_session()
    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
    WHERE toLower(m.title) = toLower($movie_title)
    OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
    RETURN m.title AS title, m.genre AS genre, m.year AS year, d.name AS director, collect(a.name) AS actors;
    """
    result = session.run(query, {"movie_title": movie_title})
    movie = result.single()
    session.close()

    if movie:
        print(f"Found movie: {movie}")  # Dodajemy logowanie, aby zobaczyć, co zwróciło zapytanie
        return {
            "title": movie["title"],
            "genre": movie["genre"],
            "year": movie["year"],
            "director": movie["director"],
            "actors": movie["actors"] if movie["actors"] is not None else []
        }
    print("Movie not found!")  # Logujemy, jeśli film nie został znaleziony
    return None


def movie_exists(title, year=None, director=None):
    query = """
    MATCH (m:Movie)
    WHERE m.title = $title
      AND ($year IS NULL OR m.year = $year)
      AND ($director IS NULL OR (m)-[:DIRECTED_BY]->(:Director {name: $director}))
    RETURN m
    """
    session = get_neo4j_session()
    parameters = {"title": title, "year": year, "director": director}
    result = session.run(query, parameters)

    movie = result.single()  # Sprawdź pierwszy wynik
    session.close()

    return movie is not None



