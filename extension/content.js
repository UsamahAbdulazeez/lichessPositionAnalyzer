// Script to extract the FEN from the Lichess board
function getBoardPosition() {
    let fenElement = document.querySelector('input.copyable');
    if (fenElement) {
        let fen = fenElement.value;
        chrome.runtime.sendMessage({ fen: fen });
    } else {
        console.error('Board not found');
    }
}

getBoardPosition();
