fetch("https://chatbot-integration.up.railway.app/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    question: "Your question here",
    url: "https://example.com"
  })
})
.then(res => res.json())
.then(data => {
  console.log(data.answer);
});
