document.querySelectorAll('.menu-toggle').forEach(toggle => {
    toggle.addEventListener('click', function(e) {
        e.preventDefault();
        const item = this.closest('.side-item');
        item.classList.toggle('active-sub');
    });
});