from neo4j_database import get_neo4j_session

def add_movie_service(title, genre, year, actors, director):
    session = get_neo4j_session()

    # Tworzymy lub łączymy węzeł filmu
    movie_query = """
    MERGE (m:Movie {title: $title, genre: $genre, year: $year})
    """
    session.run(movie_query, {"title": title, "genre": genre, "year": year})

    # Sprawdzamy i łączymy aktorów
    for actor_name in actors:
        actor_query = """
        MERGE (a:Actor {name: $actor_name})
        MERGE (a)-[:ACTED_IN]->(m)
        """
        session.run(actor_query, {"actor_name": actor_name})

    # Sprawdzamy i łączymy reżysera
    director_query = """
    MERGE (d:Director {name: $director})
    MERGE (d)-[:DIRECTED_BY]->(m)
    """
    session.run(director_query, {"director": director})

    # Dodajemy gatunek (jeśli jest wymagane)
    genre_query = """
    MERGE (g:Genre {name: $genre})
    MERGE (g)-[:IN_GENRE]->(m)
    """
    session.run(genre_query, {"genre": genre})

    session.close()
    return {'success': True}




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


def movie_exists(title, director):
    query = """
    MATCH (m:Movie)-[:DIRECTED_BY]->(d:Director)
    WHERE m.title = $title AND d.name = $director
    RETURN m
    """
    session = get_neo4j_session()
    result = session.run(query, {"title": title, "director": director})

    # Upewnij się, że nie próbujesz wielokrotnie przetwarzać wyniku
    movie = result.single()  # Tu sprawdzamy pierwszy wynik
    session.close()

    return movie is not None


