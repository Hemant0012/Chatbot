const askBot = async () => {
  const question = document.getElementById("question").value;
  const url = new URLSearchParams(window.location.search).get("url");

  const response = await fetch("https://chatbot-integration.up.railway.app/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ question, url })
  });

  const data = await response.json();
  document.getElementById("bot-response").innerText = data.answer;
};
