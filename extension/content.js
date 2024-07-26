function getBoardPosition() {
    let fenElement = document.querySelector('input.copyable');
    if (fenElement) {
        let fen = fenElement.value;
        chrome.runtime.sendMessage({ action: 'sendFen', fen: fen });
    } else {
        console.error('Board not found');
    }
}

getBoardPosition();
