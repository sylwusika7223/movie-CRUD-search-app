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

    # Debugging: Print the parameters received in the search
    print(f"Received search parameters: Title={title}, Genre={genre}, Actor={actor}, Director={director}")

    # Wywołanie zapytania do Neo4j
    results = search_movies(title, genre, actor, director)

    # Debugging: Print the results before sending them to frontend
    print(f"Results from Neo4j: {results}")

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

    print(f"Results before filtering: {results}")
    results = filter_movies(results)
    print(f"Results after filtering: {results}")

    print(f"Sending data to frontend: {results}")
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

    # Debugging: Check the parameters being passed
    print(f"Running query with parameters: {parameters}")

    session = get_neo4j_session()
    result = session.run(query, parameters)

    # Debugging: Check the raw results from Neo4j
    results = [record for record in result]
    print(f"Raw Neo4j results: {results}")

    # Przetwarzanie wyników
    movies = []
    for record in results:
        print(f"Processing record: {record}")  # Debugging: Print each record
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
