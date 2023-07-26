<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='add_author.css')}}">
    <title>Add Author</title>
</head>
<body>
    <div class="container">
        <form id="addAuthorForm" action="{{ url_for('add_author') }}" method="POST">
            <h2>Add Author</h2>
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="birthdate">Birthdate:</label>
                <input type="date" id="birthdate" name="birthdate" required>
            </div>
            <div class="form-group">
                <label for="deathdate">Deathdate:</label>
                <input type="date" id="deathdate" name="deathdate">
            </div>
            <div class="form-group">
                <button type="submit">Add Author</button>
            </div>
        </form>
    </div>
    <script>
        document.getElementById('addAuthorForm').addEventListener('submit', function(event) {
            event.preventDefault();

            fetch('/add_author', {
                method: 'POST',
                body: new FormData(event.target), // event.target is the form
            })
            .then(response => {
                if (!response.ok) {
                    throw response;
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
            })
            .catch(err => {
                if (err.json) {
                    err.json().then(errorMessage => {
                        alert(errorMessage.error);
                    });
                } else {
                    console.error('Error:', err);
                }
            });
        });
    </script>
</body>
</html>
