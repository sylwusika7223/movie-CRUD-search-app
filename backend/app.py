import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from movie_service import add_movie_service, edit_movie_service, delete_movie_service, get_movie_by_title, movie_exists
from neo4j_database import  get_neo4j_session

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

    # Wywołanie zapytania do Neo4j
    results = search_movies(title, genre, actor, director)

    query_params = []
    if title:
        query_params.append(f"Tytuł: {title}")
    if genre:
        query_params.append(f"Gatunek: {genre}")
    if actor:
        query_params.append(f"Aktor: {actor}")
    if director:
        query_params.append(f"Reżyser: {director}")

    # Debugging: Check if results are empty or not
    if not results:
        print("No results found for the given filters")

    results = filter_movies(results)

    return jsonify({
        "results": results,
        "query_params": query_params
    })


# Wywołanie zapytania do Neo4j
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

@app.route("/add", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        title = request.form.get("title")
        genre = request.form["genre"]
        year = request.form["year"]
        actors = request.form["actors"].split(",")
        director = request.form["director"]

        print(f"Received movie data: Title={title}, Genre={genre}, Year={year}, Actors={actors}, Director={director}")

        if not title or not genre or not year or not actors or not director:
            print("One or more fields are missing!")
            return jsonify({"error": "Wszystkie pola muszą być wypełnione!"}), 400

        # Sprawdzamy, czy film już istnieje
        if get_movie_by_title(title) is not None:
            print(f"Rendering duplicate_movie_alert.html for movie: {title}")
            return render_template("duplicate_movie_alert.html", title=title)

        # Dodanie filmu do bazy danych
        add_movie_service(title, genre, year, actors, director)

        # Sprawdzanie, czy zapytanie pochodzi z AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"message": "Film dodany pomyślnie!"})

        return redirect("/")

    return render_template("add-form.html")


@app.route("/movie/<string:movie_title>", methods=["GET"])
def movie_details(movie_title):
    movie = get_movie_by_title(movie_title)
    if movie:
        return render_template("movie-details.html", movie=movie)
    else:
        return "Film nie znaleziony", 404

# Route do edytowania filmu
@app.route("/edit/<string:movie_title>", methods=["GET", "POST"])
def edit_movie(movie_title):
    movie = get_movie_by_title(movie_title)  # Pobierz szczegóły filmu z bazy danych
    print(movie)  # Debugowanie - sprawdź, jakie dane są w obiekcie 'movie'
    
    if request.method == "POST":
        title = request.form["title"]
        genre = request.form["genre"]
        year = request.form["year"]
        actors = [actor.strip() for actor in request.form["actors"].split(",")]  # Rozdzielanie aktorów po przecinku
        director = request.form["director"]
        
        # Zaktualizowanie danych filmu w bazie
        edit_movie_service(movie_title, title, genre, year, actors, director)
        
        # Po zapisaniu zmian, ładujemy zaktualizowane szczegóły filmu
        updated_movie = get_movie_by_title(title)  # Aby pobrać najnowsze dane po edycji
        return render_template("movie-details.html", movie=updated_movie)
    
    # Jeśli metoda GET, przekaż dane do formularza
    return render_template("edit-movie.html", movie=movie)

# Route do usuwania filmu
@app.route("/delete/<string:movie_title>", methods=["DELETE"])
def delete_movie(movie_title):
    print(f"Attempting to delete movie with title: {movie_title}")
    # Usunięcie filmu z bazy
    delete_movie_service(movie_title)
    return jsonify({"message": "Film został usunięty pomyślnie!"}), 200

@app.route('/get_movie_data/<movie_title>', methods=['GET'])
def get_movie_data(movie_title):
    movie = get_movie_by_title(movie_title)
    
    if movie is None:
        return jsonify({"error": "Film not found"}), 404
    
    return jsonify({
        'title': movie['title'],
        'genre': movie['genre'],
        'year': movie['year'],
        'actors': movie['actors'],
        'director': movie['director']
    })

if __name__ == '__main__':
    app.run(debug=True)
