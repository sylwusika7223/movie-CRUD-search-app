from flask import jsonify
from neo4j_database import get_neo4j_session

# Dodawanie filmu
def add_movie_service(title, genre, year, actors, director):
    session = get_neo4j_session()
    try:
        title = title.strip()
        genre = genre.strip()
        year = str(year).strip()
        director = director.strip()
        actors = [actor.strip() for actor in actors]

        # Sprawdzenie czy film już istnieje
        if movie_exists(title, year, director):
            return  

        # Rozpoczęcie transakcji
        with session.begin_transaction() as tx:

            # Sprawdzenie, czy parametry są obecne
            if not genre or not year:
                return jsonify({"error": "Brak gatunku lub roku!"}), 400

            # Tworzenie węzła filmu z odpowiednimi parametrami
            movie_query = """
            MERGE (m:Movie {title: $title})
            SET m.genre = $genre, m.year = $year
            """
            tx.run(movie_query, {"title": title, "genre": genre, "year": year})

            # Tworzenie reżysera i relacji DIRECTED_BY
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

# Edycja filmu
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

        # Zaktualizowanie danych filmu (zmiana tytułu, gatunku, roku)
        query = """
        MATCH (m:Movie)
        WHERE toLower(m.title) = toLower($movie_title)
        SET m.title = $title, m.genre = $genre, m.year = $year
        """
        session.run(query, {"movie_title": movie_title, "title": title, "genre": genre, "year": year})

        # Aktualizacja zmiennej movie_title na nowy tytuł
        movie_title = title

        # Pobranie aktualnych aktorów związanych z filmem
        actor_query = """
        MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
        WHERE toLower(m.title) = toLower($movie_title)
        RETURN a.name AS actor_name
        """
        result = session.run(actor_query, {"movie_title": movie_title})
        current_actors = [record["actor_name"] for record in result]

        #print(f"Aktorzy w bazie: {current_actors}")
        #print(f"Nowi aktorzy z formularza: {actors}")

        # Podział aktorów na tych do usunięcia i do dodania
        current_actors_normalized = [actor.strip().lower() for actor in current_actors]
        actors_normalized = [actor.strip().lower() for actor in actors]

        actors_to_remove = [actor for actor in current_actors if actor.strip().lower() not in actors_normalized]
        actors_to_add = [actor for actor in actors if actor.strip().lower() not in current_actors_normalized]

        #print(f"Aktorzy do usunięcia: {actors_to_remove}")
        #print(f"Aktorzy do dodania: {actors_to_add}")

        # Usuwanie powiązań z aktorami, którzy zostali usunięci
        if actors_to_remove:
            actor_remove_query = """
            MATCH (a:Actor)-[r:ACTED_IN]->(m:Movie)
            WHERE toLower(m.title) = toLower($movie_title) AND a.name IN $actors_to_remove
            DELETE r
            """
            session.run(actor_remove_query, {"movie_title": movie_title, "actors_to_remove": actors_to_remove})

        # Dodanie nowych aktorów, którzy są w formularzu
        for actor_name in actors_to_add:
            actor_add_query = """
            MATCH (m:Movie)
            WHERE toLower(m.title) = toLower($movie_title)
            MERGE (a:Actor {name: $actor_name})
            MERGE (a)-[:ACTED_IN]->(m)
            """
            session.run(actor_add_query, {"movie_title": movie_title, "actor_name": actor_name})

        # Aktualizacja reżysera
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
    
    # Usunięcie filmu
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
        return {
            "title": movie["title"],
            "genre": movie["genre"],
            "year": movie["year"],
            "director": movie["director"],
            "actors": movie["actors"] if movie["actors"] is not None else []
        }
    return None

