// Function to display pop-up message
function showMessage(message, isSuccess) {
    const messageContainer = document.getElementById('message-container');
    const messageElement = document.createElement('div');
    messageElement.innerText = message;
    messageElement.classList.add('message');
    if (isSuccess) {
        messageElement.classList.add('success');
    } else {
        messageElement.classList.add('error');
    }
    messageContainer.appendChild(messageElement);

    // Remove the message after a few seconds
    setTimeout(() => {
        messageElement.remove();
    }, 5000); // Display message for 5 seconds
}

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
        // Display success message
        showMessage(data.message, true);
    })
    .catch(err => {
        if (err.json) {
            err.json().then(errorMessage => {
                // Display error message
                showMessage(errorMessage.error, false);
            });
        } else {
            console.error('Error:', err);
        }
    });
});
