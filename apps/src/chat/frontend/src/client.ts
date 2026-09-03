export default class Client {

    public onOpen: (() => {}) | null = null;
    public onMessage: ((event: MessageEvent) => {}) | null = null;
    public onClose: ((event: CloseEvent) => {}) | null = null;

    private socket: WebSocket;
    
    constructor(){
        const protocol = location.protocol === "https:" ? "wss" : "ws";
        this.socket = new WebSocket(`${protocol}://${location.host}/`);
        this.socket.onopen = () => {
            this.onOpen?.();
        }
        this.socket.onmessage = (event: MessageEvent) => {
            this.onMessage?.(event);
        }
        this.socket.onclose = (event: CloseEvent) => {
            this.onClose?.(event);
        }
    }

    getSocket(): WebSocket {
        return this.socket;
    }

    sendData(data: any){
        const serializedData = JSON.stringify(data);
        this.socket.send(data);
    }

}