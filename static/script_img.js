document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
        const card = e.target.closest(".image-div");
        const filename = card.dataset.filename;

        if (!confirm("Supprimer cette image ?")) return;

        const response = await fetch("/delete", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ filename })
        });

        const result = await response.json();

        if (result.success) {
            card.remove();
        } else {
            alert("Erreur lors de la suppression");
        }
    });
});