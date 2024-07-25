document.getElementById('getPosition').addEventListener('click', function() {
    chrome.tabs.query({ active: true, currentWindow: true }, async function(tabs) {
        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            files: ['content.js']
        });
    });
});

chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    if (message.fen) {
        document.getElementById('fenDisplay').innerText = 'FEN: ' + message.fen;

        const stockfishAnalysis = await getStockfishAnalysis(message.fen);
        const explanation = await getExplanation(message.fen, stockfishAnalysis);

        document.getElementById('showThreats').addEventListener('click', () => {
            document.getElementById('threats').innerText = explanation;
            document.getElementById('threats').style.display = 'block';
        });
        document.getElementById('showIdeas').addEventListener('click', () => {
            document.getElementById('ideas').innerText = explanation;
            document.getElementById('ideas').style.display = 'block';
        });
        document.getElementById('showStrengths').addEventListener('click', () => {
            document.getElementById('strengths').innerText = explanation;
            document.getElementById('strengths').style.display = 'block';
        });
        document.getElementById('showPieces').addEventListener('click', () => {
            document.getElementById('pieces').innerText = explanation;
            document.getElementById('pieces').style.display = 'block';
        });
        document.getElementById('showGuidance').addEventListener('click', () => {
            document.getElementById('guidance').innerText = explanation;
            document.getElementById('guidance').style.display = 'block';
        });
    }
});

async function getStockfishAnalysis(fen) {
    const response = await fetch('https://your-app-name.onrender.com/stockfish', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ fen: fen })
    });
    const data = await response.json();
    return data.analysis;
}

async function getExplanation(fen, stockfishAnalysis) {
    const response = await fetch('https://your-app-name.onrender.com/explanation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ fen: fen, analysis: stockfishAnalysis })
    });
    const data = await response.json();
    return data.explanation;
}
