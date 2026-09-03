export default class JoinPacket {

    constructor(username = ""){
        this.username = username;
    }

    toData(){
        return {
            username: this.username,
            type: "join"
        }
    }

    static fromData(data){
        return new JoinPacket(data["username"]);
    }

    getUsername(){
        return this.username;
    }
}