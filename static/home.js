document.addEventListener('DOMContentLoaded', (event) => {
    let sortSelect = document.getElementById('sort');
    let resetBtn = document.getElementById('resetBtn');

    sortSelect.addEventListener('change', function() {
        if (this.value) {
            // Getting href from Reset button
            let resetHref = resetBtn.getAttribute('href');
            // Update the location to the Reset button's href with the sort value
            window.location = resetHref + "?sort=" + this.value;
        }
    });
});
