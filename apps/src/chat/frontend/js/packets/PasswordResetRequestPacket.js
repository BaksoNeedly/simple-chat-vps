export default class PasswordResetRequestPacket {

    constructor(username, email) {
        this.username = username;
        this.email = email;
    }

    toData() {
        return {
            type: "password_reset_request",
            username: this.username,
            email: this.email
        };
    }

    static fromData(data) {
        return new PasswordResetRequestPacket(
            data.username,
            data.email
        );
    }
}
