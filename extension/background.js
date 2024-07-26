// background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.fen) {
        fetch('https://lichess-position-analyzer.onrender.com/stockfish', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ fen: message.fen }),
        })
        .then(response => response.json())
        .then(data => {
            chrome.runtime.sendMessage({ type: 'stockfishAnalysis', data: data });
        })
        .catch(error => console.error('Error:', error));
    }
});
