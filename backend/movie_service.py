from neo4j_database import get_neo4j_session

def search_movies(title=None, genre=None, actor=None, director=None):
    # Zaczynamy budowanie zapytania
    query = """
    MATCH (f:Movie)-[:ACTED_IN]->(a:Actor), (f)-[:DIRECTED_BY]->(d:Director)
    WHERE 1 = 1
    """
    
    parameters = {}
    query_params = []

    # Dodajemy warunki do zapytania, jeśli zostały podane przez użytkownika
    if title:
        query += " AND f.title CONTAINS $title"
        parameters["title"] = title
        query_params.append(f'Tytuł: {title}')
    
    if genre:
        query += " AND f.genre CONTAINS $genre"
        parameters["genre"] = genre
        query_params.append(f'Gatunek: {genre}')
    
    if actor:
        query += " AND a.name CONTAINS $actor"
        parameters["actor"] = actor
        query_params.append(f'Aktor: {actor}')
    
    if director:
        query += " AND d.name CONTAINS $director"
        parameters["director"] = director
        query_params.append(f'Reżyser: {director}')
    
    query += " RETURN f.title AS title, f.genre AS genre, d.name AS director, collect(DISTINCT a.name) AS actors"
    
    # Uruchamiamy zapytanie w bazie danych
    session = get_neo4j_session()
    result = session.run(query, parameters)

    # Przetwarzamy wynik zapytania
    movies = [{"title": record["title"], "genre": record["genre"], 
               "director": record["director"], "actors": record["actors"]} for record in result]
    
    # Zamknięcie sesji
    session.close()
    
    return movies, query_params
