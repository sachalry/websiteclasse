const header = document.querySelector('header');
const main = document.querySelector('main');
const links = document.querySelectorAll('header__link');

links.forEach(link => {
    link.classList.add('hide')
});

main.classList.add('hide')


window.addEventListener('DOMContentLoaded', () => {
    // wait a second before adding the class
    setTimeout(() => {
        header.classList.add('loaded')
        main.classList.remove('hide')
        links.forEach(link => {
            link.classList.remove('hide')
        });
    }, 500);
});