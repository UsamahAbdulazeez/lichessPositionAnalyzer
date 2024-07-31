chrome.runtime.onInstalled.addListener(() => {
    console.log('Lichess Position Analyzer installed');
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'fetchAnalysis') {
        fetch(request.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(request.data)
        })
        .then(response => response.json())
        .then(data => sendResponse({success: true, data: data}))
        .catch(error => sendResponse({success: false, error: error.toString()}));
        return true;  // Will respond asynchronously
    }
});