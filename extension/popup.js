document.addEventListener('DOMContentLoaded', function () {
    const explanationDiv = document.getElementById('explanation');

    document.getElementById('btn-get-explanation').addEventListener('click', function() {
        const analysis = document.getElementById('analysis-input').value;
        chrome.storage.local.set({ analysis: analysis }, function() {
            chrome.runtime.sendMessage({ action: 'getExplanation' }, function(response) {
                displayExplanation(response);
            });
        });
    });

    function displayExplanation(data) {
        explanationDiv.innerText = data.explanation;
    }
});
