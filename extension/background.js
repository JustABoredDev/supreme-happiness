
// background.js
chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    console.log("got message request")
    if (message.action === "sendImage") {
        
        response = await fetch("http://127.0.0.1:8000/post-data", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ imageUrl: message.imageUrl })
        })
        
        response = await response.json();
        console.log(response);
        chrome.tabs.sendMessage(sender.tab.id, { action: "insertResult", result: response.result });
  
    }
});