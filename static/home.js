document.addEventListener('DOMContentLoaded', (event) => {
    let sortSelect = document.getElementById('sort');

    sortSelect.addEventListener('change', function() {
        if (this.value) {
            let currentUrl = window.location.href.split('?')[0];
            window.location = currentUrl + "?sort=" + this.value;
        }
    });
});
