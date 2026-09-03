import EmailUI from "./EmailUI.js";

const emailUI = new EmailUI();

emailUI.onSubmit(async (packet) => {
    if (emailUI.getUsername() === "") {
        emailUI.setMessage("Username cannot be empty.");
        return;
    }

    if (emailUI.getEmail() === "") {
        emailUI.setMessage("Email cannot be empty.");
        return;
    }

    try {
        const response = await fetch("/reset/password/request", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(packet.toData())
        });

        if (response.ok) {
            emailUI.setMessage(
                "Password reset link sent successfully. Check your email.",
                "#027a48"
            );
        } else {
            emailUI.setMessage("Failed to send password reset link.");
        }
    } catch (error) {
        console.error(error);
        emailUI.setMessage("Something went wrong. Please try again.");
    }
});
