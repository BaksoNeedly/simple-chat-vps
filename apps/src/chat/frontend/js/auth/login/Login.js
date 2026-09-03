import LoginUI from "./LoginUI.js";

const loginUI = new LoginUI();

loginUI.onSubmit(
    async (packet) => {
        if(loginUI.getUsername() === ""){
            loginUI.setLabel("Username cannot empty.", "red");
            return;
        }
        if(loginUI.getPassword() == ""){
            loginUI.setLabel("Password cannot empty.", "red");
            return;
        }

        try {
            const response = await fetch("/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(packet.toData()),
                redirect: "follow"
            });

            if (response.redirected) {
                window.location.href = response.url;
                return;
            }

            if (response.status === 401) {
                loginUI.setLabel("Wrong password or username does not exist.", "red");
            } else {
                loginUI.setLabel("Unable to login. Please try again.", "red");
            }
        } catch (error) {
            console.error(error);
            loginUI.setLabel("Something went wrong. Please try again.", "red");
        }
    }
);

loginUI.onClickSignUp(
    () => {
        window.location.href = "/page/register";
    }
);
