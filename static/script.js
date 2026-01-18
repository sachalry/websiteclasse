const header = document.querySelector('header');
const bodyChildren = document.body.children;
const links = document.querySelectorAll('header__link');


for (let i = 0; i < bodyChildren.length; i++) {
    const child = bodyChildren[i];
    if (child !== header) {
        child.classList.add('hide')
    }
}

links.forEach(link => {
    link.classList.add('hide')
});

window.addEventListener('DOMContentLoaded', () => {
    // wait a second before adding the class
    setTimeout(() => {
        header.classList.add('loaded')

        for (let i = 0; i < bodyChildren.length; i++) {
            const child = bodyChildren[i];

            if (child !== header) {
                child.classList.remove('hide')
            }
        }
        
        links.forEach(link => {
            link.classList.remove('hide')
        });
    }, 500);
});