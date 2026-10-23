const boutons = document.querySelectorAll(".start-quiz");

boutons.forEach(bouton => {

    bouton.addEventListener("click", () => {

        window.location.href = `/quiz/${bouton.id}`;

    });

});


const score = 58;  //Connecter à la base de données pour récupérer le score réel de l'utilisateur
const total = 87; //Connecter à la base de données pour récupérer le score réel de l'utilisateur

// Calcul des résultats
const bonnesReponses = score;
const mauvaisesReponses = total - score;
const pourcentage = total > 0
    ? Math.round((score / total) * 100)
    : 0;

// Mise à jour du score
document.getElementById("score").textContent = score;
document.getElementById("total").textContent = total;

// Mise à jour du pourcentage
document.getElementById("percentage").textContent =
    pourcentage + " % de réussite";

// Mise à jour de la barre de progression
document.getElementById("progress").style.width =
    pourcentage + "%";

// Mise à jour des statistiques
document.getElementById("bonnes-reponses").textContent =
    bonnesReponses;

document.getElementById("mauvaises-reponses").textContent =
    mauvaisesReponses;

// Message personnalisé
const message = document.getElementById("message");

if (pourcentage >= 80) {
    message.textContent = "Excellent travail ! 🎉";
} else if (pourcentage >= 50) {
    message.textContent = "Bien joué, continue ! 👍";
} else {
    message.textContent = "Continue à t'entraîner ! 💪";
}