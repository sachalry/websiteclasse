// Animation du loader

window.addEventListener('load', () => {
    setTimeout(() => {
        loadFunction();
    }, 500);
});

function loadFunction() {
    const loadScreen = document.querySelector('.load_screen');
    loadScreen.classList.add('loaded');
    setTimeout(() => {
        loadScreen.style.display = 'none';
    }, 1000);
}