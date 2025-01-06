import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from movie_service import add_movie_service, edit_movie_service, delete_movie_service, filter_movies, get_movie_by_title, movie_exists, search_movies
from neo4j_database import  get_neo4j_session

# Konfiguracja ścieżek do szablonów i plików statycznych
app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))

# Strona główna
@app.route("/")
def index():
    return render_template("index.html")

# Filtrowanie filmów
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

    results = filter_movies(results)

    return jsonify({
        "results": results,
        "query_params": query_params
    })

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

        # Sprwdzanie, czy dodawany film już istnieje
        if get_movie_by_title(title) is not None:
            print(f"Rendering duplicate_movie_alert.html for movie: {title}")
            return render_template("duplicate_movie_alert.html", title=title)

        add_movie_service(title, genre, year, actors, director)

        return redirect("/")

    return render_template("add-form.html")


@app.route("/movie/<string:movie_title>", methods=["GET"])
def movie_details(movie_title):
    movie = get_movie_by_title(movie_title)
    if movie:
        return render_template("movie-details.html", movie=movie)
    else:
        return "Film nie znaleziony", 404

# Edycja filmu
@app.route("/edit/<string:movie_title>", methods=["GET", "POST"])
def edit_movie(movie_title):
    movie = get_movie_by_title(movie_title)  # Pobieranie szczegółów dot. filmu
    
    if request.method == "POST":
        title = request.form["title"]
        genre = request.form["genre"]
        year = request.form["year"]
        actors = [actor.strip() for actor in request.form["actors"].split(",")]  # Rozdzielanie aktorów po przecinku
        director = request.form["director"]
        
        edit_movie_service(movie_title, title, genre, year, actors, director)
        
        updated_movie = get_movie_by_title(title) 
        return render_template("movie-details.html", movie=updated_movie)
    
    return render_template("edit-movie.html", movie=movie)

# Usuwanie filmu
@app.route("/delete/<string:movie_title>", methods=["DELETE"])
def delete_movie(movie_title):
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
