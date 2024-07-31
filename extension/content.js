function getFen() {
    // Try to get FEN from the copyable input
    let fenInput = document.querySelector('input.copyable[spellcheck="false"]');
    if (fenInput && fenInput.value) {
        return fenInput.value;
    }

    // If not found, try to get FEN from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const fenFromUrl = urlParams.get('fen');
    if (fenFromUrl) {
        return fenFromUrl;
    }

    // If still not found, try to get it from the last move's data attribute
    const lastMove = document.querySelector('.last-move');
    if (lastMove) {
        return lastMove.getAttribute('data-fen');
    }

    return null;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getFen') {
        const fen = getFen();
        console.log("FEN found:", fen); // Add this for debugging
        sendResponse({ fen: fen });
    }
    return true; // Keeps the message channel open for asynchronous response
});