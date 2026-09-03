import UsersListHeaderUI from "./UsersListHeaderUI.js";
import UsersListBodyUI from "./UsersListBodyUI.js";
import UsersListFooterUI from "./UsersListFooterUI.js";

export default class UsersListUI {
    constructor() {
        this.usersListEl = document.querySelector(".users-list");
        this.headerUI = new UsersListHeaderUI();
        this.bodyUI = new UsersListBodyUI();
        this.footerUI = new UsersListFooterUI();
    }

    show() {
        this.usersListEl?.classList.remove("hidden");
    }

    hide() {
        this.usersListEl?.classList.add("hidden");
    }

    getHeaderUI() {
        return this.headerUI;
    }

    getBodyUI() {
        return this.bodyUI;
    }

    getFooterUI() {
        return this.footerUI;
    }
}
