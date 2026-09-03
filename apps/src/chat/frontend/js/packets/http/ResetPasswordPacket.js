export default class ResetPasswordPacket {

    constructor(password, confirm_password){
        this.password = password;
        this.confirmPassword = confirm_password;
    }

    toData(){
        return {
            type: "reset_password",
            password: this.password,
            confirm_password: this.confirmPassword
        }
    }

    static fromData(data){
        return new ResetPasswordPacket(
            data.password,
            data.confirm_password
        );
    }

    getPassword(){
        return this.password;
    }

    getConfirmPassword(){
        return this.confirmPassword;
    }
}