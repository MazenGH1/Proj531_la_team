const boutons = document.querySelectorAll(".start-quiz");

boutons.forEach(bouton => {
    bouton.addEventListener("click", () => {
        window.location.href = `/quiz?quiz_id=${bouton.id}`;
    });
});

// Results page logic (runs only if on result.html)
const scoreElement = document.getElementById("score");
if (scoreElement) {
    const score = 58;
    const total = 87;

    const bonnesReponses = score;
    const mauvaisesReponses = total - score;
    const pourcentage = total > 0 ? Math.round((score / total) * 100) : 0;

    scoreElement.textContent = score;
    document.getElementById("total").textContent = total;
    document.getElementById("percentage").textContent = pourcentage + " % de réussite";
    document.getElementById("progress").style.width = pourcentage + "%";
    document.getElementById("bonnes-reponses").textContent = bonnesReponses;
    document.getElementById("mauvaises-reponses").textContent = mauvaisesReponses;

    const message = document.getElementById("message");
    if (pourcentage >= 80) {
        message.textContent = "Excellent travail ! 🎉";
    } else if (pourcentage >= 50) {
        message.textContent = "Bien joué, continue ! 👍";
    } else {
        message.textContent = "Continue à t'entraîner ! 💪";
    }
}