chrome.runtime.onInstalled.addListener(() => {
    console.log('Lichess Position Analyzer installed');
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'fetchAnalysis') {
        console.log('Sending request:', request);  // Log the outgoing request
        fetch(request.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(request.data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data);  // Log the received data
            sendResponse({success: true, data: data});
        })
        .catch(error => {
            console.error('Fetch error:', error);  // Log any errors
            sendResponse({success: false, error: error.toString()});
        });
        return true;  // Will respond asynchronously
    }
});