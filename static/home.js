document.addEventListener('DOMContentLoaded', (event) => {
    let resetButton = document.querySelector('.reset-button');
    let baseURL = resetButton.getAttribute('href');

    document.getElementById('sort').addEventListener('change', function() {
        if (this.value) {
            window.location = baseURL + "?sorted_by=" + this.value;
        }
    });
});
