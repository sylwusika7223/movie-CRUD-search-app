import os
from flask import Flask, render_template, request, jsonify
from neo4j_database import get_neo4j_session

# Konfiguracja ścieżek do szablonów i plików statycznych
app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))

# Strona główna
@app.route("/")
def index():
    return render_template("index.html")

# Trasa wyszukiwania filmów
@app.route("/search", methods=["GET"])
def search():
    title = request.args.get("title", "").strip()
    genre = request.args.get("genre", "").strip()
    actor = request.args.get("actor", "").strip()
    director = request.args.get("director", "").strip()

    # Debugging
    print(f"Received search parameters: Title={title}, Genre={genre}, Actor={actor}, Director={director}")

    # Przekazanie parametrów do zapytania
    query_params = []
    if title:
        query_params.append(f"Title: {title}")
    if genre:
        query_params.append(f"Genre: {genre}")
    if actor:
        query_params.append(f"Actor: {actor}")
    if director:
        query_params.append(f"Director: {director}")

    # Wywołanie zapytania do Neo4j
    results, query_params = search_movies(title, genre, actor, director)

    # Jeśli są wyniki, zwróć je razem z parametrami wyszukiwania
    if results:
        return jsonify({
            "results": results,
            "query_params": query_params  # Upewniamy się, że query_params są zwrócone
        })

    else:
        return jsonify({
            "results": [],
            "message": "Brak wyników dla podanych filtrów."
        })


def search_movies(title=None, genre=None, actor=None, director=None):
    query = """
    MATCH (f:Movie)-[:ACTED_IN]->(a:Actor), (f)-[:DIRECTED_BY]->(d:Director)
    WHERE 1 = 1
    """
    
    parameters = {}
    query_params = []

    # Warunki dodane do zapytania, jeśli odpowiedni parametr został podany

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

    session = get_neo4j_session()
    result = session.run(query, parameters)

    print(f"Zapytanie: {query}")
    print(f"Parametry: {parameters}")

    # Przetwarzanie wyników zapytania
    movies = [{"title": record["title"], "genre": record["genre"], 
               "director": record["director"], "actors": record["actors"]} for record in result]
    
    # Zamknięcie sesji
    session.close()
    
    return movies, query_params



if __name__ == "__main__":
    app.run(debug=True)
