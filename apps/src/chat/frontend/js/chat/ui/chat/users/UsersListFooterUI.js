export default class UsersListFooterUI {
    constructor() {
        this.countEl = document.querySelector(".users-list-count");
    }

    setCount(count) {
        if (this.countEl) {
            this.countEl.textContent = `${count} users`;
        }
    }

    getCount() {
        return this.countEl?.textContent ?? "";
    }
}
