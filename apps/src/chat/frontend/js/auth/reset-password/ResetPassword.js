import ResetPasswordPacket from "../../packets/http/ResetPasswordPacket.js";

const query = new URLSearchParams(window.location.search);
const token = query.get("token");
const tokenInput = document.querySelector("#reset-token");
const form = document.querySelector(".card-form");
const passwordInput = document.querySelector("#password");
const confirmationInput = document.querySelector("#confirm-password");
const message = document.querySelector("#reset-message");

if (token) {
    tokenInput.value = token;
} else {
    message.textContent = "This password reset link is missing its token.";
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const password = passwordInput.value;
    const confirmation = confirmationInput.value;

    if (password !== confirmation) {
        message.textContent = "Passwords do not match.";
        return;
    }

    const packet = new ResetPasswordPacket(password, confirmation);

    try {
        const response = await fetch("/reset/password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                ...packet.toData(),
                token
            })
        });

        if (response.ok) {
            message.textContent = "Password updated successfully.";
            message.style.color = "#027a48";
            form.reset();
        } else {
            message.textContent = "Failed to update password.";
        }
    } catch (error) {
        console.error(error);
        message.textContent = "Something went wrong. Please try again.";
    }
});
