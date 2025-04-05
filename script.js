let websiteContent = "";

function loadWebsite() {
  const url = document.getElementById("urlInput").value;

  fetch('backend.php', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `url=${encodeURIComponent(url)}&action=scrape`
  })
  .then(response => response.text())
  .then(data => {
    websiteContent = data.toLowerCase();
    alert("Website content loaded.");
  });
}

function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value;
  appendToChat("You: " + message);

  fetch('backend.php', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `question=${encodeURIComponent(message)}&content=${encodeURIComponent(websiteContent)}&action=chat`
  })
  .then(response => response.text())
  .then(answer => {
    appendToChat("Bot: " + answer);
    input.value = "";
  });
}

function appendToChat(text) {
  const chatBox = document.getElementById("chatBox");
  chatBox.innerHTML += `<div>${text}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}
