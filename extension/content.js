function getFen() {
    const fenInput = document.querySelector('input.copyable');
    if (fenInput) {
        return fenInput.value;
    }
    return null;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getFen') {
        const fen = getFen();
        sendResponse({ fen: fen });
    }
});
