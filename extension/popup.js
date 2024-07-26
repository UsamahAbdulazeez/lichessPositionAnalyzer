// popup.js
document.addEventListener('DOMContentLoaded', function () {
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.type === 'stockfishAnalysis') {
            displayAnalysis(message.data);
            fetchExplanation(message.data.fen, message.data.analysis);
        }
    });
});

function displayAnalysis(data) {
    // Display Stockfish analysis in the popup
    document.getElementById('analysis').innerText = `Best Move: ${data.best_move}`;
}

function fetchExplanation(fen, analysis) {
    fetch('https://lichess-position-analyzer.onrender.com/explanation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fen: fen, analysis: analysis }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('explanation').innerText = data.explanation;
    })
    .catch(error => console.error('Error:', error));
}
