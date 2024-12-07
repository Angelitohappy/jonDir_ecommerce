function verify_email(){
    let email = document.querySelector("#email");
    let error_message = document.querySelector("#email-error");
    let register_btn = document.querySelector("#send-email");
    
    const regex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
    
    if (!RegExp(regex).test(email.value) && error_message.classList.contains("hidden")) {
        error_message.classList.remove("hidden");
        register_btn.disabled = true;
    }
    else if (RegExp(regex).test(email.value) && !error_message.classList.contains("hidden")) {
        error_message.classList.add("hidden");
        register_btn.disabled = false;
    }
}

function load_events() {
    let email = document.querySelector("#email");

    email.addEventListener("focusout", verify_email);
}

document.addEventListener("DOMContentLoaded", load_events);
