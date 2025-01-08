// Funkcja potwierdzenia usunięcia
document.querySelectorAll('.deleteButton').forEach(button => {
    button.addEventListener('click', function() {
        const movieTitle = this.getAttribute('data-movie-title'); 
        if (confirm("Czy na pewno chcesz usunąć film?")) {
            fetch(`/delete/${encodeURIComponent(movieTitle)}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json' 
                }})
                .then(response => {
                    if (response.ok) {
                        console.log("Film usunięty pomyślnie");
                        window.location.href = "/"; 
                    }
                });
        }
    });
});