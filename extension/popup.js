document.getElementById('getPosition').addEventListener('click', function() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            files: ['content.js']
        }, () => {
            chrome.tabs.sendMessage(tabs[0].id, { action: "getFen" }, (response) => {
                if (response && response.fen) {
                    document.getElementById('fenDisplay').innerText = 'FEN: ' + response.fen;
                    chrome.storage.local.set({ fen: response.fen });
                } else {
                    document.getElementById('fenDisplay').innerText = 'Failed to get FEN';
                    console.error('Failed to get FEN from content script');
                }
            });
        });
    });
});

document.getElementById('btn-checks').addEventListener('click', () => {
    performAnalysis('checks');
});
document.getElementById('btn-weak-strong').addEventListener('click', () => {
    performAnalysis('pieces');
});
document.getElementById('btn-key-ideas').addEventListener('click', () => {
    performAnalysis('ideas');
});
document.getElementById('btn-overview').addEventListener('click', () => {
    performAnalysis('overview');
});

function performAnalysis(type) {
    chrome.storage.local.get('fen', (result) => {
        if (result.fen) {
            document.getElementById('analysisResult').innerText = 'Fetching analysis...';
            fetchAnalysis(type, result.fen);
        } else {
            document.getElementById('analysisResult').innerText = 'FEN not available';
            console.error('FEN not available in storage');
        }
    });
}

async function fetchAnalysis(type, fen) {
    try {
        const response = await fetch(`https://lichess-position-analyzer.onrender.com/analysis`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ fen: fen, analysis: type })
        });
        const data = await response.json();
        document.getElementById('analysisResult').innerText = data.explanation || 'No explanation available';
    } catch (error) {
        console.error('Error fetching analysis:', error);
        document.getElementById('analysisResult').innerText = 'Error fetching analysis.';
    }
}
