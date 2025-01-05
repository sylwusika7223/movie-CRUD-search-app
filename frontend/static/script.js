document.addEventListener('DOMContentLoaded', function() {
    const searchBar = document.getElementById('searchBar');
    const resultsDiv = document.getElementById('results');
    const filterInfo = document.getElementById('filterInfo');
    const selectedFilters = document.getElementById('selectedFilters');
    const resultsTableBody = document.querySelector('#resultsTable tbody');
    const searchFormTop = document.getElementById('searchFormTop');
    const resetFiltersButton = document.getElementById('resetFilters'); // Przyciski resetu

    // Ładowanie wyników bez filtrów po załadowaniu strony
    fetchResults();

    searchFormTop.addEventListener('submit', function(event) {
        event.preventDefault();
        handleSearch();
    });

    resetFiltersButton.addEventListener('click', function() {
        resetSearchForm();
        fetchResults(); // Ładowanie danych bez filtrów
    });

    function handleSearch() {
        const title = document.getElementById('titleTop').value.trim();
        const genre = document.getElementById('genreTop').value.trim();
        const actor = document.getElementById('actorTop').value.trim();
        const director = document.getElementById('directorTop').value.trim();

        console.log(`Submitting search with parameters: Title=${title}, Genre=${genre}, Actor=${actor}, Director=${director}`);

        const url = `/search?title=${encodeURIComponent(title)}&genre=${encodeURIComponent(genre)}&actor=${encodeURIComponent(actor)}&director=${encodeURIComponent(director)}`;
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                resultsTableBody.innerHTML = ''; 
                filterInfo.style.display = data.query_params.length > 0 ? 'block' : 'none';
                selectedFilters.textContent = `Wybrane filtry: ${data.query_params.join(', ')}`;

                if (data.results.length > 0) {
                    data.results.forEach(movie => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${movie.title || "Brak danych"}</td>
                            <td>${movie.genre || "Brak danych"}</td>
                            <td>${movie.director || "Brak danych"}</td>
                            <td>${movie.actors && movie.actors.length > 0 ? movie.actors.join(', ') : "Brak danych"}</td>
                            <td class="action-buttons">
                                <button class="editButton" data-movie-title="${movie.title}">Edytuj</button>
                                <button class="detailsButton" data-movie-title="${movie.title}">Szczegóły</button>
                                <button class="deleteButton" data-movie-title="${movie.title}">Usuń</button>
                            </td>
                        `;
                        resultsTableBody.appendChild(row);
                    });

                    // Dodanie eventów do przycisków edycji i usuwania
                  document.querySelectorAll('.editButton').forEach(button => {
                        button.addEventListener('click', function() {
                            const movieTitle = this.getAttribute('data-movie-title'); // Pobieramy tytuł filmu
                            console.log(`Redirecting to edit page with title: ${movieTitle}`);
                            window.location.href = `/edit/${encodeURIComponent(movieTitle)}`;
                        });
                    });

                    document.querySelectorAll('.detailsButton').forEach(button => {
                        button.addEventListener('click', function() {
                            const movieTitle = this.getAttribute('data-movie-title'); // Pobieramy tytuł filmu
                            console.log(`Redirecting to details page with title: ${movieTitle}`);
                            window.location.href = `/movie/${encodeURIComponent(movieTitle)}`;
                        });
                    });

                    document.querySelectorAll('.deleteButton').forEach(button => {
                        button.addEventListener('click', function() {
                            const movieTitle = this.getAttribute('data-movie-title'); // Pobieramy tytuł filmu
                            console.log(`Preparing to delete movie with title: ${movieTitle}`); // Debugging line
                            if (confirm("Czy na pewno chcesz usunąć film?")) {
                                fetch(`/delete/${encodeURIComponent(movieTitle)}`, {
                                    method: 'DELETE',
                                    headers: {
                                        'Content-Type': 'application/json' // Dodanie nagłówka
                                    }})
                                    .then(response => {
                                        if (response.ok) {
                                            console.log("Film usunięty pomyślnie");
                                            window.location.href = "/index"; // Przekierowanie na stronę główną
                                        }
                                    });
                            }
                        });
                    });

                    

                } else {
                    const row = document.createElement('tr');
                    row.innerHTML = '<td colspan="5">Brak wyników dla podanych filtrów.</td>';
                    resultsTableBody.appendChild(row);
                }
            })
            .catch(error => console.error('Błąd:', error));
    }

    function resetSearchForm() {
        document.getElementById('titleTop').value = '';
        document.getElementById('genreTop').value = '';
        document.getElementById('actorTop').value = '';
        document.getElementById('directorTop').value = '';
    }

    // Funkcja do pobierania wyników bez filtrów
    function fetchResults() {
        const url = '/search'; // Bez parametrów, żeby pobrać wszystkie wyniki
        fetch(url)
            .then(response => response.json())
            .then(data => {
                filterInfo.style.display = 'none'; // Ukrywanie informacji o filtrach, gdy brak filtrów
                resultsTableBody.innerHTML = ''; // Wyczyść tabelę przed dodaniem nowych wyników
                if (data.results.length > 0) {
                    data.results.forEach(movie => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${movie.title || "Brak danych"}</td>
                            <td>${movie.genre || "Brak danych"}</td>
                            <td>${movie.director || "Brak danych"}</td>
                            <td>${movie.actors && movie.actors.length > 0 ? movie.actors.join(', ') : "Brak danych"}</td>
                            <td class="action-buttons">
                                <button class="editButton" data-movie-title="${movie.title}">Edytuj</button>
                                <button class="detailsButton" data-movie-title="${movie.title}">Szczegóły</button>
                                <button class="deleteButton" data-movie-title="${movie.title}">Usuń</button>
                            </td>
                        `;
                        resultsTableBody.appendChild(row);
                    });

                    // Dodanie eventów do przycisków edycji i usuwania
                  document.querySelectorAll('.editButton').forEach(button => {
                        button.addEventListener('click', function() {
                            const movieTitle = this.getAttribute('data-movie-title'); // Pobieramy tytuł filmu
                            console.log(`Redirecting to edit page with title: ${movieTitle}`);
                            window.location.href = `/edit/${encodeURIComponent(movieTitle)}`;
                        });
                    });

                    document.querySelectorAll('.detailsButton').forEach(button => {
                        button.addEventListener('click', function() {
                            const movieTitle = this.getAttribute('data-movie-title'); // Pobieramy tytuł filmu
                            console.log(`Redirecting to details page with title: ${movieTitle}`);
                            window.location.href = `/movie/${encodeURIComponent(movieTitle)}`;
                        });
                    });

                    document.querySelectorAll('.deleteButton').forEach(button => {
                        button.addEventListener('click', function() {
                            const movieTitle = this.getAttribute('data-movie-title'); // Pobieramy tytuł filmu
                            console.log(`Preparing to delete movie with title: ${movieTitle}`); // Debugging line
                            if (confirm("Czy na pewno chcesz usunąć film?")) {
                                console.log(`${encodeURIComponent(movieTitle)}`);
                                fetch(`/delete/${encodeURIComponent(movieTitle)}`, {
                                    method: 'DELETE',
                                    headers: {
                                        'Content-Type': 'application/json' // Dodanie nagłówka
                                    }})
                                    .then(response => {
                                        if (response.ok) {
                                            console.log("Film usunięty pomyślnie");
                                            // Możesz teraz odświeżyć widok lub usunąć film z listy bez przeładowania strony
                                            location.reload(); // Lub możesz usunąć dany wiersz z tabeli bez odświeżania całej strony
                                        } else {
                                            console.error("Błąd podczas usuwania filmu");
                                        }
                                    })
                                    .catch(error => {
                                        console.error('Błąd:', error);
                                    });
                            }
                        });
                    });

                } else {
                    const row = document.createElement('tr');
                    row.innerHTML = '<td colspan="5">Brak wyników.</td>';
                    resultsTableBody.appendChild(row);
                }
            })
            .catch(error => console.error('Błąd:', error));
    }

    // Obsługa formularza dodawania filmu
    document.getElementById('addMovieForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Zapobiega standardowemu przesyłaniu formularza
    
        const title = document.getElementById('title').value;
        const genre = document.getElementById('genre').value;
        const year = document.getElementById('year').value;
        const actors = document.getElementById('actors').value;
        const director = document.getElementById('director').value;
    
        // Debugging: Sprawdź dane przed wysłaniem
        console.log(`Form data: Title=${title}, Genre=${genre}, Year=${year}, Actors=${actors}, Director=${director}`);
    
        // Tworzymy dane do wysłania w żądaniu POST
        const formData = new FormData();
        formData.append("title", title);
        formData.append("genre", genre);
        formData.append("year", year);
        formData.append("actors", actors);
        formData.append("director", director);
    
        // Wyślij dane do serwera
        fetch('/add', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Informacja o sukcesie
    
            // Po dodaniu, przeładuj wyniki wyszukiwania (w tym przypadku bez filtrów)
            fetchResults();
        })
        .catch(error => console.error('Błąd:', error));
    }); 
});