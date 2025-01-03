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
        const title = document.getElementById('titleTop').value;
        const genre = document.getElementById('genreTop').value;
        const actor = document.getElementById('actorTop').value;
        const director = document.getElementById('directorTop').value;

        console.log(`Submitting search with parameters: Title=${title}, Genre=${genre}, Actor=${actor}, Director=${director}`);

        const url = `/search?title=${encodeURIComponent(title)}&genre=${encodeURIComponent(genre)}&actor=${encodeURIComponent(actor)}&director=${encodeURIComponent(director)}`;
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                // Jeśli nie ma wyników, ukryj informację o filtrach
                if (data.results.length === 0) {
                    filterInfo.style.display = 'none';
                } else {
                    filterInfo.style.display = 'block'; // Jeśli są wyniki, pokaż informację o filtrach
                    if (data.query_params && Array.isArray(data.query_params)) {
                        selectedFilters.textContent = `Wyniki dla: ${data.query_params.join(', ')}`;
                    } else {
                        selectedFilters.textContent = "Brak filtrów.";
                    }
                }

                resultsTableBody.innerHTML = ''; // Wyczyść tabelę przed dodaniem nowych wyników
                if (data.results.length > 0) {
                    data.results.forEach(movie => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${movie.title}</td>
                            <td>${movie.genre}</td>
                            <td>${movie.director}</td>
                            <td>${movie.actors.join(', ')}</td>
                        `;
                        resultsTableBody.appendChild(row);
                    });
                } else {
                    const row = document.createElement('tr');
                    row.innerHTML = '<td colspan="4">Brak wyników dla podanych filtrów.</td>';
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
        const url = '/search';  // Bez parametrów, żeby pobrać wszystkie wyniki
        fetch(url)
            .then(response => response.json())
            .then(data => {
                filterInfo.style.display = 'none'; // Ukrywanie informacji o filtrach, gdy brak filtrów
                resultsTableBody.innerHTML = ''; // Wyczyść tabelę przed dodaniem nowych wyników
                if (data.results.length > 0) {
                    data.results.forEach(movie => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${movie.title}</td>
                            <td>${movie.genre}</td>
                            <td>${movie.director}</td>
                            <td>${movie.actors.join(', ')}</td>
                        `;
                        resultsTableBody.appendChild(row);
                    });
                } else {
                    const row = document.createElement('tr');
                    row.innerHTML = '<td colspan="4">Brak wyników.</td>';
                    resultsTableBody.appendChild(row);
                }
            })
            .catch(error => console.error('Błąd:', error));
    }
});
