const apiGateway = "/api/get_quiz"

const delay = ms => new Promise(res => setTimeout(res, ms));

let quizData = undefined

// For test purposes
let quizExample = {
    "Quelle est la capitale de la Suisse ?": {
        "Bernes": true,
        "Genève": false,
        "Basel": false,
        "Berlin": false
    },
    "Qui présente les douzes coups de midi ?": {
        "Samuel Étienne": false,
        "Jean Pierre Foucault": false,
        "Jean Fils": false,
        "Jean Luc Reichman": true
    },
    "En quelle année est sortie le jeu vidéo Phasmophobia ?": {
        "2022": false,
        "2021": false,
        "2020": true,
        "2019": false,
        "2018": false,
        "2017": false
    },
    "Où se situe le lac d'Annecy ?": {
        "San Fransisco": false,
        "Istanbul": false,
        "L'autre": true
    },
    "Combien font 7+7 ?": {
        "1": false,
        "2": false,
        "3": false,
        "4": false,
        "5": false,
        "6": false,
        "7": false,
        "8": false,
        "9": false,
        "10": false,
        "11": false,
        "12": false,
        "13": false,
        "14": true,
        "15": false,
        "16": false,
        "17": false,
        "18": false,
        "19": false,
        "20": false
    },
    "Est-ce que vous vous amusez ?": {
        "Oui": true
    }
}


quizData = quizExample

//////////////////


async function loadQuizData(quizId) {

    const quizRequestMethod = {
        method: "post",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "id=" + quizId,
    }

    try {
        const response = await fetch(apiGateway, quizRequestMethod)

        if (!response.ok) {
            throw new Error('Une erreur est survenue lors du chargement des ressources')
        }

        const blob = await response.blob()
        const text = await blob.text()
        quizData = JSON.parse(text)

    } catch (error) {
        console.error(error)
        alert('Une erreur est survenue lors du traitement des données, voir plus de détail en console')
        return null;
    }
}

function loadQuestion(question) {
    const questionH1 = document.getElementById("question-txt")
    const currentQuestionName = Object.keys(quizData)[question]
    const currentAnswers = quizData[currentQuestionName]
    //if (!currentQuestion) throw new Error("La question " + question + " n'existe pas")
    const answersZone = document.getElementById("answers-zone")

    questionH1.innerText = currentQuestionName
    //console.log(answersZone.children)
    answersZone.innerHTML = "" // Empty the content of the div
    let i = 0
    for (const [answer, correctness] of Object.entries(currentAnswers)) {
        const newAnswer = document.createElement("button")
        newAnswer.className = "answer"
        newAnswer.id = "answer-" + i
        newAnswer.innerHTML = answer
        newAnswer.addEventListener("click", (event) => {onAnswerClick(event.target, correctness) })
        answersZone.appendChild(newAnswer)
        i++
    }
}

let currentQuestion = 0

function loadNextQuestion() {
    // TODO : Implement
    currentQuestion++
    if (currentQuestion < Object.keys(quizData).length)
        loadQuestion(currentQuestion)
    else
        finishQuiz()
}

function finishQuiz() {
    const questionH1 = document.getElementById("question-txt")
    const answersZone = document.getElementById("answers-zone")
    answersZone.innerHTML = "" // Empty the content of the div
    questionH1.innerText = "C'est la fin la team"
}


const greenBack = "linear-gradient(180deg,#12ff1b,#0fb300)"
const redBack = "linear-gradient(180deg,#ff1f1f,#cc0000)"


let hasAnswered = false

async function onAnswerClick(answer, correctness) {
    if (hasAnswered) return
    hasAnswered = true

    answer.style.background = correctness ? greenBack : redBack

    // TODO : Save answers for the result

    await delay(1000)
    loadNextQuestion()
    hasAnswered = false
}


async function init() {
    // TODO : Connect with the API
}

init().then(() => {loadQuestion(0)})

