import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from movie_service import add_movie_service, edit_movie_service, delete_movie_service, get_movie_by_id, movie_exists
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

    # Wywołanie zapytania do Neo4j
    results, query_params = search_movies(title, genre, actor, director)

    # Jeśli są wyniki, zwróć je razem z parametrami wyszukiwania
    if results:
        return jsonify({
            "results": results,
            "query_params": query_params
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
    
    session = get_neo4j_session()
    result = session.run(query, parameters)

    # Przetwarzamy wynik zapytania
    movies = [{"title": record["title"], "genre": record["genre"], 
               "director": record["director"], "actors": record["actors"]} for record in result]
    
    # Zamknięcie sesji
    session.close()
    
    return movies, query_params


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
        if movie_exists(title, director):
            return render_template("duplicate_movie_alert.html", title=title, director=director)

        # Dodanie filmu do bazy danych
        add_movie_service(title, genre, year, actors, director)

        # Sprawdzanie, czy zapytanie pochodzi z AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"message": "Film dodany pomyślnie!"})

        return redirect("/")

    return render_template("add-form.html")


@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    movie = get_movie_by_id(movie_id)
    return render_template("movie-details.html", movie=movie)

# Route do edytowania filmu
@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    movie = get_movie_by_id(movie_id)  # Get the movie details from DB
    if request.method == "POST":
        title = request.form["title"]
        genre = request.form["genre"]
        year = request.form["year"]
        actors = request.form["actors"].split(",")
        director = request.form["director"]
        edit_movie_service(movie_id, title, genre, year, actors, director)
        return redirect(url_for('movie_details', movie_id=movie_id))
    return render_template("edit-movie.html", movie=movie)

# Route do usuwania filmu
@app.route("/delete/<int:movie_id>", methods=["POST"])
def delete_movie(movie_id):
    delete_movie_service(movie_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
