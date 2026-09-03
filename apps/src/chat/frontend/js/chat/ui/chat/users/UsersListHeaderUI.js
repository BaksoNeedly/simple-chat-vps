export default class UsersListHeaderUI {
    constructor() {
        this.headerEl = document.querySelector(".users-list header");
        this.titleEl = this.headerEl?.querySelector(".title");
        this.returnButton = this.headerEl?.querySelector(".users-list-return");
    }

    getTitle() {
        return this.titleEl?.textContent ?? "";
    }

    setTitle(title) {
        if (this.titleEl) {
            this.titleEl.textContent = title;
        }
    }

    onExit(callback) {
        this.returnButton?.addEventListener("click", callback);
    }
}
