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

        document.getElementById('btn-checks').addEventListener('click', () => {
            document.getElementById('analysisResult').innerText = 'Fetching analysis...';
            fetchAnalysis('threats', message.fen);
        });
        document.getElementById('btn-weak-strong').addEventListener('click', () => {
            document.getElementById('analysisResult').innerText = 'Fetching analysis...';
            fetchAnalysis('pieces', message.fen);
        });
        document.getElementById('btn-key-ideas').addEventListener('click', () => {
            document.getElementById('analysisResult').innerText = 'Fetching analysis...';
            fetchAnalysis('ideas', message.fen);
        });
        document.getElementById('btn-overview').addEventListener('click', () => {
            document.getElementById('analysisResult').innerText = 'Fetching analysis...';
            fetchAnalysis('overview', message.fen);
        });
    }
});

async function fetchAnalysis(type, fen) {
    const response = await fetch(`https://lichess-position-analyzer.onrender.com/analysis`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ fen: fen, analysis: type })
    });
    const data = await response.json();
    document.getElementById('analysisResult').innerText = data.explanation;
}
