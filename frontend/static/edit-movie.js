document.getElementById('editMovieForm').addEventListener('submit', function(event) {
    // Pobieramy dane z formularza
    const title = document.getElementById('title').value.trim();
    const genre = document.getElementById('genre').value.trim();
    const year = document.getElementById('year').value.trim();
    const actors = document.getElementById('actors').value.trim();
    const director = document.getElementById('director').value.trim();

    // Walidacja formularza
    if (!title || !genre || !year || !actors || !director) {
        alert("Wszystkie pola są wymagane!");
        event.preventDefault(); // Zatrzymanie wysyłania formularza
        return;
    }

    // Jeśli wszystko jest OK, wyświetlamy komunikat debugujący
    console.log("Wysyłanie formularza z danymi:", { title, genre, year, actors, director });
});