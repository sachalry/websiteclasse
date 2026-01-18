const modal = document.getElementById("image-modal");
const modalImg = document.getElementById("modal-img");
const closeBtn = document.querySelector(".modal-close");

document.querySelectorAll(".button-img img").forEach(img => {
    img.addEventListener("click", () => {
        modal.style.display = "flex";       // affiche l'overlay
        modalImg.src = img.src;             // met la bonne image
        document.getElementById("modal-link").href = img.src; // met le bon lien
        setTimeout(() => {
            modal.classList.add("show");   
        }, 1);
    });
});

closeBtn.addEventListener("click", () => {
    modal.classList.remove("show");        // animation de fermeture
    setTimeout(() => {                     // attend la fin de l'animation
        modal.style.display = "none";
    }, 300);
});

// Fermer si clic en dehors de l'image
modal.addEventListener("click", e => {
    if (e.target === modal) {
        modal.classList.remove("show");
        setTimeout(() => {
            modal.style.display = "none";
        }, 300);
    }
});

// Zoom sur clic
modalImg.addEventListener("click", e => {
    e.stopPropagation(); // empêche de fermer le modal

    if (!modalImg.classList.contains("zoomed")) {

        const rect = modalImg.getBoundingClientRect();

        // Position du curseur dans l'image
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // Conversion en pourcentage
        const xPercent = (x / rect.width) * 100;
        const yPercent = (y / rect.height) * 100;

        // Définit le point d'origine du zoom
        modalImg.style.transformOrigin = `${xPercent}% ${yPercent}%`;
    }

    modalImg.classList.toggle("zoomed"); // toggle zoom
});