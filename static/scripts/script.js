const boutons = document.querySelectorAll(".start-quiz");

boutons.forEach(bouton => {
    bouton.addEventListener("click", () => {
        window.location.href = `/quiz?quiz_id=${bouton.id}`;
    });
});

