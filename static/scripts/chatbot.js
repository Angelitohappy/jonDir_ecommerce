async function exchange() {
    let user_input = document.querySelector("#user_input");
    let conversation_messages = document.querySelector("#chat");
    let message = user_input.value;
    user_input.value = "";
    let user_bubble = document.createElement("p");
    user_bubble.textContent = message;
    user_bubble.classList.add("user-message");
    conversation_messages.prepend(user_bubble);

    let server_json;
    try {
        const response = await fetch("http://127.0.0.1:5000/chatbot", {
            method: "POST",
            body: JSON.stringify({
                "input": message
            })
          });
        server_json = await response.json();
    }
    catch(error) {

    }
    
    let bot_bubble = document.createElement("p");
    bot_bubble.textContent = server_json["bot_response"];
    bot_bubble.classList.add("bot-message");
    conversation_messages.prepend(bot_bubble);
}

function load_events() {
    let send_message = document.querySelector("#send_message");
    send_message.addEventListener("click", exchange)
}

document.addEventListener("DOMContentLoaded", load_events);