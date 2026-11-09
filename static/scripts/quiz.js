const apiGateway = "/api/get_quiz"

const delay = ms => new Promise(res => setTimeout(res, ms));

let quizData = undefined

let quizResult = []


async function loadQuizData(quizId) {
    try {
        const response = await fetch(`${apiGateway}/${quizId}`);

        // Read the response body so we can inspect Flask errors
        const text = await response.text();

        if (!response.ok) {
            console.error("Flask returned an error:", response.status);
            console.error("Server response:", text);
            throw new Error(`HTTP ${response.status}: ${text}`);
        }

        quizData = JSON.parse(text);
    } catch (error) {
        console.error("Error in loadQuizData:", error);
        alert("Erreur lors du chargement du quiz. Consulte la console.");
        return null;
    }
}


function loadQuestion(question) {
    const questionH1 = document.getElementById("question-txt")
    const currentQuestionName = quizData.questions[question].title
    const currentAnswers = quizData.questions[question].answers
    const answersZone = document.getElementById("answers-zone")

    questionH1.innerText = currentQuestionName
    //console.log(answersZone.children)
    answersZone.innerHTML = "" // Empty the content of the div
    let i = 0
    for (const answer of currentAnswers) {
        const newAnswer = document.createElement("button")
        newAnswer.className = "answer"
        newAnswer.id = answer.id
        newAnswer.innerHTML = answer.title
        newAnswer.addEventListener("click", (event) => {onAnswerClick(event.target, answer.correct) })
        answersZone.appendChild(newAnswer)
        i++
    }
}

let currentQuestion = 0

function loadNextQuestion() {
    currentQuestion++
    if (currentQuestion < quizData.questions.length)
        loadQuestion(currentQuestion)
    else
        finishQuiz()
}

function finishQuiz() {
    const questionH1 = document.getElementById("question-txt")
    const answersZone = document.getElementById("answers-zone")
    answersZone.innerHTML = "" // Empty the content of the div
    //questionH1.innerText = "C'est la fin la team"
    window.location = "/result?quiz_id=" + quizData.id + "&quiz_result=" + JSON.stringify(quizResult)
}


const greenBack = "linear-gradient(180deg,#12ff1b,#0fb300)"
const redBack = "linear-gradient(180deg,#ff1f1f,#cc0000)"


let hasAnswered = false

async function onAnswerClick(answer, correctness) {
    if (hasAnswered) return
    hasAnswered = true

    answer.style.background = correctness ? greenBack : redBack

    quizResult.push(parseInt(answer.id))

    // TODO : Save answers for the result

    await delay(1000)
    loadNextQuestion()
    hasAnswered = false
}


function getQueryVariable(variable) {
    const params = new URLSearchParams(window.location.search);
    return params.get(variable); 
}



async function init() {
    const quizId = getQueryVariable("quiz_id")
    if (quizId === null || quizId === "") {
        window.location.href = "/"
        return false          
    }
    await loadQuizData(quizId)
    return quizData !== undefined
}

init().then(ok => {
    if (ok) loadQuestion(0)
})
