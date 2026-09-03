export default class UserPacket {

    constructor(
        username
    ){
        this.username = username;
    }

    toData(){
        return {
            username: this.username
        }
    }

    static fromData(data){
        return new UserPacket(data["username"]);
    }

    getUsername(){
        return this.username;
    }
}