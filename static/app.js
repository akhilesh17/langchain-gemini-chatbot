async function sendMessage() {
    let input = document.getElementById("user-input");
    let msg = input.value.trim();
    if (!msg) return;

    let chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `<div class='user'>You: ${msg}</div>`;
    input.value = "";

    const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            text: msg,
            session_id: "user1"
        })
    });

    const data = await res.json();
    chatBox.innerHTML += `<div class='bot'>Bot: ${data.reply}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}
