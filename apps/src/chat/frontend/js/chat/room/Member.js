export default class Member {

    #username;

    constructor(
        username
    ){
        this.#username = username;
    }

    getUsername(){
        return this.#username;
    }

    static fromData(data){
        return new Member(data["username"]);
    }

    toData(){
        return {
            username: this.#username
        }
    }
}