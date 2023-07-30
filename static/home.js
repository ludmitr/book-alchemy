document.getElementById('sort').addEventListener('change', function() {
    if (this.value) {
        window.location = window.location.pathname + "?sorted_by=" + this.value;
    }
});

