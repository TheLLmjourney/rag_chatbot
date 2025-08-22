const chatBody = document.getElementById("chat-body");
const userInput = document.getElementById("user-input");

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender === "user" ? "user-message" : "bot-message");
  msg.textContent = text;
  chatBody.appendChild(msg);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function sendMessage() {
  const text = userInput.value.trim();
  if (text === "") return;

  const sessionId = document.getElementById("session-id").value;

  addMessage(text, "user");
  userInput.value = "";

  fetch("/get", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `msg=${encodeURIComponent(text)}&session_id=${encodeURIComponent(sessionId)}`
  })
  .then(res => res.text())
  .then(reply => {
    addMessage(reply, "bot");
  })
  .catch(err => {
    addMessage("⚠️ Error connecting to server.", "bot");
    console.error(err);
  });
}

// ✅ Allow pressing Enter to send message
userInput.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    sendMessage();
  }
});
