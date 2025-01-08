document.getElementById('editMovieForm').addEventListener('submit', function(event) {
    const title = document.getElementById('title').value.trim();
    const genre = document.getElementById('genre').value.trim();
    const year = document.getElementById('year').value.trim();
    const actors = document.getElementById('actors').value.trim();
    const director = document.getElementById('director').value.trim();

    if (!title || !genre || !year || !actors || !director) {
        alert("Wszystkie pola są wymagane!");
        event.preventDefault(); 
        return;
    }

    console.log("Wysyłanie formularza z danymi:", { title, genre, year, actors, director });
});