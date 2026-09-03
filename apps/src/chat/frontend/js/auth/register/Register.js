import RegisterUI from "../register/RegisterUI.js";

const registerUI = new RegisterUI();

registerUI.onSubmit(
    async (packet) => {
        if(registerUI.getUsername() === ""){
            registerUI.setLabel("Username cannot empty.", "red");
            return;
        }
        if(registerUI.getEmail() === ""){
            registerUI.setLabel("Email cannot empty.", "red");
            return;
        }
        if(registerUI.getPassword() === ""){
            registerUI.setLabel("Password cannot empty.", "red");
            return;
        }
        if(registerUI.getPassword() !== registerUI.getConfirmPassword()){
            registerUI.setLabel("Passwords do not match.", "red");
            return;
        }
        
        try {
            const response = await fetch("/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(packet.toData())
            });

            if (response.ok) {
                const successPage = await response.text();
                document.open();
                document.write(successPage);
                document.close();
                return;
            }

            if (response.status === 409) {
                registerUI.setLabel("Username or email already exists.", "red");
            } else if (response.status === 422) {
                registerUI.setLabel("Invalid registration data.", "red");
            } else {
                registerUI.setLabel("Unable to register. Please try again.", "red");
            }
        } catch (error) {
            console.error(error);
            registerUI.setLabel("Something went wrong. Please try again.", "red");
        }
    }
);

registerUI.onClickLoginButton(
    () => {
        window.location.href = "/page/login"
    }
);
