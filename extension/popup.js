document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('getPosition').addEventListener('click', function() {
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
    });

    document.getElementById('btn-checks').addEventListener('click', () => {
        performAnalysis('checks_captures_threats');
    });

    document.getElementById('btn-weak-strong').addEventListener('click', () => {
        performAnalysis('weak_strong_pieces');
    });

    document.getElementById('btn-key-ideas').addEventListener('click', () => {
        performAnalysis('key_ideas_strategies');
    });

    function performAnalysis(type) {
        chrome.storage.local.get(['fen', 'pgn'], (result) => {
            if (result.fen) {
                document.getElementById('analysisResult').innerText = 'Fetching analysis...';
                fetchAnalysis(type, result.fen, result.pgn);
            } else {
                document.getElementById('analysisResult').innerText = 'FEN not available. Please get position first.';
            }
        });
    }

    function fetchAnalysis(type, fen, pgn) {
        chrome.runtime.sendMessage({
            action: 'fetchAnalysis',
            url: 'https://lichess-position-analyzer.onrender.com/analysis',
            data: { fen: fen, pgn: pgn, analysis: type }
        }, response => {
            if (response.success) {
                document.getElementById('analysisResult').innerText = response.data.explanation || 'No explanation available';
            } else {
                document.getElementById('analysisResult').innerText = 'Error: ' + response.error;
            }
        });    
    }
});