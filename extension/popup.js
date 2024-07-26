document.addEventListener('DOMContentLoaded', function () {
    let analyzeBtn = document.getElementById('analyzeBtn');
    let explanationBtn = document.getElementById('explanationBtn');

    chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
        if (request.action === 'sendFen') {
            document.getElementById('fenInput').value = request.fen;
        }
    });

    analyzeBtn.addEventListener('click', function () {
        let fen = document.getElementById('fenInput').value;
        fetch('https://lichess-position-analyzer.onrender.com/stockfish', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ fen: fen })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('analysisOutput').textContent = JSON.stringify(data.analysis, null, 2);
        })
        .catch(error => console.error('Error:', error));
    });

    explanationBtn.addEventListener('click', function () {
        let fen = document.getElementById('fenInput').value;
        let analysis = document.getElementById('analysisOutput').textContent;
        fetch('https://lichess-position-analyzer.onrender.com/explanation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ fen: fen, analysis: analysis })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('explanationOutput').textContent = data.explanation;
        })
        .catch(error => console.error('Error:', error));
    });
});
