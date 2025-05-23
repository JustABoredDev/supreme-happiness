// content.js
window.onload = function() {
  let imgElement = document.querySelector('img[name="CPTC"]');
  let inputElement = document.querySelector('input[name="res"]');
  
  console.log(imgElement)
  console.log(inputElement)
  let ran = false;
  imgElement.onload = function()
  {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = imgElement.width;
    canvas.height = imgElement.height;
    ctx.drawImage(imgElement, 0, 0);
  
    // Now get the image data
    const imageData = ctx.getImageData(0, 0, imgElement.width, imgElement.height);
    console.log(imageData);

    imageURL = canvas.toDataURL()

    if (imgElement && inputElement) {
      chrome.runtime.sendMessage({ action: "sendImage", imageUrl: imageURL });
    }
    if(!ran)
    {
      ran = true;
      chrome.runtime.onMessage.addListener((message) => {
        if (message.action === "insertResult") {
          inputElement.value = message.result;
        }
      });
    }
  }  
}