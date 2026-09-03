import PasswordResetRequestPacket from "../../packets/PasswordResetRequestPacket.js";

export default class EmailUI {

    constructor() {
        this.emailForm = document.querySelector(".card-form");
        this.message = document.querySelector(".email-message");
        this.usernameInput = document.querySelector(".username");
        this.emailInput = document.querySelector(".email");
    }

    getUsername() {
        return this.usernameInput ? this.usernameInput.value.trim() : "";
    }

    getEmail() {
        return this.emailInput ? this.emailInput.value.trim() : "";
    }

    setMessage(text, color = "red") {
        if (!this.message) return;

        this.message.textContent = text;
        this.message.style.color = color;
    }

    onSubmit(callback) {
        if (!this.emailForm) return;

        this.emailForm.addEventListener("submit", (event) => {
            event.preventDefault();

            const packet = new PasswordResetRequestPacket(
                this.getUsername(),
                this.getEmail()
            );

            callback(packet);
        });
    }
}
