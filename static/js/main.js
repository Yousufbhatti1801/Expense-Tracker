document.addEventListener('DOMContentLoaded', function () {
    const btn = document.querySelector('.nav-hamburger');
    const navLinks = document.getElementById('nav-links');

    if (!btn || !navLinks) return;

    btn.addEventListener('click', function () {
        const isOpen = navLinks.classList.toggle('nav-open');
        btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    document.addEventListener('click', function (e) {
        if (!e.target.closest('.nav')) {
            navLinks.classList.remove('nav-open');
            btn.setAttribute('aria-expanded', 'false');
        }
    });
});