# Wyszukiwanie
def search_movies(title=None, genre=None, actor=None, director=None):
    query = """
    MATCH (m:Movie)
    OPTIONAL MATCH (m)<-[:ACTED_IN]-(a:Actor)
    OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
    OPTIONAL MATCH (m)-[:IN_GENRE]->(g:Genre)
    WHERE
        ($title IS NULL OR toLower(m.title) CONTAINS toLower($title)) AND
        ($genre IS NULL OR toLower(g.name) CONTAINS toLower($genre)) AND
        ($actor IS NULL OR toLower(a.name) CONTAINS toLower($actor)) AND
        ($director IS NULL OR toLower(d.name) CONTAINS toLower($director))
    RETURN 
        m.title AS title, 
        coalesce(g.name, 'Brak danych') AS genre, 
        coalesce(m.year, 'Brak danych') AS year, 
        coalesce(d.name, 'Brak danych') AS director, 
        collect(DISTINCT a.name) AS actors
    ORDER BY title
    """

    parameters = {
        "title": title if title else None,
        "genre": genre if genre else None,
        "actor": actor if actor else None,
        "director": director if director else None,
    }

    session = get_neo4j_session()
    result = session.run(query, parameters)

    # Debugging: Check the raw results from Neo4j
    results = [record for record in result]

    # Przetwarzanie wyników
    movies = []
    for record in results:
        movies.append({
            "title": record["title"],
            "genre": record["genre"],
            "year": record["year"],
            "director": record["director"],
            "actors": record["actors"] if record["actors"] else ["Brak danych"],
        })

    session.close()
    return movies

def filter_movies(movies):
    return [movie for movie in movies if movie["genre"] != "Brak danych" and movie["director"] != "Brak danych"]

def get_recommendations(movie):
    query = """
    MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
    WHERE toLower(m.title) = toLower($movie_title)
    WITH g
    MATCH (m2:Movie)-[:IN_GENRE]->(g)
    WHERE toLower(m2.title) <> toLower($movie_title)
    MATCH (m2)-[:DIRECTED_BY]->(d:Director)
    OPTIONAL MATCH (m2)-[:ACTED_IN]-(a:Actor)
    RETURN DISTINCT m2.title AS title, 
                    coalesce(g.name, 'Brak danych') AS genre, 
                    coalesce(d.name, 'Brak danych') AS director, 
                    collect(DISTINCT a.name) AS actors
    UNION ALL

    MATCH (m:Movie)-[:DIRECTED_BY]->(d:Director)
    WHERE toLower(m.title) = toLower($movie_title)
    WITH d
    MATCH (m2:Movie)-[:DIRECTED_BY]->(d)
    WHERE toLower(m2.title) <> toLower($movie_title)
    MATCH (m2)-[:IN_GENRE]->(g:Genre)
    OPTIONAL MATCH (m2)-[:ACTED_IN]-(a:Actor)
    RETURN DISTINCT m2.title AS title, 
                    coalesce(g.name, 'Brak danych') AS genre, 
                    coalesce(d.name, 'Brak danych') AS director, 
                    collect(DISTINCT a.name) AS actors
    UNION ALL

    MATCH (m:Movie)-[:ACTED_IN]-(a:Actor)
    WHERE toLower(m.title) = toLower($movie_title)
    WITH COLLECT(a.name) AS actors
    MATCH (m2:Movie)-[:ACTED_IN]-(a2:Actor)
    WHERE toLower(m2.title) <> toLower($movie_title) AND a2.name IN actors
    WITH m2, actors, COLLECT(DISTINCT a2.name) AS actorsList
    MATCH (m2)-[:IN_GENRE]->(g:Genre)
    OPTIONAL MATCH (m2)-[:DIRECTED_BY]->(d:Director)
    RETURN DISTINCT m2.title AS title, 
                    coalesce(g.name, 'Brak danych') AS genre, 
                    coalesce(d.name, 'Brak danych') AS director, 
                    actorsList AS actors
    """
    
    parameters = {
        "movie_title": movie["title"]
    }

    session = get_neo4j_session()
    result = session.run(query, parameters)

    recommendations = []
    seen_titles = set()  # Zestaw, aby przechowywać już przetworzone tytuły

    for record in result:
        # Sprawdzamy, czy tytuł już został dodany
        title = record["title"]
        if title not in seen_titles:
            seen_titles.add(title)
            recommendations.append({
                "title": title,
                "genre": record["genre"],
                "director": record["director"],
                "actors": record["actors"] if record["actors"] else ["Brak danych"]
            })

    session.close()
    print('\n\nRekomendacje: ', recommendations)
    return recommendations


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

    movie = result.single() 
    session.close()

    return movie is not None