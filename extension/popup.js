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
            if (result.fen) {
                document.getElementById('analysisResult').innerText = 'Analyzing...';
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
                displayAnalysis(response.data, type);
            } else {
                document.getElementById('analysisResult').innerText = 'Error: ' + response.error;
            }
        });    
    }

    function displayAnalysis(data, type) {
        let result = '';
        switch (type) {
            case 'tactical':
                result = `Checks, Captures, and Threats:\n${data.checksCapturesThreats}\n\n`;
                result += `Tactical Motifs:\n${data.tacticalMotifs}`;
                break;
            case 'positional':
                result = `Piece Activity:\n${data.pieceActivity}\n\n`;
                result += `Pawn Structure:\n${data.pawnStructure}\n\n`;
                result += `King Safety:\n${data.kingSafety}\n\n`;
                result += `Control of Key Squares and Open Files:\n${data.keySquaresAndFiles}`;
                break;
            case 'material':
                result = `Piece Count:\n${data.pieceCount}\n\n`;
                result += `Material Imbalances:\n${data.materialImbalances}`;
                break;
            case 'strategic':
                result = `Key Ideas and Strategies:\n${data.keyIdeasStrategies}\n\n`;
                result += `Long-term Plans:\n${data.longTermPlans}\n\n`;
                result += `Potential Pawn Breaks:\n${data.pawnBreaks}`;
                break;
            case 'dynamic':
                result = `Initiative:\n${data.initiative}\n\n`;
                result += `Piece Coordination:\n${data.pieceCoordination}\n\n`;
                result += `Tempo Considerations:\n${data.tempoConsiderations}`;
                break;
            case 'summary':
                result = `Overall Position Assessment:\n${data.overallAssessment}\n\n`;
                result += `Critical Moves or Plans:\n${data.criticalMovesPlans}`;
                break;
        }
        document.getElementById('analysisResult').innerText = result;
    }
});