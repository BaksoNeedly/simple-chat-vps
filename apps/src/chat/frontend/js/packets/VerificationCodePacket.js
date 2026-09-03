export default class VerificationCodePacket {

    constructor(code = "") {
        this.code = code;
    }

    toData() {
        return {
            type: "verification_code",
            code: this.code
        };
    }

    static fromData(data) {
        return new VerificationCodePacket(
            data.verification_code
        );
    }

    getCode() {
        return this.code;
    }
}
