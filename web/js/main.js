document.addEventListener("DOMContentLoaded", () => {
    const popup = document.getElementById("popup");
    const popupContent = document.getElementById("popup-content");
    const popupClose = document.getElementById("popup-close");

    if (!popup || !popupContent || !popupClose) {
        console.error("Popup elements not found in DOM.");
        return;
    }

    document.querySelectorAll(".article-link").forEach(link => {
        link.addEventListener("click", e => {
            e.preventDefault();
            const id = link.dataset.id;
            popupContent.innerHTML = "Loading...";
            popup.classList.remove("hidden");

            fetch(`fetch_article.php?id=${id}`)
                .then(res => res.text())
                .then(html => popupContent.innerHTML = html)
                .catch(() => popupContent.innerHTML = "Error loading article.");
        });
    });

    popupClose.addEventListener("click", () => {
        popup.classList.add("hidden");
        popupContent.innerHTML = "";
    });
});

