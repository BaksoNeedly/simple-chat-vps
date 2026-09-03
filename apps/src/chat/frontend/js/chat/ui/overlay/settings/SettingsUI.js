import SettingsHeaderUI from './SettingsHeaderUI.js';
import SettingsBodyUI from './SettingsBodyUI.js';
import SettingsFooterUI from './SettingsFooterUI.js';

export default class SettingsUI {
    constructor() {
        this.overlay = document.querySelector('.settings-overlay');
        this.settings = document.querySelector('.settings-panel');
        this.deleteOverlay = document.querySelector('.delete-account-overlay');
        this.deleteNoButton = document.querySelector('.delete-account-no');
        this.deleteYesButton = document.querySelector('.delete-account-yes');
        this.header = new SettingsHeaderUI();
        this.body = new SettingsBodyUI();
        this.footer = new SettingsFooterUI();

        document.querySelector('.settings-btn')?.addEventListener('click', () => this.show());
        this.body.onClickDeleteAccountBtn(() => this.showDeleteConfirmation());
        this.footer.onClickCloseBtn(() => this.hide());
        this.overlay?.addEventListener('click', event => {
            if (event.target === this.overlay) this.hide();
        });
        this.deleteNoButton?.addEventListener('click', () => this.hideDeleteConfirmation());
        this.deleteOverlay?.addEventListener('click', event => {
            if (event.target === this.deleteOverlay) this.hideDeleteConfirmation();
        });
    }

    getHeaderUI() { return this.header; }
    getBodyUI() { return this.body; }
    getFooterUI() { return this.footer; }

    show() {
        this.overlay?.classList.remove('hidden');
        this.settings?.classList.remove('hidden');
    }

    hide() {
        this.settings?.classList.add('hidden');
        this.overlay?.classList.add('hidden');
    }

    showDeleteConfirmation() {
        this.hide();
        this.deleteOverlay?.classList.remove('hidden');
    }

    hideDeleteConfirmation() {
        this.deleteOverlay?.classList.add('hidden');
    }

    onConfirmDeleteAccount(callback) {
        this.deleteYesButton?.addEventListener('click', () => {
            this.hideDeleteConfirmation();
            callback?.();
        });
    }
}
