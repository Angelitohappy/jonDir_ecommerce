function verify_password() {
    let password = document.querySelector("#new-password");
    let confirm_password = document.querySelector("#confirm-password");
    let error_message = document.querySelector("#password-error");
    let register_btn = document.querySelector("#reset-password");

    if (password.value !== confirm_password.value && error_message.classList.contains("hidden")) {
        error_message.classList.remove("hidden");
        register_btn.disabled = true;
    }
    else if (password.value === confirm_password.value && !error_message.classList.contains("hidden")) {
        error_message.classList.add("hidden");
        register_btn.disabled = false;
    }

}

function verify_password_original() {
    let confirm_password = document.querySelector("#confirm-password");
    if (confirm_password.value) {
        verify_password();
    }
}

function verify_email(){
    let email = document.querySelector("#email");
    let error_message = document.querySelector("#email-error");
    let register_btn = document.querySelector("#save-changes");
    
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
    let password = document.querySelector("#new-password");
    let confirm_password = document.querySelector("#confirm-password");
    let email = document.querySelector("#email");

    password.addEventListener("keyup", verify_password_original);
    confirm_password.addEventListener("keyup", verify_password);
    email.addEventListener("focusout", verify_email);
}

document.addEventListener("DOMContentLoaded", load_events);
