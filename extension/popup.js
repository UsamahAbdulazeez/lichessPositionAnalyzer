document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('getPosition').addEventListener('click', getPosition);
    
    document.getElementById('btn-tactical').addEventListener('click', () => performAnalysis('tactical'));
    document.getElementById('btn-positional').addEventListener('click', () => performAnalysis('positional'));
    document.getElementById('btn-material').addEventListener('click', () => performAnalysis('material'));
    document.getElementById('btn-strategic').addEventListener('click', () => performAnalysis('strategic'));
    document.getElementById('btn-dynamic').addEventListener('click', () => performAnalysis('dynamic'));
    document.getElementById('btn-summary').addEventListener('click', () => performAnalysis('summary'));

    function getPosition() {
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, { action: "getFen" }, (response) => {
                if (chrome.runtime.lastError) {
                    console.error(chrome.runtime.lastError);
                    document.getElementById('fenDisplay').innerText = 'Error: ' + chrome.runtime.lastError.message;
                    return;
                }
                if (response && response.fen) {
                    document.getElementById('fenDisplay').innerText = 'FEN: ' + response.fen;
                    document.getElementById('pgnDisplay').innerText = 'PGN: ' + response.pgn;
                    chrome.storage.local.set({ fen: response.fen, pgn: response.pgn });
                } else {
                    document.getElementById('fenDisplay').innerText = 'Failed to get FEN';
                }
            });
        });
    }

    function performAnalysis(type) {
        chrome.storage.local.get(['fen', 'pgn'], (result) => {
            if (result.fen && result.pgn) {
                document.getElementById('analysisResult').innerText = 'Analyzing...';
                fetchAnalysis(type, result.fen, result.pgn);
            } else {
                document.getElementById('analysisResult').innerText = 'FEN or PGN not available. Please get position first.';
            }
        });
    }

    function fetchAnalysis(type, fen, pgn) {
        chrome.runtime.sendMessage({
            action: 'fetchAnalysis',
            url: 'https://lichess-position-analyzer.onrender.com/analysis',
            data: { fen: fen, pgn: pgn, analysis: type }
        }, response => {
            console.log('Response:', response);  // Log the entire response
            if (response.success && response.data.explanation) {
                displayAnalysis(response.data.explanation, type);
            } else {
                document.getElementById('analysisResult').innerText = 'Error: ' + (response.error || 'Unknown error occurred');
            }
        });    
    }

    function displayAnalysis(explanation, type) {
        document.getElementById('analysisResult').innerText = explanation;
    }
});