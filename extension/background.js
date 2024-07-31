chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "getFen",
        title: "Get FEN",
        contexts: ["all"]
    });

    chrome.contextMenus.onClicked.addListener((info, tab) => {
        if (info.menuItemId === "getFen") {
            chrome.tabs.sendMessage(tab.id, { action: "getFen" }, (response) => {
                if (response && response.fen) {
                    chrome.storage.local.set({ fen: response.fen }, () => {
                        console.log("FEN saved: " + response.fen);
                    });
                } else {
                    console.error('Failed to retrieve FEN from content script');
                }
            });
        }
    });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'sendFen') {
        chrome.storage.local.set({ fen: message.fen });
    } else if (message.action === 'getExplanation') {
        chrome.storage.local.get(['fen', 'analysis'], (result) => {
            if (result.fen && result.analysis) {
                fetchExplanation(result.fen, result.analysis, sendResponse);
            } else {
                console.error('FEN or analysis type not found in storage');
            }
        });
    }
    return true;
});

function fetchExplanation(fen, analysis, callback) {
    fetch('https://lichess-position-analyzer.onrender.com/analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fen: fen, analysis: analysis }),
    })
    .then(response => response.json())
    .then(data => {
        callback(data);
    })
    .catch(error => {
        console.error('Error fetching explanation:', error);
        callback({ error: 'Failed to fetch analysis' });
    });
}
