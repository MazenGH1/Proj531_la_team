let GLOBAL_QUESTION_INDEX = 0;

function setup_question(questionEl, id) {
    const form = document.createElement("div");
    form.className = "question-card-content";

    // En-tête de la question (Label + Bouton supprimer)
    const header = document.createElement("div");
    header.className = "question-header";

    const titleLabel = document.createElement("label");
    titleLabel.htmlFor = "question-title-" + id;
    titleLabel.textContent = "Titre de la question :";

    const deleteQBtn = document.createElement("button");
    deleteQBtn.type = "button";
    deleteQBtn.className = "delete-question-btn";
    deleteQBtn.textContent = "Supprimer la question";
    deleteQBtn.onclick = () => delete_question(id);

    header.appendChild(titleLabel);
    header.appendChild(deleteQBtn);

    // Champ texte de la question
    const titleInput = document.createElement("input");
    titleInput.id = "question-title-" + id;
    titleInput.className = "question-title-input";
    titleInput.type = "text";
    titleInput.name = "question-title-" + id;
    titleInput.placeholder = "Quelle est la capitale de la France ?";

    // Conteneur des réponses
    const answerContainer = document.createElement("div");
    answerContainer.className = "answer-container";
    answerContainer.id = "answer-container-" + id;

    // Bouton "+" pour ajouter une réponse
    const addAnswerButton = document.createElement("div");
    addAnswerButton.className = "add-answer";
    addAnswerButton.onclick = () => new_answer(id);

    const plusObj = document.createElement("object");
    plusObj.className = "plus-icon small-plus";
    plusObj.data = "../static/icons/plus.svg";
    plusObj.type = "image/svg+xml";

    const addAnswerText = document.createElement("span");
    addAnswerText.textContent = "Ajouter une réponse";

    addAnswerButton.appendChild(plusObj);
    addAnswerButton.appendChild(addAnswerText);

    form.appendChild(header);
    form.appendChild(titleInput);
    form.appendChild(answerContainer);
    form.appendChild(addAnswerButton);
    questionEl.appendChild(form);

    // Ajoute 2 réponses par défaut pour gagner du temps
    new_answer(id);
    new_answer(id);
}

function new_question() {
    const qContainer = document.getElementById("question-container");
    const id = GLOBAL_QUESTION_INDEX++;

    const nel = document.createElement("div");
    nel.className = "question";
    nel.id = "q-" + id;
    nel.dataset.questionId = id;

    setup_question(nel, id);
    qContainer.appendChild(nel);
}

function delete_question(id) {
    const questionEl = document.getElementById("q-" + id);
    if (questionEl) {
        questionEl.remove();
    }
}

function new_answer(question_id) {
    const answerContainer = document.getElementById("answer-container-" + question_id);
    if (!answerContainer) return;

    const answerRow = document.createElement("div");
    answerRow.className = "answer-row";

    const answerInput = document.createElement("input");
    answerInput.type = "text";
    answerInput.className = "answer-input";
    answerInput.placeholder = "Texte de la réponse...";

    const correctLabel = document.createElement("label");
    correctLabel.className = "correct-label";

    const correctCheckbox = document.createElement("input");
    correctCheckbox.type = "checkbox";
    correctCheckbox.className = "answer-correct";

    correctLabel.appendChild(correctCheckbox);
    correctLabel.appendChild(document.createTextNode(" Bonne réponse"));

    const deleteAnsBtn = document.createElement("button");
    deleteAnsBtn.type = "button";
    deleteAnsBtn.className = "delete-answer-btn";
    deleteAnsBtn.textContent = "✕";
    deleteAnsBtn.title = "Supprimer cette réponse";
    deleteAnsBtn.onclick = () => answerRow.remove();

    answerRow.appendChild(answerInput);
    answerRow.appendChild(correctLabel);
    answerRow.appendChild(deleteAnsBtn);

    answerContainer.appendChild(answerRow);
}

async function submit() {
    const quizTitleInput = document.getElementById("quiz_name");
    const quizTitle = quizTitleInput ? quizTitleInput.value.trim() : "";

    if (!quizTitle) {
        alert("Veuillez entrer un titre pour le quiz.");
        return;
    }

    const questionElements = document.querySelectorAll("#question-container .question");
    if (questionElements.length === 0) {
        alert("Veuillez ajouter au moins une question.");
        return;
    }

    const questions = [];

    for (let i = 0; i < questionElements.length; i++) {
        const qEl = questionElements[i];
        const qTitleInput = qEl.querySelector(".question-title-input");
        const qTitle = qTitleInput ? qTitleInput.value.trim() : "";

        if (!qTitle) {
            alert(`La question n°${i + 1} n'a pas de titre.`);
            return;
        }

        const answerRows = qEl.querySelectorAll(".answer-row");
        const answers = [];
        let hasCorrectAnswer = false;

        answerRows.forEach((row) => {
            const aTitle = row.querySelector(".answer-input").value.trim();
            const isCorrect = row.querySelector(".answer-correct").checked;

            if (aTitle !== "") {
                answers.push({
                    title: aTitle,
                    correct: isCorrect
                });
                if (isCorrect) {
                    hasCorrectAnswer = true;
                }
            }
        });

        if (answers.length < 2) {
            alert(`La question "${qTitle}" doit contenir au moins 2 réponses.`);
            return;
        }

        if (!hasCorrectAnswer) {
            alert(`Veuillez cocher au moins une bonne réponse pour la question "${qTitle}".`);
            return;
        }

        questions.push({
            title: qTitle,
            answers: answers
        });
    }

    try {
        const response = await fetch("/creer_quiz", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: quizTitle,
                questions: questions
            })
        });

        const result = await response.json();

        if (!response.ok || result.error) {
            alert(result.error || "Une erreur est survenue lors de la création du quiz.");
            return;
        }

        if (result.status === "success" && result.redirect) {
            window.location.href = result.redirect;
        }
    } catch (error) {
        console.error("Erreur lors de l'envoi du quiz :", error);
        alert("Impossible de contacter le serveur.");
    }
}

// Crée automatiquement une première question au chargement de la page
document.addEventListener("DOMContentLoaded", () => {
    new_question();
});