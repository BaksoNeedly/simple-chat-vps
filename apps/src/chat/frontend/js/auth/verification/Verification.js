import VerificationHeaderUI from './VerificationHeaderUI.js';
import VerificationBodyUI from './VerificationBodyUI.js';
import VerificationFooterUI from './VerificationFooterUI.js';
import VerificationCodePacket from '../../packets/VerificationCodePacket.js';

export default class VerificationUI {
    constructor() {
        this.header = new VerificationHeaderUI();
        this.body = new VerificationBodyUI();
        this.footer = new VerificationFooterUI();

        this.setupEvents();
    }

    getHeaderUI() { return this.header; }
    getBodyUI() { return this.body; }
    getFooterUI() { return this.footer; }

    setupEvents() {
        this.body.onClickVerifyEmail(async (code) => { 
            this.body.showMessage(
                code.length === 6 ? 'Verification code submitted.' : 'Please enter all 6 digits.',
                code.length === 6 ? '#039855' : '#d92d20'
            );
            const codePacket = new VerificationCodePacket(String(code));
            const response = await fetch("/user/verify/code", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(codePacket.toData())
            });

            if(response.ok){
                // fetch follows HTTP redirects internally; it does not
                // navigate the current page automatically.
                window.location.href = response.redirected
                    ? response.url
                    : "/page/verified";
            }else{
                this.body.showMessage(
                    "Invalid verification code.",
                    "#d92e20"
                );
            }
        });

        this.footer.onClickReturn(async () => {
            window.location.href = "/user/return";
        });
    }
}

new VerificationUI();
