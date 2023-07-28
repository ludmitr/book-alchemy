document.getElementById('searchMovieForm').addEventListener('submit', function(e) {
    e.preventDefault();
    let searchQuery = document.getElementById('search').value;
    let url = this.dataset.url;

    fetch(`${url}?search=${searchQuery}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            let resultsContainer = document.getElementById('resultsContainer');
            resultsContainer.innerHTML = '';

            if (data.books.length === 0) {
                resultsContainer.innerHTML = '<p class="error-message">We couldn\'t find any books matching your search. Please try again with a different title.</p>';
                return;
            }

            data.books.forEach(book => {
                let bookDiv = document.createElement('div');
                bookDiv.classList.add('book');

                bookDiv.innerHTML = `
                    <img src="https://covers.openlibrary.org/b/isbn/${book.isbn}-S.jpg" alt="${book.default_image_url}" class="book-image" />
                    <div class="book-details">
                        <h2>${book.title}</h2>
                        <p><strong>ISBN:</strong> ${book.isbn}</p>
                        <p><strong>Author:</strong> ${book.author}</p>
                        <p><strong>Publication Year:</strong> ${book.publication_year}</p>
                        <button class="add-book-btn" data-book-id="${book.id}">Add Book</button>
                    </div>
                `;

                resultsContainer.appendChild(bookDiv);
            });

            document.querySelectorAll('.add-book-btn').forEach(button => {
                button.addEventListener('click', function() {
                    let bookId = this.dataset.bookId;

                    fetch('book/add', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ bookId: bookId }),
                    })
                    .then(response => response.json())
                    .then(data => console.log(data))
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                });
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
