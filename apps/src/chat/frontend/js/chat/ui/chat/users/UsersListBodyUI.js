export default class UsersListBodyUI {

    #dummies = []

    constructor() {
        this.usersEl = document.querySelector(".users-list-body");
        // this.renderDummyUsers();
    }

    renderDummyUsers() {
        const dummyUsers = [
            { username: "Chelly", status: "Online", statusClass: "online" },
            { username: "Andi", status: "Offline", statusClass: "offline" },
            { username: "Sarah", status: "Online", statusClass: "online" }
        ];

        dummyUsers.forEach((user) => this.addDummyUser(user));
    }

    addDummyUser(user) {
        if(this.#dummies.includes(user.getUsername())){
            return false;
        }
        const userEl = document.createElement("div");
        userEl.classList.add("users-list-card");

        const avatarEl = document.createElement("img");
        avatarEl.classList.add("avatar");
        avatarEl.src = "/img/user_icon.jpg";
        avatarEl.alt = `${user.username} avatar`;

        const contentEl = document.createElement("div");
        contentEl.classList.add("content");

        const nameEl = document.createElement("p");
        nameEl.classList.add("name");
        nameEl.textContent = user.username;

        const statusEl = document.createElement("p");
        statusEl.classList.add("status", user.statusClass);
        statusEl.textContent = user.status;

        contentEl.append(nameEl, statusEl);

        const actionEl = document.createElement("button");
        actionEl.classList.add("users-list-action");
        actionEl.type = "button";
        actionEl.textContent = "View";

        userEl.append(avatarEl, contentEl, actionEl);
        this.usersEl?.appendChild(userEl);

        this.#dummies.push(user.getUsername());
        return true;
    }
}
