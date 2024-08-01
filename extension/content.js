function getFen() {
    const fenInputElement = document.querySelector('input.copyable[spellcheck="false"]');

    if (!fenInputElement) {
        console.error('Error: FEN input element not found');
        return null;
    }

    const fenValue = fenInputElement.value.trim();

    if (fenValue === '') {
        console.error('Error: FEN input value is empty');
        return null;
    }

    return fenValue;
}

function getPgn() {
    const pgnElement = document.querySelector('textarea.copyable[spellcheck="false"]');

    if (!pgnElement) {
        console.error('Error: PGN element not found');
        return null;
    }

    const pgnValue = pgnElement.value.trim();

    if (pgnValue === '') {
        console.error('Error: PGN value is empty');
        return null;
    }

    return pgnValue;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getFen') {
        const fen = getFen();
        const pgn = getPgn();
        sendResponse({ fen: fen, pgn: pgn });
    }
    return true; // Keeps the message channel open for asynchronous response
});
