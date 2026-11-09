
let GLOBAL_QUESTION_INDEX = 0;

function setup_question(question, id) {
    const form = document.createElement("form");
    const titleLabel = document.createElement("label");
    titleLabel.for = "question-title-" + id;
    titleLabel.innerHTML = "Titre de la question :"
    const titleInput = document.createElement("input");
    titleInput.id = "question-title-" + id;
    titleInput.type = "text";
    titleInput.name = "question-title-" + id;
    titleInput.placeholder = "Quelle est la capital de la France ?";
    const answerContainer = document.createElement("div");
    answerContainer.class = "answer-container";
    const addAnswerButton = document.createElement("div");
    addAnswerButton.class = "add-answer";
    // <object class="plus-icon" data="../static/icons/plus.svg" type="image/svg+xml"></object>
    const plusSvg = document.createElement("svg");
    plusSvg.class = "plus-icon";
    plusSvg.data = "../static/icons/plus.svg"
    plusSvg.type = "image/svg+xml"
    addAnswerButton.appendChild(plusSvg);
    answerContainer.appendChild(addAnswerButton);

    form.appendChild(titleLabel);
    form.appendChild(titleInput);
    form.appendChild(answerContainer);
    question.appendChild(form)
}

function new_question() {
    const qContainer = document.getElementById("question-container")
    let nel = document.createElement("div")
    nel.className = "question"
    nel.id = "q-" + GLOBAL_QUESTION_INDEX
    GLOBAL_QUESTION_INDEX++;
    //nel.innerHTML = "Bonjor"
    setup_question(nel)

    qContainer.insertBefore(nel, qContainer.firstChild)

}

function delete_question(id) {

}

function new_answer(question_id) {

}

function submit() {

}