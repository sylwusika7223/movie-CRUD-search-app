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


def edit_movie_service(movie_id, title, genre, year, actors, director):
    session = get_neo4j_session()

    query = """
    MATCH (m:Movie) WHERE ID(m) = $movie_id
    SET m.title = $title, m.genre = $genre, m.year = $year
    """
    session.run(query, {"movie_id": movie_id, "title": title, "genre": genre, "year": year})

    # Update actors and director (this can be customized further)
    actor_query = """
    MATCH (m:Movie)-[r:ACTED_IN]->(a:Actor)
    WHERE ID(m) = $movie_id
    DELETE r
    """
    session.run(actor_query, {"movie_id": movie_id})
    for actor_name in actors:
        actor_query = """
        MATCH (m:Movie) WHERE ID(m) = $movie_id
        MERGE (a:Actor {name: $actor_name})
        MERGE (a)-[:ACTED_IN]->(m)
        """
        session.run(actor_query, {"movie_id": movie_id, "actor_name": actor_name})

    director_query = """
    MATCH (m:Movie)-[r:DIRECTED_BY]->(d:Director)
    WHERE ID(m) = $movie_id
    DELETE r
    MERGE (d:Director {name: $director})
    MERGE (d)-[:DIRECTED_BY]->(m)
    """
    session.run(director_query, {"movie_id": movie_id, "director": director})

    session.close()
    return {'success': True}

def delete_movie_service(movie_id):
    session = get_neo4j_session()
    query = """
    MATCH (m:Movie) WHERE ID(m) = $movie_id
    DELETE m
    """
    session.run(query, {"movie_id": movie_id})
    session.close()
    return {'success': True}

def get_movie_by_id(movie_id):
    session = get_neo4j_session()
    query = """
    MATCH (m:Movie)-[:ACTED_IN]->(a:Actor), (m)-[:DIRECTED_BY]->(d:Director)
    WHERE ID(m) = $movie_id
    RETURN m.title AS title, m.genre AS genre, m.year AS year, d.name AS director, collect(a.name) AS actors
    """
    result = session.run(query, {"movie_id": movie_id})
    movie = result.single()
    session.close()

    if movie:
        return {
            "title": movie["title"],
            "genre": movie["genre"],
            "year": movie["year"],
            "director": movie["director"],
            "actors": movie["actors"]
        }
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



