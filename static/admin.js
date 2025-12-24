async function loadImages() {
    const res = await fetch("/api/images");
    const images = await res.json();

    const gallery = document.getElementById("gallery");
    gallery.innerHTML = "";

    images.forEach(filename => {
        const card = document.createElement("div");
        card.className = "image-card";

        const img = document.createElement("img");
        img.src = `/uploads/${filename}`;

        const btn = document.createElement("button");
        btn.className = "delete-btn";
        btn.textContent = "🗑️";

        btn.onclick = async () => {
            if (!confirm("Supprimer cette image ?")) return;

            const res = await fetch("/delete", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ filename })
            });

            const result = await res.json();
            if (result.success) loadImages();
        };

        card.appendChild(img);
        card.appendChild(btn);
        gallery.appendChild(card);
    });
}

document.getElementById("upload-form").addEventListener("submit", async e => {
    e.preventDefault();

    const file = document.getElementById("image-input").files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    await fetch("/upload", {
        method: "POST",
        body: formData
    });

    loadImages();
    e.target.reset();
});

loadImages();

const matiereButtons = document.querySelectorAll("button.title-matiere");

matiereButtons.forEach(matiereButton => {
    matiereButton.addEventListener("click", () => {
        let el = matiereButton.parentElement.getElementsByClassName("list-cours")[0]
        if (el.style.maxHeight === "0px"){
            el.style.maxHeight = el.scrollHeight + "px";
        }
        else {
            el.style.maxHeight = "0";
        }
        let arrow = matiereButton.parentElement.getElementsByClassName("arrow")[0]
        arrow.classList.toggle("return")
    });
});
