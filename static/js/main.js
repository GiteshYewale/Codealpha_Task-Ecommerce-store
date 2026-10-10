document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Dynamic Star Rating selector interactive hover
    const ratingInputs = document.querySelectorAll('.star-rating-input input');
    ratingInputs.forEach(input => {
        input.addEventListener('change', function () {
            console.log('Selected rating:', this.value);
        });
    });

    // Quick Image preview switcher for product detail page
    const thumbnails = document.querySelectorAll('.product-thumb-sm');
    const mainImg = document.getElementById('main-product-img');
    if (thumbnails && mainImg) {
        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', function () {
                mainImg.src = this.dataset.src;
                thumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }
});
